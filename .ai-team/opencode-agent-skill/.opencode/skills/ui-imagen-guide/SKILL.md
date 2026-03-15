---
name: ui-imagen-guide
description: Imagen 4 图片生成提示词规范，包含提示词格式、风格关键词、尺寸规格指引。UI 设计师使用。
---

# Imagen 4 图片生成指南

## 每张图片的提示词格式

```markdown
### 图片: [用途，如：Hero Banner 背景图]

**提示词（英文）：**
"[主体描述], [风格], [色调], [构图], high quality, professional design asset, no text"

**尺寸规格：** [宽x高 px]
**用途说明：** [在页面中的位置和作用]
**保存路径：** `public/images/[文件名].png`
```

## 提示词结构拆解

```
[主体] + [风格] + [色调] + [构图] + [质量关键词]

示例：
"A minimalist flat illustration of a person using a laptop,
clean modern style, soft blue and white palette,
centered composition with negative space,
high quality, professional design asset, no text"
```

## 常用风格关键词

| 风格 | 关键词 |
|------|--------|
| 扁平插图 | flat illustration, minimal, clean |
| 写实 | photorealistic, detailed, realistic lighting |
| 3D | 3D render, isometric, soft shadows |
| 渐变 | gradient, glassmorphism, vibrant |
| 线稿 | line art, outline style, monochrome |

## 常用尺寸规格

| 用途 | 尺寸 |
|------|------|
| Hero Banner | 1440×600px |
| 卡片封面 | 800×450px |
| 空状态插图 | 400×300px |
| 头像/图标 | 200×200px |
| 背景纹理 | 1920×1080px |

## 禁止行为
- ❌ 提示词里不允许包含文字内容（图片里不放文字）
- ❌ 不允许生成人脸识别相关图片
- ❌ 不允许包含品牌 Logo 或版权内容
