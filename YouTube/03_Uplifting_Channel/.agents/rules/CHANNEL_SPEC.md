---
trigger: always_on
---

# 【Ch 3: AuraMelody Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 3: AuraMelody Audio (@AuraMelody-Audio)** のチャンネル固有ルール、サムネイルデザイン規格、およびビジュアルガイドラインを集約した仕様書である。

---

## 1. チャンネル概要

* **チャンネル名**: `AuraMelody Audio`
* **ハンドル**: `@AuraMelody-Audio`
* **テーマ**: **Sunshine Feel-Good Pop** (朝の目覚め・青空・爽快Pop)
* **ターゲット時間帯**: 朝 6:00 - 12:00 (朝の準備・通勤・爽やかな目覚め)
* **トークンファイル**: `YouTube/shared/credentials/token_auramelody.json` (`account_key: auramelody`)

---

## 2. 🎨 サムネイル ＆ ビジュアルデザイン規格 (`02_thumbnail_gen.py`)

* **コンセプト**: 「朝の都市カフェテラス × 目の前に広がる波打ち際の違和感」
* **デザインスタイル**: **クリーン ＆ モダン (Clean & Modern)**
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: 極細バー ＋ **クリスタルシアン発光**
* **サムネイルフォント規格**:
  * **メインフォント**: `Avenir Next (Heavy/Bold)` または `Futura (Bold)`
  * **文字の組み方**: ALL CAPS -> `AURAMELODY`
  * **カラー**: 高級オフホワイト (`#F4F4F2` / RGB: `244, 244, 242`)
  * **ドロップシャドウ**: カラー `#000000` (純黒), オフセット `x=0, y=0`, 不透明度 `50%`, ぼかし範囲 `文字高さと同等 (広範囲ソフトシャドウ)`
  * **文字サイズ・配置**: 画面中央ジャスト (`x=(1920-w)//2, y=(1080-h)//2 - 20`), `260px` 基準 (サブタイトルなし)
  * **デザイン意図**: 直線的で無駄のないジオメトリック・サンセリフを使うことで、朝の澄んだ空気、規則正しいルーティン、前向きなエネルギーを視覚化します。

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/03_Uplifting_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/03_Uplifting_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/03_Uplifting_Channel/templates/prompts.md`
