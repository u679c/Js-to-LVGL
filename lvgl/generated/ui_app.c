#include "ui_app.h"
#include "lvgl.h"

static lv_obj_t * display_label;
static const char * messages[] = {
  "now：waiting",
  "now：running",
  "now：completed"
};
static int msg_idx = 0;

static void btn_event_cb(lv_event_t * e) {
  msg_idx = (msg_idx + 1) % (sizeof(messages)/sizeof(messages[0]));
  lv_label_set_text(display_label, messages[msg_idx]);
}

void ui_build(void) {
  lv_obj_t * layer = lv_layer_top();
  lv_obj_t * scr = lv_obj_create(layer);
  lv_obj_remove_style_all(scr);
  lv_obj_set_size(scr, lv_pct(100), lv_pct(100));
  lv_obj_set_style_bg_color(scr, lv_color_hex(0x0b1d36), 0);
  lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);
  lv_obj_clear_flag(scr, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_add_flag(scr, LV_OBJ_FLAG_CLICKABLE);
  lv_obj_set_flex_flow(scr, LV_FLEX_FLOW_COLUMN);
  lv_obj_set_flex_align(scr, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
  lv_obj_set_style_pad_all(scr, 20, 0);

  lv_obj_t * title = lv_label_create(scr);
  lv_label_set_text(title, "Touch Grid");
  lv_obj_set_style_text_color(title, lv_color_hex(0x8ab4ff), 0);

  display_label = lv_label_create(scr);
  lv_label_set_text(display_label, "Touch Grid");
  lv_obj_set_style_text_font(display_label, LV_FONT_DEFAULT, 0);
  lv_obj_set_style_pad_bottom(display_label, 12, 0);

  lv_obj_t * grid = lv_obj_create(scr);
  lv_obj_remove_style_all(grid);
  lv_obj_set_size(grid, lv_pct(100), lv_pct(100));
  lv_obj_set_style_bg_opa(grid, LV_OPA_TRANSP, 0);
  lv_obj_set_style_pad_all(grid, 4, 0);
  lv_obj_set_style_pad_row(grid, 4, 0);
  lv_obj_set_style_pad_column(grid, 4, 0);
  lv_obj_set_flex_flow(grid, LV_FLEX_FLOW_ROW_WRAP);
  lv_obj_set_flex_align(grid, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_START, LV_FLEX_ALIGN_START);
  lv_obj_set_flex_grow(grid, 1);
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,0");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,1");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,2");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,3");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,4");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "0,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "1,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "2,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "3,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "4,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "5,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "6,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "7,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "8,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
  {
    lv_obj_t * btn = lv_btn_create(grid);
    lv_obj_set_size(btn, lv_pct(10), lv_pct(16));
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "9,5");
    lv_obj_center(btn_label);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
  }
}