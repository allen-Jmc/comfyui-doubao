# ComfyUI-JmcAI

多平台 AI 节点集合（目前包含火山引擎 Doubao/Seedream 4.0），支持聊天与图片生成。
后续将逐步扩展到其他平台，统一以 `JmcAI/<平台名>` 分类呈现。

## 功能一览
- Doubao Chat：文本聊天，支持可选图片输入（多模态）
- Seedream 4.0 文生图（Text-to-Image）
- Seedream 4.0 图生图（Image-to-Image）
- Seedream 4.0 多图融合（Multi Image Fusion）
- Seedream 4.0 流式输出（顺序生成多图）

分类与显示名称：
- 分类：`JmcAI/Doubao`
- 节点：
  - `Doubao Chat（火山引擎对话API）`
  - `Doubao Seedream4 文生图`
  - `Doubao Seedream4 图生图`
  - `Doubao Seedream4 多图融合`
  - `Doubao Seedream4 流式输出`

## 安装

- 通过 ComfyUI-Manager（URL 安装）：
  1. 打开 ComfyUI-Manager → `Install custom nodes`
  2. 粘贴仓库地址：`https://github.com/allen-Jmc/comfyui-jmcai`
  3. 安装完成后重启 ComfyUI

- 手动安装到 `custom_nodes`：
  - `git clone https://github.com/allen-Jmc/comfyui-jmcai <ComfyUI路径>/custom_nodes/comfyui-jmcai`
  - 或使用软链接：`ln -s /path/to/comfyui-jmcai <ComfyUI路径>/custom_nodes/comfyui-jmcai`
  - 安装依赖：`pip install -r <ComfyUI路径>/custom_nodes/comfyui-jmcai/requirements.txt`

## 使用
- 在左侧节点库或右键菜单搜索 `JmcAI`、`Doubao`、`Seedream4`（或中文关键字）。
- 每个节点最少需要输入 `api_key`。为安全起见，推荐通过环境变量或 ComfyUI 的安全管理器注入，不要硬编码。
- Seedream 4.0 尺寸说明见下文“Seedream 4.0 尺寸说明”。
- 示例工作流位于 `example_workflows/`，包含 Chat、T2I、I2I、多图融合、流式输出。

## Seedream 4.0 尺寸说明
- 选择方式：预设等级（`1K/2K/4K`）或像素尺寸（如 `2048x2048`），两者不可混用。
- 预设等级：最长边约 `1K≈1024`、`2K≈2048`、`4K≈4096`，按纵横比自适应宽高。
- 像素尺寸：固定宽高（例如 `2048x2048`、`2560x1440`、`4096x4096` 等），会规范乘号为小写 `x`。
- 参考图建议：参考图最长边不要明显超过目标等级；多图融合尽量选择纵横比相近的图片。
- 常见问题：若返回 400 或无图，检查是否混用尺寸、`api_key` 额度、参考图尺寸与格式。
- 示例工作流：仓库示例以 `2K` 或 `2048x2048 (1:1)` 为主，可在节点的 `size` 下拉中切换。

## 依赖
- `requests`
- `Pillow`
- `numpy`


## 许可证
- MIT（见 `LICENSE`）

## 版本说明
- 当前支持：火山引擎 Doubao Chat 与 Seedream 4.0 图片生成相关 API（文生图、图生图、多图融合、流式输出）。
- 后续：新增其他平台或 API 时将在此章节更新说明。