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
* **デザインスタイル**: **シネマティック ＆ リュクス (Cinematic & Luxe)**
* **人物配置**: **【人物完全ゼロ】**
* **波形演出**: 極細バー ＋ **サンセットオレンジ発光**
* **サムネイルフォント規格**:
  * **メインフォント (メインアセット)**: `Bodoni 72 (Bold)` (`thumb_ch2_bodoni.jpg`)
  * **サブフォント (A/Bテスト比較用)**: `Didot (Bold)` (`thumb_ch2_didot.jpg`)
  * **文字の組み方**: ALL CAPS -> `VELVET SUNSET`
  * **カラー**: 高級オフホワイト (`#F4F4F2` / RGB: `244, 244, 242`)
  * **ドロップシャドウ**: カラー `#000000` (純黒), オフセット `x=0, y=0`, 不透明度 `50%`, ぼかし範囲 `文字高さと同等 (広範囲ソフトシャドウ)`
  * **文字サイズ・配置**: 画面中央ジャスト (文字長に応じた動的Auto-Fit: ターゲット幅 `1480px` / 画面幅の約77%)
  * **デザイン意図**: 洗練されたモダン・セリフ体（Bodoni 72）を中央配置し、品格と高級感を与えます。

---

## 3. 📂 関連ファイル参照

* **テンプレート設定**: `YouTube/02_Velvet_Sunset_Channel/templates/config.json`
* **概要欄テンプレート**: `YouTube/02_Velvet_Sunset_Channel/templates/description_template.txt`
* **Imagen 3 プロンプト集**: `YouTube/02_Velvet_Sunset_Channel/templates/prompts.md`
