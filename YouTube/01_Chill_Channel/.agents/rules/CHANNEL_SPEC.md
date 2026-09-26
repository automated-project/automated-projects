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
* **デザインスタイル**: **レトロ ＆ アナログ (Retro & Analog)**
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: **波形完全OFF** (睡眠・深い集中を妨げないための静寂仕様)
* **サムネイルフォント規格**:
  * **メインフォント (メインアセット)**: `American Typewriter (Bold)` (`thumb_ch1_typewriter.jpg`)
  * **サブフォント (A/Bテスト比較用)**: `Courier New (Bold)` (`thumb_ch1_courier.jpg`)
  * **文字の組み方**: 単語の頭だけ大文字 (Title Case) -> `Haven Chill`
  * **カラー**: 高級オフホワイト (`#F4F4F2` / RGB: `244, 244, 242`)
  * **ドロップシャドウ**: カラー `#000000` (純黒), オフセット `x=0, y=0`, 不透明度 `50%`, ぼかし範囲 `文字高さと同等 (広範囲ソフトシャドウ)`
  * **文字サイズ・配置**: 画面中央ジャスト (文字長に応じた動的Auto-Fit: ターゲット幅 `1480px` / 画面幅の約77%, 上限 `260px`)
  * **デザイン意図**: タイプライター調のレトロなフォントを中央配置し、親密な個人の部屋・書斎のような空気感を作ります。

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/01_Chill_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/01_Chill_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/01_Chill_Channel/templates/prompts.md`
