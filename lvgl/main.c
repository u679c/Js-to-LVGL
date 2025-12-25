
      #include "lvgl.h"
      #include "lv_conf.h"
      #include "lv_drv_conf.h"
      #include "display/fbdev.h"
      #include "indev/evdev.h"
      #include "generated/ui_app.h"
      #include <unistd.h>

      #define SCREEN_W 1024
      #define SCREEN_H 600

      static void hal_init(void) {
        lv_init();
        fbdev_init();
        evdev_init();

        static lv_color_t buf1[SCREEN_W * 80];
        static lv_color_t buf2[SCREEN_W * 80];
        static lv_disp_draw_buf_t draw_buf;
        lv_disp_draw_buf_init(&draw_buf, buf1, buf2, SCREEN_W * 80);

        static lv_disp_drv_t disp_drv;
        lv_disp_drv_init(&disp_drv);
        disp_drv.hor_res = SCREEN_W;
        disp_drv.ver_res = SCREEN_H;
        disp_drv.flush_cb = fbdev_flush;
        disp_drv.draw_buf = &draw_buf;
#ifdef DISP_SW_ROTATE
        disp_drv.sw_rotate = DISP_SW_ROTATE;
#endif
#ifdef DISP_ROTATION
        disp_drv.rotated = DISP_ROTATION;
#endif
#ifdef DISP_FULL_REFRESH
        disp_drv.full_refresh = DISP_FULL_REFRESH;
#endif
        lv_disp_drv_register(&disp_drv);

        static lv_indev_drv_t indev_drv;
        lv_indev_drv_init(&indev_drv);
        indev_drv.type = LV_INDEV_TYPE_POINTER;
        indev_drv.read_cb = evdev_read;
        lv_indev_drv_register(&indev_drv);
      }

      int main(void) {
        hal_init();
        ui_build();
        while (1) {
          lv_timer_handler();
          usleep(5000);
        }
        return 0;
      }
