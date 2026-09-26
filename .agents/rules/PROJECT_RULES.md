---
trigger: always_on
---

# Automated-Projects 最重要運用ルール (MASTER PROJECT RULES)

本ファイルは、本プロジェクト群（YouTube、Adobe Stock、Game-Assets販売等）における**最上位の絶対遵守ルール**である。

---

## 0. 基本方針 & 最上位原則 (Supreme Ecosystem Rules)

### 0.0 【最上位絶対原則】すべてのAI生成物はGemini・Google系AIで生成
* **Google/Gemini系への完全統一**:
  * 全てのAI生成物（画像・アートワーク・動画・楽曲・効果音・テキスト・プロンプト・メタデータ等）は、**Gemini 2.0 / Imagen 3 / Lyria / Google Cloud AI等を用いて生成・運用することを最上位の絶対原則とする**。
  * 外部他社ツール（Midjourney, Stable Diffusion, Suno, Udio等）専用の構文や前提記述は一切排除する。

### 0.1 【最上位原則】指示内容達成度の自己チェックリスト義務（改竄・誤魔化し・隠蔽の絶対禁止）
* **完了最優先による内容改竄の禁止**:
  * AI/エージェントは「完了」を最優先して結果をごまかしたり、ユーザーの指示した引数・要件・未達成項目を達成したかのように報告・誤魔化すことを**固く禁止**する。
* **【確定】成果物検証と報告の役割**:
  * 完了報告は `walkthrough.md` で結果と検証内容を簡潔に示せば十分とし、明示的な「ユーザー指示履行確認チェックリスト」アスキーテキストの記載は不要とする。

### 0.2 【最上位原則】想定外エラー発生時の勝手な代替手段捏造・引数変更の禁止
* **無断変更・捏造の禁止**:
  * 想定外のエラーや仕様不整合が発生した場合、独自に勝手な代替手段を捏造したり、ユーザーに指定された引数・変数を勝手に変更・緩和して正常終了を装うことを**固く禁止**する。
* **エラー発生時の必須プロトコル**:
  - **選択肢A**: 発生したエラーの根本原因と具体的な代替案をユーザーに提示し、承認（y/n）を得てから実行する。
  - **選択肢B**: 処理を安全に即時停止（`raise` / `sys.exit`）し、ユーザーの指示を仰ぐ。

### 0.3 【最上位原則】Markdownファイルの細分化・タスク別参照運用原則
* **認知のズレ防止**:
  * ドキュメントはタスク・コンポーネント単位で細かく分割して管理する。
  * 作業実行時、AIは該当する専用の細分化 `.md` ファイルのみを `view_file` で物理ロードし、コンテキストの希釈や勝手な自己解釈を排除して実行すること。

### 0.4 【最上位原則】全スクリプトへの自動バリデーションコード記述義務
* **引数・変数・アウトプット検証の自動化**:
  * すべての実行スクリプト（画像・動画生成、音声マスタリング、YouTube投稿等）において、ユーザーが指示した引数・変数が正しく渡されているか、および意図したアウトプット（サムネイルパス、動画時間、音声ファイル存在、解像度等）が正しく出力されたかを自動チェックするコード（事前・事後ガード）を必ず記述すること。
  * 条件を満たさない場合はごまかさず即座にエラー・例外を投げて処理を停止させること。

### 0.5 【厳格原則】ローカルGitによるテキスト・コード履歴管理 (Local-Only Git Rule)
* **ローカル履歴管理の徹底**: 仕様変更やコード修正のたびに、ローカルGit（`git commit`）で確実に変更履歴と物理差分を記録する。

### 0.6 【新アーキテクチャ原則】ドキュメント・ルールとテンプレートデータの役割分離
* **`.agents/rules/` の役割**: 「実行手順」「ツールの使い方」「絶対禁止事項（No-Push / ローカル動画エンコード禁止等）」に限定して記述する。
* **各チャンネル `templates/` の役割**: 動画タイトル、概要欄テンプレート、タグ、素材ファイルパスなどの「可変・データ要素」はすべて各チャンネル配下の `templates/config.json` および `templates/description_template.txt` に記述し、スクリプトから物理参照させる。
* **対話運用プロトコル**: `/plan` および `/grill-me` スラッシュコマンドを用いて事前に設計・引数・成果物の対話と相互承認を行い、承認された Artifact に基づいてのみスクリプトを実行すること。

### 0.7 【環境運用原則】外部API通信コマンド実行時の BypassSandbox: true 義務化
* **外部API通信時のバイパス承認プロトコル**:
  * ターミナルから外部API通信（Gemini API、Google Cloud API、外部HTTPリクエスト等）を伴うコマンドやPythonスクリプトを実行する際は、**必ず `BypassSandbox: true` を指定してコマンド実行を提案すること**。
  * `BypassSandbox: false`（標準モード）のままで外部通信を行うと、エージェントプロキシにより「not allowed by policy」エラーが発生するため、厳格に本プロトコルを遵守すること。


---

## 1. 📂 細分化ドキュメント マスターインデックス

* [`RULE_00_SUPREME_ECOSYSTEM.md`](file:///Users/base/Automated-Projects/.agents/rules/RULE_00_SUPREME_ECOSYSTEM.md): 最上位原則・ごまかし禁止・エラー報告・チェックリスト規約
* [`RULE_01_AI_OPTIMIZATION.md`](file:///Users/base/Automated-Projects/.agents/rules/RULE_01_AI_OPTIMIZATION.md): AI運用プロトコル・タグ規約・細分化参照運用
* [`RULE_02_VALIDATION_GUARD.md`](file:///Users/base/Automated-Projects/.agents/rules/RULE_02_VALIDATION_GUARD.md): 全スクリプト引数・成果物自動検証ガード規格
* [`TASK_MASTER_ROADMAP.md`](file:///Users/base/Automated-Projects/.agents/rules/TASK_MASTER_ROADMAP.md): 全体実行計画・ロードマップ

---

## 2. 各プロジェクト仕様書インデックス

### ① YouTube プロジェクト (`YouTube/.agents/rules/`)
* [`01_youtube_master_rules.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/01_youtube_master_rules.md)
* [`02_audio_mastering_spec.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/02_audio_mastering_spec.md)
* [`03_thumbnail_and_visual_spec.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/03_thumbnail_and_visual_spec.md)
* [`04_youtube_api_metadata_spec.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/04_youtube_api_metadata_spec.md)
* [`05_pre_post_validation_spec.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/05_pre_post_validation_spec.md)

### ② Adobe Stock & Game-Assets
* [`Adobe-Stock/.agents/rules/01_adobe_stock_master.md`](file:///Users/base/Automated-Projects/Adobe-Stock/.agents/rules/01_adobe_stock_master.md)
* [`Game-Assets/.agents/rules/01_game_assets_master.md`](file:///Users/base/Automated-Projects/Game-Assets/.agents/rules/01_game_assets_master.md)
