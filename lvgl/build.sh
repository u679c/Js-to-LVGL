
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
BUILD_DIR="$SCRIPT_DIR/build"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake .. -DCMAKE_BUILD_TYPE=Release         -DFETCHCONTENT_FULLY_DISCONNECTED=ON         -DFETCHCONTENT_QUIET=OFF         -DLVGL_SOURCE_DIR="$SCRIPT_DIR/.deps/lvgl"         -DLV_DRIVERS_DIR="$SCRIPT_DIR/.deps/lv_drivers"
cmake --build . --config Release
echo "Executable located at $BUILD_DIR/lvgl_web"
