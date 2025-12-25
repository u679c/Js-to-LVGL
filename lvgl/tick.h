
#pragma once
#include <stdint.h>
#include <sys/time.h>
static inline uint32_t lv_tick_custom_handler(void) {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return (uint32_t)(tv.tv_sec * 1000u + (uint32_t)(tv.tv_usec / 1000u));
}
