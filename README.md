# Js-to-LVGL

将一段极简 HTML/JS 转换成 LVGL C 代码的小工具。当前只面向快速原型：读取 `web/index.html` 与 `web/js/app.js`，生成 `lvgl/generated/ui_app.c` 等文件，必要时可在 Linux 上编译出 SDL 演示程序。

## 快速开始
- 需要 Python 3；生成代码：`python main.py`（输出位于 `lvgl/`）。
- Linux 上可尝试编译：`python main.py --build`，需预装 `cmake`、`git`、`pkg-config`、SDL2 开发包。其他平台仅做代码生成。
- 生成的 LVGL 项目包含 `lv_conf.h`、`lv_drv_conf.h`、`main.c`、`generated/ui_app.c`，并会拷贝当前 `web/` 为快照。

## 版本列表
- V 2025.12.16-r1：仅支持的标签/功能：
  - HTML 标签：`<p>`、`<span>`、`<h1>`-`<h3>`（文本），`<button>`（单个按钮）。
  - JS：解析 `web/js/app.js` 中 `messages = [...]` 的字符串数组，按钮点击轮换显示。
  - 布局：单屏垂直居中堆叠，背景/配色为内置默认值。

## 注意事项
- 未实现任意布局、样式映射或多按钮交互；其他标签会被忽略。
- 构建脚本会自动尝试拉取 `lvgl` 与 `lv_drivers`（深度 1，指定 tag），请确保网络可用或提前放入 `lvgl/.deps/`。
