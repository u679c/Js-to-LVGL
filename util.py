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


class Node:
  def __init__(self, tag: str, text: str):
    self.tag = tag
    self.text = text.strip()


class SimpleParser(HTMLParser):
  def __init__(self) -> None:
    super().__init__()
    self.nodes: List[Node] = []
    self._current_tag: str | None = None
    self._buffer: List[str] = []

  def handle_starttag(self, tag, attrs):
    if tag in TEXT_TAGS or tag in BUTTON_TAGS:
      self._current_tag = tag
      self._buffer = []

  def handle_endtag(self, tag):
    if tag == self._current_tag:
      self._flush(tag)
      self._current_tag = None

  def handle_data(self, data):
    if self._current_tag:
      self._buffer.append(data)

  def _flush(self, tag: str):
    if self._buffer:
      text = "".join(self._buffer).strip()
      if text:
        self.nodes.append(Node(tag, text))
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
  first_text = next((n.text for n in nodes if n.tag in TEXT_TAGS), "(empty)")
  btn_text = next((n.text for n in nodes if n.tag in BUTTON_TAGS), "Click")
  msgs = messages if messages else [first_text]
  msg_array = ",\n  ".join(f"\"{m}\"" for m in msgs)
  lines = []
  lines.append('#include "lvgl.h"')
  lines.append("")
  lines.append("static lv_obj_t * display_label;")
  lines.append(f"static const char * messages[] = {{\n  {msg_array}\n}};")
  lines.append("static int msg_idx = 0;")
  lines.append("")
  lines.append("static void btn_event_cb(lv_event_t * e) {")
  lines.append("  msg_idx = (msg_idx + 1) % (sizeof(messages)/sizeof(messages[0]));")
  lines.append("  lv_label_set_text(display_label, messages[msg_idx]);")
  lines.append("}")
  lines.append("")
  lines.append("void ui_build(void) {")
  lines.append("  lv_obj_t * scr = lv_scr_act();")
  lines.append("  lv_obj_set_style_bg_color(scr, lv_color_hex(0x0b1d36), 0);")
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
  lines.append("  lv_obj_t * btn = lv_btn_create(scr);")
  lines.append(f"  lv_obj_set_size(btn, LV_SIZE_CONTENT, LV_SIZE_CONTENT);")
  lines.append(f"  lv_obj_set_style_pad_all(btn, 10, 0);")
  lines.append(f"  lv_obj_t * btn_label = lv_label_create(btn);")
  lines.append(f"  lv_label_set_text(btn_label, \"{btn_text}\");")
  lines.append("  lv_obj_center(btn_label);")
  lines.append("  lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);")
  lines.append("}")
  return "\n".join(lines)
