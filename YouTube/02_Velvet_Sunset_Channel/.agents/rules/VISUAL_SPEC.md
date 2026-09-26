---
trigger: model_decision
---

# Ch 2: Velvet Sunset Audio - ビジュアル ＆ サムネイル制作仕様 (Visual Spec)

本ドキュメントは、Ch 2 (Velvet Sunset Audio) における背景画像生成プロンプトおよび公式サムネイルのデザイン規格を定めたものである。

---

## 1. Imagen 3 ビジュアル生成プロンプト

```text
An ultra-detailed contemporary urban fine art photography, 16:9 widescreen composition.
An empty, sun-drenched city intersection surrounded by towering brownstone buildings and skyscrapers at a glowing crimson sunset.
The asphalt street surface seamlessly transitions into a flawlessly transparent glass floor, revealing a deep, sunlit underwater cityscape directly beneath the street.
Long golden hour shadows stretching across the warm pavement, traffic lights glowing amber, rich copper and violet twilight sky reflections, no people, gender-neutral, stunning perspective, crisp 85mm lens, 8k resolution, cinematic masterpiece --ar 16:9
```

---

## 2. サムネイルデザイン規格
* **フォント**: `/System/Library/Fonts/Supplemental/SignPainter.ttc` (`index=0`, HouseScript)
* **配置**: 画面中央ジャスト（超巨大 260px / サブタイトルなし）
* **カラー & エフェクト**: `#FFFFFF` ＋ Sunset Orange Glow (`255, 140, 50`) ＋ 濃い黒影
* **絶対禁止**: 動画からの切り出し画像の使用、サムネイルへのサブタイトル追加。
