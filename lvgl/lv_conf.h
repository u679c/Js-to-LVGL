
#ifndef LV_CONF_H
#define LV_CONF_H
#define LV_USE_LOG 1
#define LV_COLOR_DEPTH 32
#define LV_USE_FONT_ROBOTO 0
#define LV_USE_FONT_MONTSERRAT 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_MONTSERRAT_18 1
#define LV_FONT_MONTSERRAT_22 1
#define LV_FONT_MONTSERRAT_30 1
#define LV_FONT_MONTSERRAT_36 1
#define LV_FONT_DEFAULT &lv_font_montserrat_16
#define LV_TICK_CUSTOM 1
#define LV_TICK_CUSTOM_INCLUDE "tick.h"
#define LV_TICK_CUSTOM_SYS_TIME_EXPR (lv_tick_custom_handler())
#endif
