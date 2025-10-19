# Add comfyui-jmcai — JmcAI/Doubao (Volcengine) nodes

Repository: https://github.com/allen-Jmc/comfyui-jmcai
Target: https://github.com/ltdrdata/ComfyUI-Manager (custom-node-list.json)

## Summary
ComfyUI-JmcAI is a multi-platform AI nodes plugin. Currently it provides Volcengine Doubao chat and Seedream 4.0 image generation (text-to-image, image-to-image, multi image fusion, sequential output). Nodes are grouped under category `JmcAI/Doubao`.

## Entry (JSON)
```json
{
  "author": "allen-Jmc",
  "title": "ComfyUI JmcAI (Doubao/Seedream 4.0)",
  "id": "comfyui-jmcai",
  "reference": "https://github.com/allen-Jmc/comfyui-jmcai",
  "files": ["https://github.com/allen-Jmc/comfyui-jmcai"],
  "install_type": "git-clone",
  "description": "Multi-platform AI nodes. Currently Volcengine Doubao chat and Seedream 4.0 image generation."
}
```

## Validation
- Switch on "Use local DB" in ComfyUI-Manager and append the above entry locally to validate JSON is correct.
- Search keywords: `JmcAI`, `Doubao`, `Seedream`, `comfyui-jmcai`.
- After installation, restart ComfyUI and verify nodes appear under category `JmcAI/Doubao`.

## Dependencies
- requests, Pillow, numpy

## Install Instructions
- Manager URL: paste `https://github.com/allen-Jmc/comfyui-jmcai` in Install custom nodes.
- Manual: `git clone https://github.com/allen-Jmc/comfyui-jmcai <ComfyUI>/custom_nodes/comfyui-jmcai` and `pip install -r <ComfyUI>/custom_nodes/comfyui-jmcai/requirements.txt`.

## Suggested PR title
feat(index): add comfyui-jmcai (JmcAI/Doubao) custom nodes

---

# 中文版说明

## 概述
ComfyUI-JmcAI 是一个多平台 AI 节点集合，目前包含火山引擎 Doubao 的聊天节点和 Seedream 4.0 的图像生成（文生图、图生图、多图融合、顺序多图）。节点统一分类为 `JmcAI/Doubao`。

## 索引条目（JSON）
请在 ComfyUI-Manager 仓库根目录的 `custom-node-list.json` 追加以下内容：
```json
{
  "author": "allen-Jmc",
  "title": "ComfyUI JmcAI (Doubao/Seedream 4.0)",
  "id": "comfyui-jmcai",
  "reference": "https://github.com/allen-Jmc/comfyui-jmcai",
  "files": ["https://github.com/allen-Jmc/comfyui-jmcai"],
  "install_type": "git-clone",
  "description": "多平台 AI 节点。目前包含火山引擎 Doubao 聊天与 Seedream 4.0 图像生成。"
}
```

## 验证
- 在管理器界面启用 `Use local DB`，将上述 JSON 条目临时追加到本地以验证语法。
- 搜索关键字：`JmcAI`、`Doubao`、`Seedream`、`comfyui-jmcai`。
- 安装后重启 ComfyUI，确认分类为 `JmcAI/Doubao`，节点名称包含 Doubao Chat 与 Seedream4 系列。

## 依赖与安装
- 依赖：`requests`、`Pillow`、`numpy`
- URL 安装：粘贴 `https://github.com/allen-Jmc/comfyui-jmcai`
- 手动安装：`git clone` 到 `custom_nodes/comfyui-jmcai`，并执行依赖安装。

## PR 标题建议
feat(index): add comfyui-jmcai (JmcAI/Doubao) custom nodes

## 其他
- 仓库为公共可见，README 已包含功能与安装信息。
- 推荐在 GitHub repo 添加 topics：`comfyui`, `comfyui-nodes`, `comfyui-custom-nodes`, `doubao`, `seedream4`，提高检索概率。