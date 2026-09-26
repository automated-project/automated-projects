---
name: phonk-shorts-production
description: Ch2 (PhonkForge Audio) のShorts動画をマスタリング済み音源・背景ローテーション・Futuraグローテキスト・重低音パルスで自動レンダリングする手順パッケージ。
---

# Phonk Shorts Production Skill

本スキルは、**Ch2（PhonkForge Audio: Gym / Drift Phonk / Heavy Bass EDM）のShorts動画**を、マスタリング済み音源の抽出から背景ローテーション、重低音連動パルス、Futuraグローテキスト合成、動画レンダリングまで一貫して実行するための専門手順パッケージです。

---

## 1. 音源分類と選定ルール (Audio Classification Standard)

プロジェクト内の音源は以下の3層構造で分類・管理されています。Shorts制作時は**必ず「マスタリング済み音源（3層目）」を使用すること**。

| ディレクトリ | 状態・役割 | Shorts制作での扱い |
| :--- | :--- | :--- |
| `02_Phonk_Channel/raw_audio/` | AI生成・未加工の生音源 | ❌ 使用禁止 |
| `02_Phonk_Channel/extracted_audio/wav/` | トラック切り出し音源（未マスタリング） | ❌ 使用禁止 |
| `02_Phonk_Channel/mastered_audio/wav/` | **【Super Crisp Mastering】適用済みマスター音源**（55Hz/110Hz重低音ブースト、濁りカット、音圧最大化） | **⭕ 必須使用** |

---

## 2. 背景ローテーション設計 (Background Ratio & Rotation)

実データに基づき、再生数が伸びやすい **「Gym / Strength / Combat（ハードワークアウト系）」を主軸（全体の85〜90%）** とし、**「Car系」はアクセントとして全体の1割（約10%）程度**に留めます。

### 背景画像アセット一覧
* **【主力】Gym / Strength / Combat 背景（85〜90% / メイン）**:
  1. `bg_power_rack.jpeg` (Gym / Power Rack / Heavy Workout)
  2. `bg_gym_shorts.jpeg` (Gym / Heavy Dumbbells / Strength)
  3. `bg_dark_combat_shorts.jpeg` (Combat / Arena / Brutal Aggressive)
  4. `bg_cyberpunk_rain_shorts.jpeg` (Cyberpunk / Heavy Training / Night)
* **【サブ】Car / Drift 背景（約10% / アクセント）**:
  5. `bg_neon_crimson_car.jpeg` (Car / Neon Crimson / Drift)
  6. `bg_tunnel_car.jpeg` (Car / Concrete Tunnel / Bass)
  7. `bg_highway_car.jpeg` (Car / Highway / Speed)

### ローテーション順序の最適パターン
- **Gym (Power Rack) ➔ Combat ➔ Gym (Dumbbell) ➔ Cyberpunk ➔ Gym ➔ Combat ➔ Gym ➔ Car (10%枠)** のように、筋トレ・ハードワークアウト系を9割配分で展開する。


---

## 3. テキスト＆ビジュアル規格 (Visual & Typography Rules)

* **解像度**: `1080 x 1920` (9:16 縦型Full HD), `30 fps`
* **フォント**: `Futura Medium` (`/System/Library/Fonts/Supplemental/Futura.ttc`, index=0) ※仕様書 `.agents/rules/01_youtube_automation.md` 準拠
* **テキストデザイン（不変性原則）**:
  - **文字枠（ピルバッジ）完全禁止**: 背景に不透明ボックスや角丸長方形を絶対に敷かない。
  - **ネオングロー直載せ**: 文字背後にぼかし発光レイヤー（クリムゾン/シアン/オレンジ）を重ね、前面にソリッドホワイト文字を描画。
  - **配置位置**: 上部安全領域（`Y=280px〜380px`）
  - **【最重要】固有名詞・変動情報の焼き込み完全禁止**:
    - 一度アップロードした動画は差し替えできないため、**チャンネル名、曲名/トラック名、価格、年号、URL等の変動要素は動画内に一切焼き込まない**。
    - 表記テキストは **不変のジャンル・感情・用途のみ**（例: `GYM MOTIVATION`, `HEAVY BASS DROP`, `DRIFT & AGGRESSIVE PHONK`, `PURE ADRENALINE` 等）に限定する。
    - 曲名やチャンネル名は、後から修正可能なYouTubeメタデータ（タイトル・概要欄）で管理する。
* **重低音連動パルス（Bass Reactive Pulse）**:
  - `40Hz〜160Hz` のキック・サブベースピークに連動して背景画像を瞬間拡大（1.00〜1.035倍）＆指数減衰（`decay=0.78`）。
  - 黒帯防止のため、6%オーバーサイズ（`1144 x 2035`）から中心クロップ。
* **波形ビジュアライザー**:
  - 48本独立丸角バー、ルミナスホワイト（角丸4px、外枠1px）。
  - 下部マージン `340px`（Shorts UI非干渉の安全領域）。

---

## 4. メタデータ設計規約 (Metadata & SEO Strategy)

### 4.1 【最重要】タイトル完全一意性 & API事前重複チェック
* **重複絶対禁止**: 全動画（長尺・Shorts問わず）においてタイトル重複を永久に禁止。タイトルはその動画固有の「顔」。
* **API事前照合**: アップロード前に YouTube Data API で既存タイトルを取得・照合し、被りがある場合は絵文字や語順等の些細な違いを付与して自動一意化（Unique Title Resolution）する。

### 4.2 タイトル黄金パターン（35〜50文字・スマホ最適化）
* **必須アピール**: `[Free BGM]` または `[Free DL]` をさり気なく挿入しフリー音源であることを訴求。
* **キーワード優先順位**:
  1. **最優先**: `Gym`, `Workout`（筋トレ・フィットネス需要）
  2. **コア価値**: `Heavy Bass` / `Bass Boosted`（破壊的重低音）
  3. **次点**: `Drift`, `Car`, `Drive`（ドライブ・スピード感）
* **タイトル例**:
  - `HEAVY BASS GYM PHONK 🔥 [Free BGM] #Shorts #gym`
  - `BRUTAL WORKOUT HEAVY BASS ⚡ [Free BGM] #Shorts #workout`
  - `DRIFT & AGGRESSIVE PHONK ⚡ [Free BGM] #Shorts #drift`

### 4.3 概要欄・固定コメント規約
* **フリー音源ライセンス案内**: クレジット表記（`PhonkForge Audio`）で商用利用・動画利用可能であることを明記。
* **1時間Mixへの誘導**: 「Related Video（関連動画）」への誘導文を設置。
* **固定コメント**: URLや数字を含めず、英語でシンプルにフリー音源と本編を案内。

---

## 5. 実行手順 (Execution Steps)

### Step 1: レンダリングキューの定義
`YouTube/02_Phonk_Channel/scripts/render_mastered_shorts_pipeline.py` 内の `SHORTS_QUEUE` に対象トラック、ドロップ開始秒、背景画像、テキスト、グロー色を定義する。

### Step 2: レンダリングの実行
```bash
/Users/base/Automated-Projects/YouTube/venv/bin/python3 /Users/base/Automated-Projects/YouTube/02_Phonk_Channel/scripts/render_mastered_shorts_pipeline.py
```

### Step 3: 成果物の確認
出力先: `YouTube/02_Phonk_Channel/output_videos/shorts/`
生成されたMP4動画の再生時間、音質、パルス同期、テキスト可読性を確認する。

> [!IMPORTANT]
> ユーザーの明示的な指示がない限り、YouTubeへのアップロードは行わず、ローカル動画の生成・確認にとどめること。
