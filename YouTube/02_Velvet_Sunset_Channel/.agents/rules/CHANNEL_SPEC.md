---
trigger: always_on
---

# 【Ch 2: Velvet Sunset Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 2: Velvet Sunset Audio (@Velvet-Sunset-Audio)** のチャンネル固有ルール、サムネイルデザイン規格、およびビジュアルガイドラインを集約した仕様書である。

---

## 1. チャンネル概要

* **チャンネル名**: `Velvet Sunset Audio`
* **ハンドル**: `@Velvet-Sunset-Audio`
* **テーマ**: **Sunset Pop & R&B** (Charlie Puth / Justin Bieber 風 / 色気ボーカル)
* **ターゲット時間帯**: 夕方〜夜 17:00 - 22:00 (仕事終わりのチルアウト・ドライブ)
* **トークンファイル**: `YouTube/shared/credentials/token_phonkforge.json` (`account_key: phonk`)

---

## 2. 🎨 サムネイル ＆ ビジュアルデザイン規格 (`02_thumbnail_gen.py`)

* **コンセプト**: 「夕暮れの都市交差点 × 鏡面・透明道路の違和感」
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: 極細バー ＋ **サンセットオレンジ発光**
* **サムネイルフォント規格**:
  * **フォント**: `/System/Library/Fonts/Supplemental/SignPainter.ttc` (`index=0`, HouseScript)
  * **メインタイトル**: `260px` / `#FFFFFF`
  * **サブタイトル**: **【サブタイトル完全排除】**
  * **エフェクト**: Sunset Orange Glow (`255, 140, 50`) ＋ 濃い黒影
  * **配置**: **画面中央ジャスト**

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/02_Velvet_Sunset_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/02_Velvet_Sunset_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/02_Velvet_Sunset_Channel/templates/prompts.md`
