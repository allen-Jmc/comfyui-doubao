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
> 仓库已重命名为 `comfyui-jmcai`，请使用新地址。

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
- Seedream 4.0 尺寸与选型说明见 `docs/seedream4-sizing.md`。
- 示例工作流位于 `example_workflows/`，包含 Chat、T2I、I2I、多图融合、流式输出。

## 依赖
- `requests`
- `Pillow`
- `numpy`

## ComfyUI-Manager 收录（可选）
若希望在管理器搜索列表中直接出现本插件，请向索引仓库提交 PR：
- 仓库：`https://github.com/ltdrdata/ComfyUI-Manager`
- 文件：在根目录 `custom-node-list.json` 增加条目，示例：
```json
{
  "author": "allen-Jmc",
  "title": "ComfyUI JmcAI (Doubao/Seedream4)",
  "id": "comfyui-jmcai",
  "reference": "https://github.com/allen-Jmc/comfyui-jmcai",
  "files": ["https://github.com/allen-Jmc/comfyui-jmcai"],
  "install_type": "git-clone",
  "description": "Multi-platform AI nodes. Currently Volcengine Doubao chat and Seedream 4.0 image generation."
}
```
提交前，在管理器对话框启用 `Use local DB` 验证 JSON 无语法错误。

## 许可证
- MIT（见 `LICENSE`）

## 变更日志
- v0.2.0：重命名为 `ComfyUI-JmcAI`，统一分类为 `JmcAI/Doubao`；优化节点显示名称以便搜索。