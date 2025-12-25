"""
Minimal HTML+JS to LVGL translator:
- Supports text (<p>, <span>, <h1>-<h3>, <button>) and a simple click-to-cycle message array from JS.
- Layout: vertical stack centered.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import List

TEXT_TAGS = {"p", "span", "h1", "h2", "h3"}
BUTTON_TAGS = {"button"}


def parse_style(style: str) -> dict[str, str]:
  result: dict[str, str] = {}
  for chunk in style.split(";"):
    if ":" not in chunk:
      continue
    key, value = chunk.split(":", 1)
    key = key.strip().lower()
    value = value.strip()
    if key and value:
      result[key] = value
  return result


def parse_css_length(value: str | None) -> int | None:
  if not value:
    return None
  raw = value.strip().lower()
  if raw.endswith("px"):
    raw = raw[:-2].strip()
  if raw.endswith("%"):
    return None
  try:
    return int(round(float(raw)))
  except ValueError:
    return None


def parse_css_color(value: str | None) -> int | None:
  if not value:
    return None
  raw = value.strip().lower()
  if raw.startswith("#"):
    raw = raw[1:]
    if len(raw) == 3:
      raw = "".join(ch * 2 for ch in raw)
    if len(raw) == 6:
      try:
        return int(raw, 16)
      except ValueError:
        return None
    return None
  m = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", raw)
  if not m:
    return None
  r, g, b = (max(0, min(255, int(v))) for v in m.groups())
  return (r << 16) | (g << 8) | b


def pick_font(size_px: int | None) -> str | None:
  if size_px is None:
    return None
  options = [16, 18, 22, 30, 36]
  nearest = min(options, key=lambda v: abs(v - size_px))
  return f"&lv_font_montserrat_{nearest}"


class Node:
  def __init__(self, tag: str, text: str, attrs: dict[str, str]):
    self.tag = tag
    self.text = text.strip()
    self.attrs = attrs
    self.style = parse_style(attrs.get("style", ""))


class SimpleParser(HTMLParser):
  def __init__(self) -> None:
    super().__init__()
    self.nodes: List[Node] = []
    self._current_tag: str | None = None
    self._buffer: List[str] = []
    self._current_attrs: dict[str, str] = {}

  def handle_starttag(self, tag, attrs):
    if tag in TEXT_TAGS or tag in BUTTON_TAGS:
      self._current_tag = tag
      self._buffer = []
      self._current_attrs = {k: (v if v is not None else "") for k, v in attrs}

  def handle_endtag(self, tag):
    if tag == self._current_tag:
      self._flush(tag)
      self._current_tag = None
      self._current_attrs = {}

  def handle_data(self, data):
    if self._current_tag:
      self._buffer.append(data)

  def _flush(self, tag: str):
    if self._buffer:
      text = "".join(self._buffer).strip()
      if text:
        self.nodes.append(Node(tag, text, dict(self._current_attrs)))
    self._buffer = []


def parse_messages(js_path: Path) -> list[str]:
  if not js_path.exists():
    return []
  text = js_path.read_text(encoding="utf-8", errors="ignore")
  m = re.search(r"messages\s*=\s*\[([^\]]+)\]", text)
  if not m:
    return []
  raw = m.group(1)
  parts = re.findall(r'"([^"]+)"', raw) + re.findall(r"'([^']+)'", raw)
  return [p.strip() for p in parts if p.strip()]


def generate_c(nodes: list[Node], messages: list[str]) -> str:
  title = next((n.text for n in nodes if n.tag in ("h1", "h2", "h3")), "LVGL Demo")
  text_nodes = [n for n in nodes if n.tag in TEXT_TAGS]
  button_nodes = [n for n in nodes if n.tag in BUTTON_TAGS]
  button_texts = [n.text for n in button_nodes]
  btn_text = button_texts[0] if button_texts else "Click"
  multi_buttons = len(button_texts) > 1
  first_text = text_nodes[0].text if text_nodes else ""
  if not first_text:
    first_text = "Tap a cell"
  use_messages = bool(messages)
  if use_messages:
    msgs = messages
  else:
    msgs = [first_text]
  msg_array = ",\n  ".join(f"\"{m}\"" for m in msgs)
  grid_cols = min(10, max(1, len(button_texts))) if multi_buttons else 1
  grid_rows = (len(button_texts) + grid_cols - 1) // grid_cols if multi_buttons else 1
  btn_w_pct = max(1, 100 // grid_cols) if multi_buttons else 100
  btn_h_pct = max(1, 100 // grid_rows) if multi_buttons else 100
  use_absolute = any(
    n.style.get("position") == "absolute"
    or any(k in n.style for k in ("left", "top", "width", "height"))
    or any(k in n.attrs for k in ("data-x", "data-y", "data-w", "data-h"))
    for n in nodes
  )
  lines = []
  lines.append('#include "lvgl.h"')
  lines.append("")
  lines.append("static lv_obj_t * display_label;")
  if use_messages:
    lines.append(f"static const char * messages[] = {{\n  {msg_array}\n}};")
    lines.append("static int msg_idx = 0;")
    lines.append("")
    lines.append("static void btn_event_cb(lv_event_t * e) {")
    lines.append("  msg_idx = (msg_idx + 1) % (sizeof(messages)/sizeof(messages[0]));")
    lines.append("  lv_label_set_text(display_label, messages[msg_idx]);")
    lines.append("}")
  else:
    if multi_buttons:
      label_array = ",\n  ".join(f"\"{m}\"" for m in button_texts)
      lines.append(f"static const char * button_labels[] = {{\n  {label_array}\n}};")
      lines.append("")
    lines.append("static void btn_event_cb(lv_event_t * e) {")
    lines.append("  const char * label = (const char *)lv_event_get_user_data(e);")
    lines.append("  if (label) {")
    lines.append("    lv_label_set_text(display_label, label);")
    lines.append("  }")
    lines.append("}")
  lines.append("")
  lines.append("void ui_build(void) {")
  lines.append("  lv_obj_t * layer = lv_layer_top();")
  lines.append("  lv_obj_t * scr = lv_obj_create(layer);")
  lines.append("  lv_obj_remove_style_all(scr);")
  lines.append("  lv_obj_set_size(scr, lv_pct(100), lv_pct(100));")
  lines.append("  lv_obj_set_style_bg_color(scr, lv_color_hex(0x0b1d36), 0);")
  lines.append("  lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);")
  lines.append("  lv_obj_clear_flag(scr, LV_OBJ_FLAG_SCROLLABLE);")
  lines.append("  lv_obj_add_flag(scr, LV_OBJ_FLAG_CLICKABLE);")
  if use_absolute:
    created_label = False
    button_idx = 0
    for idx, node in enumerate(nodes):
      if node.tag in TEXT_TAGS:
        lines.append(f"  lv_obj_t * label_{idx} = lv_label_create(scr);")
        lines.append(f"  lv_label_set_text(label_{idx}, \"{node.text}\");")
        if not created_label:
          lines.append(f"  display_label = label_{idx};")
          created_label = True
        text_color = parse_css_color(node.style.get("color"))
        if text_color is not None:
          lines.append(f"  lv_obj_set_style_text_color(label_{idx}, lv_color_hex(0x{text_color:06x}), 0);")
        font_ptr = pick_font(parse_css_length(node.style.get("font-size")))
        if font_ptr:
          lines.append(f"  lv_obj_set_style_text_font(label_{idx}, {font_ptr}, 0);")
        left = parse_css_length(node.style.get("left")) or parse_css_length(node.attrs.get("data-x"))
        top = parse_css_length(node.style.get("top")) or parse_css_length(node.attrs.get("data-y"))
        width = parse_css_length(node.style.get("width")) or parse_css_length(node.attrs.get("data-w"))
        height = parse_css_length(node.style.get("height")) or parse_css_length(node.attrs.get("data-h"))
        if width is not None or height is not None:
          lines.append(f"  lv_obj_set_size(label_{idx}, {width if width is not None else 'LV_SIZE_CONTENT'}, {height if height is not None else 'LV_SIZE_CONTENT'});")
        if left is not None or top is not None:
          lines.append(f"  lv_obj_set_pos(label_{idx}, {left if left is not None else 0}, {top if top is not None else 0});")
      elif node.tag in BUTTON_TAGS:
        lines.append(f"  lv_obj_t * btn_{idx} = lv_btn_create(scr);")
        left = parse_css_length(node.style.get("left")) or parse_css_length(node.attrs.get("data-x"))
        top = parse_css_length(node.style.get("top")) or parse_css_length(node.attrs.get("data-y"))
        width = parse_css_length(node.style.get("width")) or parse_css_length(node.attrs.get("data-w"))
        height = parse_css_length(node.style.get("height")) or parse_css_length(node.attrs.get("data-h"))
        if width is not None or height is not None:
          lines.append(f"  lv_obj_set_size(btn_{idx}, {width if width is not None else 'LV_SIZE_CONTENT'}, {height if height is not None else 'LV_SIZE_CONTENT'});")
        if left is not None or top is not None:
          lines.append(f"  lv_obj_set_pos(btn_{idx}, {left if left is not None else 0}, {top if top is not None else 0});")
        bg_color = parse_css_color(node.style.get("background-color") or node.style.get("background"))
        if bg_color is not None:
          lines.append(f"  lv_obj_set_style_bg_color(btn_{idx}, lv_color_hex(0x{bg_color:06x}), 0);")
        lines.append(f"  lv_obj_t * btn_label_{idx} = lv_label_create(btn_{idx});")
        lines.append(f"  lv_label_set_text(btn_label_{idx}, \"{node.text}\");")
        lines.append(f"  lv_obj_center(btn_label_{idx});")
        label_color = parse_css_color(node.style.get("color"))
        if label_color is not None:
          lines.append(f"  lv_obj_set_style_text_color(btn_label_{idx}, lv_color_hex(0x{label_color:06x}), 0);")
        font_ptr = pick_font(parse_css_length(node.style.get("font-size")))
        if font_ptr:
          lines.append(f"  lv_obj_set_style_text_font(btn_label_{idx}, {font_ptr}, 0);")
        if use_messages:
          lines.append(f"  lv_obj_add_event_cb(btn_{idx}, btn_event_cb, LV_EVENT_CLICKED, NULL);")
        else:
          label_ref = f"button_labels[{button_idx}]" if multi_buttons else f"\"{node.text}\""
          lines.append(f"  lv_obj_add_event_cb(btn_{idx}, btn_event_cb, LV_EVENT_CLICKED, (void *){label_ref});")
        if multi_buttons:
          button_idx += 1
    if not text_nodes:
      lines.append("  display_label = lv_label_create(scr);")
      lines.append(f"  lv_label_set_text(display_label, \"{first_text}\");")
      lines.append("  lv_obj_set_pos(display_label, 0, 0);")
  else:
    lines.append("  lv_obj_set_flex_flow(scr, LV_FLEX_FLOW_COLUMN);")
    lines.append("  lv_obj_set_flex_align(scr, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);")
    lines.append("  lv_obj_set_style_pad_all(scr, 20, 0);")
    lines.append("")
    lines.append("  lv_obj_t * title = lv_label_create(scr);")
    lines.append(f"  lv_label_set_text(title, \"{title}\");")
    lines.append("  lv_obj_set_style_text_color(title, lv_color_hex(0x8ab4ff), 0);")
    lines.append("")
    lines.append("  display_label = lv_label_create(scr);")
    lines.append(f"  lv_label_set_text(display_label, \"{first_text}\");")
    lines.append("  lv_obj_set_style_text_font(display_label, LV_FONT_DEFAULT, 0);")
    lines.append("  lv_obj_set_style_pad_bottom(display_label, 12, 0);")
    lines.append("")
    if multi_buttons:
      lines.append("  lv_obj_t * grid = lv_obj_create(scr);")
      lines.append("  lv_obj_remove_style_all(grid);")
      lines.append("  lv_obj_set_size(grid, lv_pct(100), lv_pct(100));")
      lines.append("  lv_obj_set_style_bg_opa(grid, LV_OPA_TRANSP, 0);")
      lines.append("  lv_obj_set_style_pad_all(grid, 4, 0);")
      lines.append("  lv_obj_set_style_pad_row(grid, 4, 0);")
      lines.append("  lv_obj_set_style_pad_column(grid, 4, 0);")
      lines.append("  lv_obj_set_flex_flow(grid, LV_FLEX_FLOW_ROW_WRAP);")
      lines.append("  lv_obj_set_flex_align(grid, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_START, LV_FLEX_ALIGN_START);")
      lines.append("  lv_obj_set_flex_grow(grid, 1);")
      for idx, label in enumerate(button_texts):
        lines.append("  {")
        lines.append("    lv_obj_t * btn = lv_btn_create(grid);")
        lines.append(f"    lv_obj_set_size(btn, lv_pct({btn_w_pct}), lv_pct({btn_h_pct}));")
        lines.append("    lv_obj_t * btn_label = lv_label_create(btn);")
        lines.append(f"    lv_label_set_text(btn_label, \"{label}\");")
        lines.append("    lv_obj_center(btn_label);")
        if use_messages:
          lines.append("    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);")
        else:
          lines.append(f"    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, (void *)button_labels[{idx}]);")
        lines.append("  }")
    else:
      lines.append("  lv_obj_t * btn = lv_btn_create(scr);")
      lines.append(f"  lv_obj_set_size(btn, LV_SIZE_CONTENT, LV_SIZE_CONTENT);")
      lines.append(f"  lv_obj_set_style_pad_all(btn, 10, 0);")
      lines.append(f"  lv_obj_t * btn_label = lv_label_create(btn);")
      lines.append(f"  lv_label_set_text(btn_label, \"{btn_text}\");")
      lines.append("  lv_obj_center(btn_label);")
      if use_messages:
        lines.append("  lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);")
      else:
        lines.append(f"  lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, (void *)\"{btn_text}\");")
  lines.append("}")
  return "\n".join(lines)
