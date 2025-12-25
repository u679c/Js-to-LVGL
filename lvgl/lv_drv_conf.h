
#ifndef LV_DRV_CONF_H
#define LV_DRV_CONF_H
#define USE_FBDEV 1
#define USE_EVDEV 1
#define FBDEV_HOR_RES 1024
#define FBDEV_VER_RES 600
#define FBDEV_BUFFER_SIZE (FBDEV_HOR_RES * 80)
#define FBDEV_DEV "/dev/fb0"
#define EVDEV_NAME "/dev/input/event0"
#define DISP_SW_ROTATE 1
#define DISP_ROTATION LV_DISP_ROT_90
#define DISP_FULL_REFRESH 1
#endif
