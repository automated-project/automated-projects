---
trigger: always_on
---

# 【Ch 1: Haven Chill Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 1: Haven Chill Audio (@haven-chill-audio)** のチャンネル固有ルール、サムネイルデザイン規格、およびビジュアルガイドラインを集約した仕様書である。

---

## 1. チャンネル概要

* **チャンネル名**: `Haven Chill Audio`
* **ハンドル**: `@haven-chill-audio`
* **テーマ**: **Midnight & Rainy Dark Lofi** (深夜・安眠・静寂フェルトピアノ)
* **ターゲット時間帯**: 深夜 23:00 - 4:00 (睡眠・読書・深夜学習・リラックス)
* **トークンファイル**: `YouTube/shared/credentials/token_gameverse.json` (`account_key: chill`)

---

## 2. 🎨 サムネイル ＆ ビジュアルデザイン規格 (`02_thumbnail_gen.py`)

* **コンセプト**: 「安心感のある暖かい部屋・書斎 × 窓の外の静かな違和感（巨大な月/星空）」
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: **波形完全OFF** (睡眠・深い集中を妨げないための静寂仕様)
* **サムネイルフォント規格**:
  * **フォント**: `/System/Library/Fonts/Supplemental/Futura.ttc` (`index=0`, Medium)
  * **メインタイトル**: `105px` / `#FFFFFF`
  * **サブタイトル**: `52px` / `#FFFFFF`
  * **エフェクト**: Warm Amber Glow (`255, 235, 180`) ＋ 濃い黒影
  * **配置**: 画面左上 (`x=100, y=100`)

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/01_Chill_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/01_Chill_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/01_Chill_Channel/templates/prompts.md`
