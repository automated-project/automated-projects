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
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: 極細バー ＋ **クリスタルシアン発光**
* **サムネイルフォント規格**:
  * **フォント**: `/System/Library/Fonts/Supplemental/Futura.ttc` (`index=2`, Bold)
  * **メインタイトル**: `98px` / `#FFFFFF`
  * **サブタイトル**: `42px` / `#FFFFFF`
  * **エフェクト**: Electric Cyan Glow (`0, 229, 255`) ＋ 濃い黒影
  * **配置**: 画面左上 (`x=100, y=100`)

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/03_Uplifting_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/03_Uplifting_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/03_Uplifting_Channel/templates/prompts.md`
