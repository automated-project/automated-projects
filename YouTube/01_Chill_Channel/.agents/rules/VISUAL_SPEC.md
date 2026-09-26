---
trigger: model_decision
---

# Ch 1: Haven Chill Audio - ビジュアル ＆ サムネイル制作仕様 (Visual Spec)

本ドキュメントは、Ch 1 (Haven Chill Audio) における画像生成プロンプトおよびサムネイルデザイン規格を定めたものである。

---

## 1. Imagen 3 ビジュアル生成プロンプト

```text
An ultra-detailed cinematic interior photography, 16:9 widescreen composition.
A cozy, warm minimalist bedroom at midnight, a safe sanctuary from the dark.
A warm wooden desk with an open notebook and an amber glowing vintage desk lamp casting a soft golden pool of light.
Beside the desk, a massive arched floor-to-ceiling glass window with soft rain droplets trickling down.
Just outside the glass, hanging impossibly close in the clear dark starry night sky, is a colossal, softly glowing crescent moon, casting ethereal silver moonlight across the warm wooden floor.
Deep comfort, tranquil solitude, no people, gender-neutral, 85mm f/1.4 lens, hyper-realistic cozy textures, 8k resolution, cinematic masterpiece --ar 16:9
```

---

## 2. サムネイル制作規格
* **物理元画像ダイレクト指定**: 動画からの切り出しは完全禁止。原画JPEGを使用。
* **フォント**: `Futura.ttc` (`index=0`, Medium)
* **文字仕様**: メイン `100px` `#FFFFFF`, Amber Glow (`255, 235, 180`)
* **配置**: 左上 (`x=100, y=100`)
