# 示例工作流（ComfyUI-JmcAI）

本目录提供了适配 `ComfyUI-JmcAI` 的示例 JSON 工作流，涵盖 Doubao Chat 与 Seedream 4.0 的文生图、图生图、多图融合、流式输出。

## 导入方式
- 在 ComfyUI 画布中：菜单导入 JSON，或将 JSON 文件拖拽到画布。
- 导入后，找到左侧节点库分类 `JmcAI/Doubao`（或搜索 `JmcAI`/`Doubao`/`Seedream4`）。

## 节点关键参数
- `api_key`：必填；建议通过环境变量或安全管理器提供，不要硬编码。
- `model`：默认 Chat `doubao-pro`，图生成 `doubao-seedream-4-0-250828`。
- `size`：Seedream 4.0 支持预设（如 `1K/2K/4K`）与像素（如 `2048×2048`）；不要混用。
- `sequential_image_generation`：`auto` 顺序生成多图（可配 `max_images`）；`disabled` 为单图输出。
- `seed`：可复现生成结果；默认 `-1` 随机。
- `watermark`：开关水印。

## 典型连接
- 将输出 `IMAGE` 连接到 `PreviewImage` 或 `SaveImage` 查看/保存。
- Chat 节点输出为 `STRING`，可用作文本流入其他节点。

## 文件列表
- `doubao_chat_workflow.json`
- `doubao_seedream4_t2i_workflow.json`
- `doubao_seedream4_i2i_workflow.json`
- `doubao_seedream4_multi_fusion_workflow.json`
- `doubao_seedream4_stream_workflow.json`

## 常见问题
- 搜不到节点：重启 ComfyUI；确认插件安装在 `custom_nodes/comfyui-jmcai`（或临时 `comfyui-doubao`）；检查启动日志是否有导入错误。
- 400 或无图返回：检查 `api_key`/配额、尺寸参数选择是否一致、参考图尺寸与格式。

## 许可
- MIT（遵循仓库根目录 `LICENSE`）。