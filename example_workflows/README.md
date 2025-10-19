# 示例工作流使用指南

本目录包含以下 ComfyUI 工作流 JSON 文件：
- `doubao_chat_workflow.json`（对话/可选图像）
- `doubao_seedream4_t2i_workflow.json`（文生图）
- `doubao_seedream4_i2i_workflow.json`（图生图）
- `doubao_seedream4_multi_fusion_workflow.json`（多图融合）
- `doubao_seedream4_stream_workflow.json`（顺序多图输出）

## 导入方式
1. 启动 ComfyUI。
2. 将上述 JSON 文件拖拽到画布，或在菜单中选择导入工作流。
3. 在节点的 `api_key` 输入框填入你的 Ark API Key（不要把 Key 写入仓库）。

## 节点参数要点
- `model`：
  - 对话：`doubao-pro`（可根据实际可用模型调整）。
  - 图生成：`doubao-seedream-4-0-250828`（示例默认）。
- `size`：在 `1K/2K/4K` 与像素尺寸（如 `2048×2048`）二选一，勿混用。详见 `../docs/seedream4-sizing.md`。
- `sequential_image_generation`：
  - `disabled`：单张输出（默认）。
  - `auto`：顺序生成多张；结合 `max_images` 控制数量。

## 典型连接
- 对话：将 `response` 连接到 `PrimitiveNode(STRING)` 或其他文本节点查看结果。
- 文生图：将 `image` 连接到 `PreviewImage` 或 `SaveImage`。
- 图生图：在 `image` 输入连接一个 `LoadImage` 或上游图像输出。
- 多图融合：用 `StackImages` 或多个 `LoadImage` 的批量输出连接到 `images`。
- 流式输出：设置 `sequential_image_generation=auto` 并调节 `max_images`。

## 故障排查
- 无图返回/400：检查 `api_key`、配额与尺寸混用问题；参考图是否过大或格式不对。
- 速度与成本：提升至 `4K` 会显著增加成本与时延，请按需选择。

## 许可与贡献
- 许可证见仓库根目录 `LICENSE`（MIT）。欢迎通过 GitHub Issues 提出需求或反馈。