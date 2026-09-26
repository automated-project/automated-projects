---
trigger: always_on
---

# YouTube 自動化・制作・運用 統合マスター規約 (YouTube Automation Master Rules)

本ファイルは、YouTube 3大音楽特化チャンネル体制における**音響マスタリング、モジュール構造、サムネイルデザイン、映像レンダリング、波形ビジュアル演出、概要欄・タグの管理、API自動運用の確定仕様手順および絶対禁止事項**を集約した最上位規約である。

---

## 0. 【最上位絶対原則】すべてのAI生成物はGemini・Google系AIで生成

本プロジェクトにおける**すべてのAI生成物（テキスト・タイトル・概要欄・画像・動画・音楽・効果音・コード・プロンプト等）は、GeminiおよびGoogle系AI技術（Gemini 2.0 / Imagen 3 / Lyria / Google Cloud AI等）を用いて生成・運用することを最上位の絶対原則とする。**

---

## 1. 🎵 確定音響整音 ＆ シームレスDJクロスフェード規格 (`01_audio_master.py`)

### ① 【確定原則】イコライザー（EQ）完全撤廃 & 原音尊重 (`Zero-EQ`)
* **全チャンネルEQ完全OFF**: 原音バランスを100%活かすため、EQ（低音ブーストや高音強調）は一切適用しない。
* **`loudnorm` の完全永久禁止**: 音質変化・不自然な音量ダイナミクスの揺れを防ぐため、過度なラウドネス圧縮 (`loudnorm`) は行わない（YouTube標準の自動調整に任せる）。
* **ピーク保護のみ適用**: Peak Limiter (`alimiter=limit=0.95:level=disabled`) のみを適用して音割れを防止。

### ② シームレスDJクロスフェード & 末尾処理仕様
1. **2.5秒 等エネルギーDJクロスフェード (Equal-Power Crossfade)**: 前後曲を $\cos/\sin$ カーブで2.5秒オーバーラップさせ、音圧凹みを防ぎ接続。
2. **動画末尾フェードアウトなし**: **動画全体の末尾フェードアウト (`afade`) は行わない**（音楽の自然な余韻を守る）。
3. **MP3 320kbps 最高品質保存**: 中間音声およびマスター音声は MP3 320kbps（`libmp3lame`）で高速・高音質保存する。

---

## 2. 🎬 確定映像スペック ＆ 画面左下波形演出規格 (`03_video_render.py` / `visualizer_engine.py`)

1. **画質スペック**: **`3840x2160 (4K UHD)`**, **`30 fps`**, **`9500 kbps`** (H.264 / AAC 320k)
2. **画面左下 BPM同期波形演出 (Center-Mirrored 3-Bar Visualizer)**:
   * **演出方式**: 3本の極細丸角スリムカプセルバー（幅: 8px, 隙間: 14px）が中心Y座標から上下対称に滑らかに伸び縮みする。
   * **配置位置**: **【画面左下】** (`START_X = 150`, `CENTER_Y = 2050`) に全チャンネル共通配置。
   * **テンポ同期**: 各チャンネルの平均BPM（Ch1: 68 BPM, Ch2: 102 BPM, Ch3: 128 BPM）に合わせたBPM同期ポリリズムモーション。

---

## 3. 📝 確定メタデータ ＆ 多言語展開 ＆ 固定コメント規格 (`04_youtube_upload.py` / `config.json`)

### ① 【確定規約】タイトル・サムネイル・テキストの変動・権利・重複禁止規定
1. **権利・商標・季節等の完全禁止**: 著作権・特定のアーティスト名、特定の年度、季節、および「1hour」などの変動時間をタイトル・概要欄・サムネイルに含めることを禁止する。
2. **動画タイトルの固有性・完全重複禁止**: 動画ごとに必ず固有のタイトル（ユニークな英語表現）を設定し、過去動画とタイトルが被ることを固く禁止する（少しでも異なる文字・表現にする）。
3. **サムネイルテキストの概念（コンセプト）表現規定**:
   - **チャンネル名は入力禁止**: サムネイルは固定ブランド名ではなく、動画のテーマ・イメージを簡潔に表現する短文テキスト（例: `Deep Focus`, `Sunset Drive`, `Morning Vibes`）を入れる。
   - **変動要素の完全排除**: チャプター名、曲名、動画時間（1hour等）などの変動する文字をサムネイルに記載することを禁止する。

### ② 【確定規約】多言語メタデータ展開規格
1. **基本言語 (`defaultLanguage`)**: **英語 (`en`)** に固定。
2. **多言語ローカライズ (`localizations`)**:
   - YouTube Data API の `localizations` オブジェクトにより、投稿時に **日本語 (`ja`)・韓国語 (`ko`)・スペイン語 (`es`)・ポルトガル語 (`pt`)・インドネシア語 (`id`)** の5言語タイトルおよび概要欄説明文を自動セットする。
   - **概要欄ライセンス表記の多言語化**: 各言語の概要欄説明文内においても、フリー音源ライセンス表記（`FREE MUSIC & CREATOR LICENSE`）および「自由に使用可 / 概要欄等でリンクしていただけたら嬉しい」という説明文を各対象言語へ多言語ローカライズして記載する。
   - サムネイル画像は英語表記のみ固定（他言語テキストのサムネイル混入禁止）。
   - タグ (`tags`) のみ多言語キーワード（英語 ＋ 日本語等）の併記を許可。

### ③ 💬 確定固定コメント (Pinned Comment) 自動投稿規格
* **タイムスタンプ義務化**: コメント欄最上部に英語のタイムスタンプ（`00:00 - Track Title`）を必ず記載する。
* **エンゲージメント促進ローテーション文**:
  * コメントおよびチャンネル登録を促すメッセージ（英語 ＋ 日本語の一言）を複数パターンでローテーション挿入する。
  * **言語仕様**: タイムスタンプは英語のみ、促進メッセージは英語 ＋ 日本語一言。

### ④ 📜 フリー音源ライセンス ＆ クレジット表記規定 (全チャンネル共通)
* **トーン**: 「自由に使用可 / もし概要欄等で紹介・リンクしていただけたら嬉しい」という親しみやすいトーンで全チャンネル統一（`description_template.txt` 参照）。

## 3. 📂 新モジュール構造 ＆ データ・制御の分離設計

```text
YouTube/
├── shared/
│   ├── credentials/                 # 認証トークン (token_gameverse.json 等)
│   └── scripts/
│       ├── 01_audio_master.py        # 【共通①】音源マスタリング & 2.5s DJ Crossfade (Zero-EQ / 末尾フェードなし)
│       ├── 04_youtube_upload.py     # 【共通④】YouTube Data API 非公開投稿
│       ├── visualizer_engine.py     # 【共通】画面左下 BPM同期波形描画エンジン
│       └── run_pipeline.py          # 【統括】パイプラインオーケストレーター
│
└── [01_Chill_Channel | 02_Velvet_Sunset_Channel | 03_Uplifting_Channel]/
    ├── templates/
    │   ├── config.json              # 動画タイトル、タグ、音源・画像参照パス、確定スペック
    │   ├── description_template.txt # 概要欄テンプレート・ライセンス文
    │   └── prompts.md               # Imagen 3 プロンプト集・ビジュアルガイド
    └── scripts/
        ├── 02_thumbnail_gen.py      # 【固有②】サムネイル自動生成
        └── 03_video_render.py       # 【固有③】画面左下波形組み込み 4K レンダリング
```

---

## 4. 🚀 統括スクリプト (`run_pipeline.py`) の実行手順

```bash
# 基本実行 (Ch2の全工程を実行)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --step all

# 特定ステップのみの個別実行 (--step audio / thumb / video / upload)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --step audio

# 確認実行 (実際にYouTubeアップロードを行わない dry-run モード)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --dry-run

# クラウド実行環境用 (GitHub Actions 等で libx264 エンコーダを強制)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --cloud
```

---

## 5. ⛔ 絶対禁止事項 (No-Push & Prohibition Rules)

* ❌ **【絶対禁止】リモートプッシュの自己判断実行 (`No-Push Rule`)**: 明示的な指示がない限り `git push` を自動実行しない。
* ❌ **【絶対禁止】Macローカル環境でのFFmpeg動画エンコード**: ローカルMacのCPU/GPU負荷を避けるため、動画レンダリングはクラウド（GitHub Actions）で実行する。
* ❌ **【絶対禁止】`loudnorm` フィルタおよび末尾 `afade` の使用**: 音質劣化・余韻切断を防ぐため絶対禁止。
* ❌ **【絶対禁止】波形演出の画面右下・画面中央への無断配置**: 波形配置は必ず【画面左下 (`x=150, y=2050`)】に固定する。
