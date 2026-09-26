---
trigger: always_on
---

# YouTube 自動化・制作・運用 統合マスター規約 (YouTube Automation Master Rules)

本ファイルは、YouTube 3大音楽特化チャンネル体制における**音響マスタリング、モジュール構造、サムネイルデザイン、映像レンダリング、概要欄・タグの管理、API自動運用の手順および絶対禁止事項**を集約した最上位規約である。

---

## 0. 【最上位絶対原則】すべてのAI生成物はGemini・Google系AIで生成

本プロジェクトにおける**すべてのAI生成物（テキスト・タイトル・概要欄・画像・動画・音楽・効果音・コード・プロンプト等）は、GeminiおよびGoogle系AI技術（Gemini 2.0 / Imagen 3 / Lyria / Google Cloud AI等）を用いて生成・運用することを最上位の絶対原則とする。**

---

## 1. 📂 新モジュール構造 ＆ データ・制御の分離設計

本プロジェクトは、機能別に分解された**単機能モジュール群**と、CLI引数でそれらをコントロールする**統括スクリプト**、および可変データを保持する**各チャンネルの `templates/`** で構成される。

```text
YouTube/
├── shared/
│   ├── credentials/                 # 認証トークン (token_gameverse.json 等)
│   └── scripts/
│       ├── 01_audio_master.py        # 【共通①】音源マスタリング & 2.5s DJ Crossfade (Zero-EQ)
│       ├── 04_youtube_upload.py     # 【共通④】YouTube Data API 非公開投稿
│       └── run_pipeline.py          # 【統括】パイプラインオーケストレーター
│
└── [01_Chill_Channel | 02_Velvet_Sunset_Channel | 03_Uplifting_Channel]/
    ├── templates/
    │   ├── config.json              # 動画タイトル、タグ、音源・画像参照パス、固有設定
    │   ├── description_template.txt # 概要欄テンプレート・ライセンス文
    │   └── prompts.md               # Imagen 3 プロンプト集・ビジュアルガイド
    └── scripts/
        ├── 02_thumbnail_gen.py      # 【固有②】サムネイル自動生成
        └── 03_video_render.py       # 【固有③】4K H.264 ビデオレンダリング
```

---

## 2. 🚀 統括スクリプト (`run_pipeline.py`) の実行手順 ＆ CLI引数

全工程の実行は統括スクリプト `run_pipeline.py` に指定チャンネルの `config.json` を渡して呼び出す。

```bash
# 基本実行 (指定チャンネルの templates/config.json を読み込み、全工程を実行)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --step all

# 特定ステップのみの個別実行 (--step audio / thumb / video / upload)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --step audio

# 確認実行 (実際にYouTubeアップロードを行わない dry-run モード)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --dry-run

# クラウド実行環境用 (GitHub Actions 等で libx264 エンコーダを強制)
python YouTube/shared/scripts/run_pipeline.py --config YouTube/02_Velvet_Sunset_Channel/templates/config.json --cloud
```

---

## 3. 🎵 音響整音 & シームレスDJクロスフェード規格 (Zero-EQ Natural Audio Pipeline)

### ① 【確定原則】イコライザー（EQ）完全撤廃 & 原音尊重 (`01_audio_master.py`)
* **全チャンネルEQ完全OFF**: 原音バランスを100%活かすため、EQ（低音ブーストや高音強調）は一切適用しない。
* **`loudnorm` の完全永久禁止**: 音質変化・不自然なポンピングを防ぐため、過度なラウドネス圧縮は行わない。
* **ピーク保護のみ適用**: Peak Limiter (`alimiter=limit=0.95:level=disabled`) のみを適用。

### ② シームレスDJクロスフェード合成仕様
1. **2.5秒 等エネルギーDJクロスフェード (Equal-Power Crossfade)**: 前後曲を $\cos/\sin$ カーブで2.5秒オーバーラップさせ、音圧凹みを防ぎ接続。
2. **末尾フェードアウト**: 動画全体のラスト3秒で滑らかにフェードアウト（`afade`）。
3. **MP3 320kbps 最高品質保存**: 中間音声およびマスター音声は MP3 320kbps（`libmp3lame`）で高速・高音質保存する。

---

## 4. 📤 YouTube API 自動投稿 ＆ メタデータ規約 (`04_youtube_upload.py`)

1. **非公開（private）投稿の徹底**: レンダリング完了後の投稿は、安全確認のため必ず **「非公開（private）」** 設定で投入する。
2. **テンプレートファイルの自動置換**: 概要欄は `templates/description_template.txt` をロードし、計算されたタイムスタンプ文字列 `{chapters}` を自動挿入する。
3. **タイトルへのメタ情報記述の完全禁止**: タイトルに「商用利用OK / Commercial Use OK / 1 Hour / 30 Min」等のメタ情報や時間表記は含めない（世界観最優先）。
4. **ネイティブ検索フレーズ準拠**: 直訳や機械翻訳を避け、現地需要フレーズ（例: 韓国 `노동요`, ロシア `Музыка в машину` 等）を採用する。

---

## 5. ⛔ 絶対禁止事項 (No-Push & Prohibition Rules)

* ❌ **【絶対禁止】リモートプッシュの自己判断実行 (`No-Push Rule`)**: 明示的な指示がない限り `git push` を自動実行しない。
* ❌ **【絶対禁止】Macローカル環境でのFFmpeg動画エンコード**: ローカルMacのCPU/GPU負荷を避けるため、動画レンダリングはクラウド（GitHub Actions）で実行する。
* ❌ **【絶対禁止】コード内への秘密鍵・トークンの直接ベタ書き**: APIキーやOAuthトークンは必ず `shared/credentials/` 配下のファイルを参照または GitHub Secrets から復元する。
* ❌ **【絶対禁止】`loudnorm` フィルタの使用**: 過度な音圧圧縮を永久禁止。
