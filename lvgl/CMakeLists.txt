
cmake_minimum_required(VERSION 3.16)
project(lvgl_web_ui C)
set(CMAKE_C_STANDARD 99)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)
# v8.3.11 matches lv_drivers master API
set(LVGL_TAG v8.3.11)
set(LV_DRIVERS_TAG master)

set(LVGL_GIT_URL_DEFAULT "https://github.com/lvgl/lvgl.git")
set(LVGL_GIT_URL "${LVGL_GIT_URL_DEFAULT}" CACHE STRING "LVGL git URL")
set(LVGL_SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/.deps/lvgl" CACHE PATH "Local LVGL source path")

# lv_drivers is used as a source directory only (no CMake from that repo).
set(LV_DRIVERS_DIR "${CMAKE_CURRENT_LIST_DIR}/.deps/lv_drivers" CACHE PATH "Local LV drivers path")
if(NOT EXISTS "${LV_DRIVERS_DIR}/display/fbdev.c" OR NOT EXISTS "${LV_DRIVERS_DIR}/indev/evdev.c")
  message(FATAL_ERROR "lv_drivers not found at ${LV_DRIVERS_DIR}; please run main.py --build to prefetch.")
endif()

FetchContent_Declare(
  lvgl
  GIT_REPOSITORY ${LVGL_GIT_URL}
  GIT_TAG ${LVGL_TAG}
  SOURCE_DIR ${LVGL_SOURCE_DIR}
)
FetchContent_MakeAvailable(lvgl)

target_compile_definitions(lvgl PUBLIC
  LV_CONF_INCLUDE_SIMPLE
  LV_LVGL_H_INCLUDE_SIMPLE
)
target_include_directories(lvgl PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(lvgl_web
  main.c
  generated/ui_app.c
  ${LV_DRIVERS_DIR}/display/fbdev.c
  ${LV_DRIVERS_DIR}/indev/evdev.c
)

target_include_directories(lvgl_web PRIVATE
  ${lvgl_SOURCE_DIR}
  ${LV_DRIVERS_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/generated
)

target_compile_definitions(lvgl_web PRIVATE
  LV_CONF_INCLUDE_SIMPLE
  LV_DRV_CONF_INCLUDE_SIMPLE
  LV_LVGL_H_INCLUDE_SIMPLE
  LV_TICK_CUSTOM_INCLUDE="tick.h"
)

target_link_libraries(lvgl_web PRIVATE
  lvgl
)
