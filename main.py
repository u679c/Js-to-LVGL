"""Build script: translate web HTML/JS (text + buttons) into LVGL C code and optionally build.

Usage:
  python main.py           # generate LVGL sources (no build)
  python main.py --build   # generate and build (requires cmake/git/gcc/pkg-config/libsdl2-dev on Linux)
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

from util import SimpleParser, generate_c, Node, parse_messages

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
LVGL_DIR = ROOT / "lvgl"
DEPS_DIR = LVGL_DIR / ".deps"
GENERATED_DIR = LVGL_DIR / "generated"
BUILD_DIR = LVGL_DIR / "build"
LVGL_REPO = "https://github.com/lvgl/lvgl.git"
LVGL_REPO_FALLBACK = "https://github.com/lvgl/lvgl.git"
LV_DRIVERS_REPO = "https://github.com/lvgl/lv_drivers.git"
LV_DRIVERS_REPO_FALLBACK = "https://github.com/lvgl/lv_drivers.git"
# Use LVGL v8.3.11 (matches lv_drivers master API)
LV_TAG = "v8.3.11"
# lv_drivers has no v9.1 tag; use master
LV_DRIVERS_TAG = "master"


def run(cmd: list[str], cwd: Path | None = None) -> None:
  """Run a shell command and raise on failure."""
  print(f"[run] {' '.join(cmd)}")
  subprocess.run(cmd, cwd=cwd, check=True)


def ensure_dirs() -> None:
  for path in (DEPS_DIR, GENERATED_DIR, BUILD_DIR):
    path.mkdir(parents=True, exist_ok=True)


def write_lv_conf() -> None:
  target = LVGL_DIR / "lv_conf.h"
  target.write_text(
    textwrap.dedent(
      """
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
      """
    ),
    encoding="utf-8",
  )


def write_main_c() -> None:
  target = LVGL_DIR / "main.c"
  target.write_text(
    textwrap.dedent(
      r'''
      #include "lvgl.h"
      #include "lv_conf.h"
      #ifndef SDL_MAIN_HANDLED
      #define SDL_MAIN_HANDLED
      #endif
      #include <SDL2/SDL.h>
      #include "sdl/sdl.h"
      #include "generated/ui_app.h"

      #define SCREEN_W 720
      #define SCREEN_H 1280

      static void hal_init(void) {
        lv_init();
        sdl_init();

        static lv_color_t buf1[SCREEN_W * 80];
        static lv_color_t buf2[SCREEN_W * 80];
        static lv_disp_draw_buf_t draw_buf;
        lv_disp_draw_buf_init(&draw_buf, buf1, buf2, SCREEN_W * 80);

        static lv_disp_drv_t disp_drv;
        lv_disp_drv_init(&disp_drv);
        disp_drv.hor_res = SCREEN_W;
        disp_drv.ver_res = SCREEN_H;
        disp_drv.flush_cb = sdl_display_flush;
        disp_drv.draw_buf = &draw_buf;
        lv_disp_drv_register(&disp_drv);

        static lv_indev_drv_t indev_drv;
        lv_indev_drv_init(&indev_drv);
        indev_drv.type = LV_INDEV_TYPE_POINTER;
        indev_drv.read_cb = sdl_mouse_read;
        lv_indev_drv_register(&indev_drv);
      }

      int main(void) {
        hal_init();
        ui_build();
        while (1) {
          lv_timer_handler();
          SDL_Delay(5);
        }
        return 0;
      }
      '''
    ),
    encoding="utf-8",
  )


def write_lv_drv_conf() -> None:
  target = LVGL_DIR / "lv_drv_conf.h"
  target.write_text(
    textwrap.dedent(
      """
      #ifndef LV_DRV_CONF_H
      #define LV_DRV_CONF_H
      #define SDL_HOR_RES 720
      #define SDL_VER_RES 1280
      #define USE_SDL 1
      #define SDL_INCLUDE_PATH <SDL2/SDL.h>
      #define MONITOR_ZOOM 1
      #endif
      """
    ),
    encoding="utf-8",
  )


def write_ui_files() -> None:
  header = GENERATED_DIR / "ui_app.h"
  source = GENERATED_DIR / "ui_app.c"

  header.write_text(
    textwrap.dedent(
      """
      #pragma once
      void ui_build(void);
      """
    ),
    encoding="utf-8",
  )

  parser = SimpleParser()
  html_path = WEB_DIR / "index.html"
  parser.feed(html_path.read_text(encoding="utf-8", errors="ignore"))
  nodes = parser.nodes if parser.nodes else [Node("p", "(empty)")]
  js_path = WEB_DIR / "js" / "app.js"
  messages = parse_messages(js_path) if js_path.exists() else []
  c_body = generate_c(nodes, messages)
  source_content = '#include "ui_app.h"\n' + c_body
  source.write_text(source_content, encoding="utf-8")


def write_cmakelists() -> None:
  target = LVGL_DIR / "CMakeLists.txt"
  target.write_text(
    textwrap.dedent(
      """
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
      if(NOT EXISTS "${LV_DRIVERS_DIR}/sdl/sdl.c")
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
        ${LV_DRIVERS_DIR}/sdl/sdl.c
        ${LV_DRIVERS_DIR}/sdl/sdl_common.c
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
        SDL_MAIN_HANDLED
        LV_TICK_CUSTOM_INCLUDE="tick.h"
      )

      find_package(PkgConfig REQUIRED)
      pkg_check_modules(SDL2 REQUIRED sdl2)

      target_link_libraries(lvgl_web PRIVATE
        lvgl
        ${SDL2_LIBRARIES}
      )
      target_include_directories(lvgl_web PRIVATE ${SDL2_INCLUDE_DIRS})
      """
    ),
    encoding="utf-8",
  )


def write_build_sh() -> None:
  target = LVGL_DIR / "build.sh"
  target.write_text(
    textwrap.dedent(
      """
      #!/usr/bin/env bash
      set -euo pipefail
      SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
      BUILD_DIR="$SCRIPT_DIR/build"
      mkdir -p "$BUILD_DIR"
      cd "$BUILD_DIR"
      cmake .. -DCMAKE_BUILD_TYPE=Release \
        -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
        -DFETCHCONTENT_QUIET=OFF \
        -DLVGL_SOURCE_DIR="$SCRIPT_DIR/.deps/lvgl" \
        -DLV_DRIVERS_DIR="$SCRIPT_DIR/.deps/lv_drivers"
      cmake --build . --config Release
      echo "Executable located at $BUILD_DIR/lvgl_web"
      """
    ),
    encoding="utf-8",
  )
  os.chmod(target, 0o755)


def copy_web_assets() -> None:
  dest = LVGL_DIR / "web_snapshot"
  if dest.exists():
    shutil.rmtree(dest)
  shutil.copytree(WEB_DIR, dest)


def ensure_repo(name: str, urls: list[str], tag: str, dest: Path) -> None:
  if dest.exists():
    print(f"[download] {name} already present at {dest}")
    return
  dest.parent.mkdir(parents=True, exist_ok=True)
  for url in urls:
    print(f"[download] cloning {name} from {url} (tag {tag}) -> {dest}")
    try:
      run(["git", "clone", "--depth=1", "--branch", tag, "--progress", url, str(dest)])
      return
    except subprocess.CalledProcessError as exc:
      print(f"[warn] clone failed from {url}: {exc}")
      if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
  raise RuntimeError(f"All clone attempts failed for {name}")


def maybe_build() -> None:
  if platform.system().lower() != "linux":
    print("Build step skipped: not running on Linux.")
    return
  required = ["cmake", "git", "pkg-config"]
  missing = [cmd for cmd in required if shutil.which(cmd) is None]
  if missing:
    print(f"Build step skipped: missing tools {missing}")
    return
  ensure_repo("lvgl", [LVGL_REPO, LVGL_REPO_FALLBACK], LV_TAG, DEPS_DIR / "lvgl")
  ensure_repo("lv_drivers", [LV_DRIVERS_REPO, LV_DRIVERS_REPO_FALLBACK], LV_DRIVERS_TAG, DEPS_DIR / "lv_drivers")
  try:
    run(["bash", str(LVGL_DIR / "build.sh")])
  except subprocess.CalledProcessError as exc:
    print(f"Build failed: {exc}")


def main() -> None:
  parser = argparse.ArgumentParser(description="Generate LVGL demo from web UI.")
  parser.add_argument("--build", action="store_true", help="Attempt to compile the LVGL executable (Linux).")
  args = parser.parse_args()

  ensure_dirs()
  write_lv_conf()
  write_lv_drv_conf()
  write_main_c()
  write_ui_files()
  write_cmakelists()
  write_build_sh()
  copy_web_assets()

  tick_header = LVGL_DIR / "tick.h"
  tick_header.write_text(
    textwrap.dedent(
      """
      #pragma once
      #include <stdint.h>
      #include <SDL2/SDL.h>
      static inline uint32_t lv_tick_custom_handler(void) {
        return SDL_GetTicks();
      }
      """
    ),
    encoding="utf-8",
  )

  if args.build:
    maybe_build()
  print("LVGL sources generated under ./lvgl. Run main.py --build on Linux with SDL2 dev packages to compile.")


if __name__ == "__main__":
  main()
