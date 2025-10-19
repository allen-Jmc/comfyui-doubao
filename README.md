# ComfyUI-Doubao 插件使用说明

> 为 ComfyUI 提供 Doubao/Seedream 能力的自定义节点与示例工作流。

## 插件总览与结构
- 能力：
  - 文本对话：`VolcengineChatAPI`（支持可选图像作为多模态输入）。
  - Seedream 4.0 图像生成：文生图、图生图、多图融合、流式输出。
- 预置示例工作流：位于 `example_workflows/`，默认尺寸已统一为 `"2K"`。

### 插件列表
- `VolcengineChatAPI`：对话补全，输入 `api_key`、`model`、`prompt`；可选 `image`；输出 `response`。
- `VolcengineSeedream4TextToImage`：文生图；输出 `IMAGE`。
- `VolcengineSeedream4ImageToImage`：图生图；需 `image` 参考图；输出 `IMAGE`。
- `VolcengineSeedream4MultiImageFusion`：多图融合；需 `images` 批量参考图；输出 `IMAGE`。
- `VolcengineSeedream4StreamOutput`：顺序多图流式输出；输出 `IMAGE`（多张）。

### 示例工作流
- `example_workflows/doubao_chat_workflow.json`（对话）
- `example_workflows/doubao_seedream4_t2i_workflow.json`（文生图）
- `example_workflows/doubao_seedream4_i2i_workflow.json`（图生图）
- `example_workflows/doubao_seedream4_multi_fusion_workflow.json`（多图融合）
- `example_workflows/doubao_seedream4_stream_workflow.json`（顺序多图）

## 安装与环境
- 依赖：
  - Python 包：见 `requirements.txt`（`requests`, `Pillow`, `numpy`）
- 安装步骤：
  - 安装依赖：`pip install -r requirements.txt`
  - 放置插件：将整个仓库置于 ComfyUI 的 `custom_nodes/` 下（如 `~/ComfyUI/custom_nodes/comfyui-doubao`），或以符号链接方式加入。
  - 重启 ComfyUI：在节点面板搜索 `Doubao` 分类确认加载成功。
- Ark API Key：
  - 在各节点的 `api_key` 输入框填入你的 Key；建议不要将 Key 写入仓库。
  - 可将 Key 存于安全管理器或环境变量中，按需复制到 ComfyUI 节点。

## 快速上手
1. 启动 ComfyUI 并导入示例工作流（菜单或将 JSON 拖拽至画布）：
   - `example_workflows/doubao_chat_workflow.json`
   - `example_workflows/doubao_seedream4_t2i_workflow.json`
   - `example_workflows/doubao_seedream4_i2i_workflow.json`
   - `example_workflows/doubao_seedream4_multi_fusion_workflow.json`
   - `example_workflows/doubao_seedream4_stream_workflow.json`
2. 在节点的 `api_key` 输入框填入你的 Ark API Key。
3. 设置 `model`：对话默认 `doubao-pro`，图生成默认 `doubao-seedream-4-0-250828`；设置 `prompt` 和 `size`（图生成默认 `"2K"`）。
4. 将 `image` 输出连接到 `PreviewImage` 或 `SaveImage` 查看结果。

## 尺寸选择
- 支持两种方式：
  - 预设等级：`"1K"`、`"2K"`、`"4K"`（限制最大边长，按纵横比自适应宽高）。
  - 像素尺寸：如 `"2048x2048"`（固定宽高）。
- 二选一：同一请求中只能使用一种方式，不可混用。
- 详细说明见文档：`docs/seedream4-sizing.md`

## 节点清单
- `VolcengineChatAPI`：对话，支持可选图像多模态；输出 `response`。
- `VolcengineSeedream4TextToImage`：文生图；输出 `IMAGE`。
- `VolcengineSeedream4ImageToImage`：图生图；需 `image`；输出 `IMAGE`。
- `VolcengineSeedream4MultiImageFusion`：多图融合；需 `images`；输出 `IMAGE`。
- `VolcengineSeedream4StreamOutput`：顺序多图；默认 `sequential_image_generation="auto"`；输出 `IMAGE`。

## 使用建议
- 参考图长边不应超过目标等级（如使用 `"4K"`，建议长边 ≤ 4096）。
- 预设与像素不要混用；混用可能导致 400 错误。
- 多图融合时请准备纵横比相近的参考图，以减少裁切和意外效果。

## 常见问题与排查
- 无图返回或 400：检查 `api_key`/配额、`size`（预设或像素二选一）、参考图尺寸/格式。
- 顺序生成限速：适当降低 `max_images` 或关闭 `sequential_image_generation="auto"`。
- 混用尺寸：不要同时使用预设与像素尺寸。

## 示例与预览
- 本地预览静态文件：
  ```bash
  python3 -m http.server 8001
  ```
- 打开：
  - `http://localhost:8001/example_workflows/doubao_chat_workflow.json`
  - `http://localhost:8001/example_workflows/doubao_seedream4_t2i_workflow.json`
  - `http://localhost:8001/example_workflows/doubao_seedream4_i2i_workflow.json`
  - `http://localhost:8001/example_workflows/doubao_seedream4_multi_fusion_workflow.json`
  - `http://localhost:8001/example_workflows/doubao_seedream4_stream_workflow.json`
  - `http://localhost:8001/docs/seedream4-sizing.md`

## 版本与兼容性
- Seedream 4.0 支持预设与像素两种尺寸方式；旧版像素工作流仍可运行。
- 节点内部统一处理返回的 `b64_json` 或 `url`，并提供占位图以降低下游报错概率。

## 反馈与改进
- 欢迎提交问题与需求；如需新增尺寸预设或更多示例工作流，可在 `issues` 中提出。

## 通过 ComfyUI 管理器安装
- 在 ComfyUI 插件管理器中选择“通过 URL 安装”，填入仓库地址：`https://github.com/allen-Jmc/comfyui-doubao.git`。
- 若希望在管理器内可搜索到：需要到该管理器的索引仓库提交 PR，将本仓库加入索引列表（不同管理器索引仓库与文件位置不同）。

## 许可证
- 本项目使用 `MIT` 许可证。详见仓库根目录 `LICENSE`。

## 快速安装（另一种方式）
- 将仓库克隆到 ComfyUI 的 `custom_nodes` 目录：
  - `cd ~/ComfyUI/custom_nodes && git clone https://github.com/allen-Jmc/comfyui-doubao.git`
  - `cd comfyui-doubao && pip install -r requirements.txt`
- 重启 ComfyUI，在节点面板搜索 `Doubao`，并导入 `example_workflows/*.json` 体验。