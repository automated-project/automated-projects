---
trigger: always_on
---

# YouTube 自動化・制作・運用 統合マスター規約 (YouTube Automation Master Rules)

本ファイルは、YouTube 3大音楽特化チャンネル体制における**音響マスタリング、DJクロスフェード、サムネイルデザイン、映像レンダリング、About概要欄、公式キーワード、API運用の全ルールを集約した最上位規約**である。

---

## 0. 【最上位絶対原則】すべてのAI生成物はGemini・Google系AIで生成

本プロジェクトにおける**すべてのAI生成物（テキスト・タイトル・概要欄・画像・動画・音楽・効果音・コード・プロンプト等）は、GeminiおよびGoogle系AI技術（Gemini 2.0 / Imagen 3 / Lyria / Google Cloud AI等）を用いて生成・運用することを最上位の絶対原則とする。**
* **画像・アートワーク**: Gemini / Imagen 3 を使用（外部ツールの構文 `--ar` 等は完全排除）。
* **音楽・オーディオ**: Google DeepMind Lyria 公式ガイドラインに完全準拠。
* **テキスト・多言語翻訳**: Geminiによる自然なネイティブ需要フレーズを生成。

---

## 1. 3大音楽特化チャンネル体制 & 運用戦略

| アカウント | チャンネル名 / ID / URL | テーマ / ジャンル | メイン形式 / 特徴 | Shorts運用方針 | トークンキー |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ch 1** | **Haven Chill Audio**<br>`UC4Cjd2YmARE7rr59u1UqUbw`<br>`@haven-chill-audio` | **Midnight & Rainy Dark Lofi**<br>(深夜・安眠・静寂フェルトピアノ) | **1〜2時間長尺Lofi Mix**<br>非現実の詩的空間・静寂美 / -14 LUFS | **【Shorts完全禁止（0本）】**<br>長尺ウォッチタイム特化 | `gameverse`<br>(`chill`) |
| **Ch 2** | **Velvet Sunset Audio**<br>`UCsyFo4FtRSWLxX_53j77AFg`<br>`@Velvet-Sunset-Audio` | **Sunset Pop & R&B**<br>(Charlie Puth/Justin Bieber風 / 色気ボーカル) | **30分〜1時間長尺R&B Mix**<br>夕暮れの都市・極上グルーヴ / Smooth Groove | **【Shorts補助（週2〜3本）】**<br>サビ切り抜きで長尺へ誘導 | `phonkforge`<br>(`velvet`) |
| **Ch 3** | **AuraMelody Audio**<br>`UCldq7fhclKDAXUA1gLI0FRw`<br>`@AuraMelody-Audio` | **Sunshine Feel-Good Pop**<br>(朝の目覚め・青空・爽快Pop) | **1時間長尺Mix & 24/7ライブ**<br>朝の都市テラス×波打ち際 / 爽快Pop | **【長尺公開時の補助（週1本）】**<br>15秒ループで長尺へ誘導 | `auramelody`<br>(`uplifting`) |

---

## 2. 音響整音 & シームレスDJクロスフェード規格 (Zero-EQ Natural Audio Pipeline)

### ① 【確定原則】イコライザー（EQ）完全撤廃 & 原音尊重
* **全チャンネルEQ完全OFF**: Google Flow/Lyriaの原音バランスを100%活かすため、EQ（低音ブーストや高音強調）は一切適用しない。
* **`loudnorm` の完全永久禁止**: 音質変化・不自然なポンピングを防ぐため、過度なラウドネス圧縮は行わない。
* **ピーク保護のみ適用**: 歪み・音割れを防ぐため、ピークリミッター（`alimiter=limit=0.95:level=disabled`）のみを使用。

### ② シームレスDJクロスフェード合成仕様
1. **無音トリミングの完全廃止（自然な余白保持）**: 曲末尾・冒頭のフェードや余白を無理にカットせず、世界観と落ち着いた間をそのまま尊重する。
2. **2.5秒 等エネルギーDJクロスフェード (Equal-Power Crossfade)**: 前後曲を $\cos/\sin$ カーブで2.5秒オーバーラップさせ、音圧凹みを防ぎシームレスに接続。
3. **末尾フェードアウト**: 動画全体のラスト3秒で滑らかにフェードアウト（`afade`）。


---

## 3. 🖼️ 【全チャンネル共通】非現実・現代アート ビジュアル制作規約 (Surreal Contemporary Art Spec)

本プロジェクトの動画背景・サムネイルは、**「人物を完全排除した、日常（部屋・都市・自然）× 1点だけの美しく心地よい違和感」** に完全統一する。幾何学や特定の形状に限定せず、詩的な非日常空間を描く。

### ① 成立させる3大黄金ルール
1. **安心感の確保（部屋・足元）**: 部屋の中に雨を降らせるなど居心地を悪くする違和感は完全禁止。室内は「暖かく乾いた安全な避難所」とする。
2. **境界線の外にある美しい嘘**: 窓の外に巨大な月、透明な道路、都会のテラスに直結する波打ち際など、見慣れた日常の外側に1点だけ詩的な嘘を配置する。
3. **中性・現代アートトーン**: 日常生活感や特定の性別要素を排除し、洗練された85mmレンズによるハイエンド写真質感で描く。

### ② プロンプト生成 4層構造フォーミュラ
```text
[① アートスタイル指定] + [② 空間・場所の指定 (安心・安全)] + [③ 境界線の外にある美しい違和感 (嘘の1点)] + [④ 光学・中性指定 (No people, 85mm lens)]
```

### ③ 公式サムネイル 完全再現デザイン規格

macOS標準フォント `/System/Library/Fonts/Supplemental/Futura.ttc` を使用。

| チャンネル | フォント実体 (TTC Index) | メイン文字仕様 | サブ文字仕様 | エフェクト仕様 (Glow / Shadow) | 配置位置 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ch 1: Haven Chill** | `Futura.ttc` (`index=0`, Medium) | `105px` / `#FFFFFF` | `52px` / `#FFFFFF` | **Warm Amber Glow** (`255, 235, 180`) ＋ 黒影 | 左上 (`x=100, y=100`) |
| **Ch 2: Velvet Sunset** | `SignPainter.ttc` (`index=0`, HouseScript) | `260px` / `#FFFFFF` | **サブタイトルなし（単体）** | **Sunset Orange Glow** (`255, 140, 50`) ＋ 濃い黒影 | **画面中央ジャスト** |
| **Ch 3: AuraMelody** | `Futura.ttc` (`index=2`, Bold) | `98px` / `#FFFFFF` | `42px` / `#FFFFFF` | **Electric Cyan Glow** (`0, 229, 255`) ＋ 黒影 | 左上 (`x=100, y=100`) |

* **絶対禁止**: 文字の枠入れ（ピルバッジ・座布団プレート）、Impact等のフォント変更。

---

## 4. 映像レンダリング仕様 (Video Rendering Standards)

* **解像度**: **`3840x2160 4K UHD`（標準仕様・Lanczos展開）**
* **フレームレート**: `30 fps`
* **エンコーダ**: `h264_videotoolbox` (`-b:v 9500k`), `AAC 320kbps` (44.1kHz/48kHz)
* **ピクセルフォーマット**: `yuv420p` (`-pix_fmt yuv420p -movflags +faststart`)
* **波形演出**:
  * **Ch 1 (Haven Chill)**: 波形完全OFF（静寂美・睡眠邪魔防止）
  * **Ch 2 (Velvet Sunset)**: 極細64本バー ＋ サンセットオレンジ発光
  * **Ch 3 (AuraMelody)**: 極細64本バー ＋ クリスタルシアン発光

---

## 5. 公式チャンネル基本情報タグ（Channel Keywords）

* **Ch 1 (Haven Chill)**: `lofi, lofi hip hop, study beats, deep focus, ambient study, sleep music, haven chill, haven chill audio, relaxation music, midnight beats`
* **Ch 2 (Velvet Sunset)**: `sunset pop, modern r&b, neo soul, pop r&b, sunset groove, evening chill, velvet sunset, velvet sunset audio, smooth r&b, driving pop`
* **Ch 3 (AuraMelody)**: `uplifting pop, sunshine pop, summer vibes, energetic pop, morning music, auramelody, auramelody audio, positive energy, feel good music`

---

## 6. 概要欄 (Description) 共通ライセンスフォーマット (100% English)

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【CREATOR LICENSE & USAGE】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: [Channel Name]
   Watch: https://youtu.be/[VideoID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. API自動反映 & メタデータ規約

1. **100% API自動反映**: メタデータ更新はYouTube Data APIスクリプトで自動反映（手動テキスト提示で終わらせない）。
2. **未開設リンクの完全排除（Gumroad等）**: ストアが実際に開設されるまで、未開設のURLや案内文を概要欄・コメント・ドキュメントに一切記載しない。
3. **【全チャンネル共通】タイムスタンプは「概要欄」と「コメント欄」の両方に必ず記載**:
   - **概要欄（Description）**: `00:00 - Track Title` から始まる完全なタイムスタンプを直接記載（**YouTubeシークバーの自動チャプター区切りを有効化するために必須**）。
   - **コメント欄（Comment）**: 同様に全曲タイムスタンプ ＋ エンゲージメント質問を投稿（リスナーの利便性とコメント欄活性化）。
4. **【全チャンネル共通】タイトルへの「商用利用OK」完全禁止 & 世界観最優先**:
   - タイトルに「商用利用OK / Commercial Use OK」等のメタ情報は絶対に含めない（世界観崩壊防止）。利用規約は概要欄・固定コメントに記載。
5. **【全チャンネル共通】メタデータへのマスタリング・内部仕様記述の排除**:
   - 概要欄やタイトルに「マスタリング方式（Warm Tape / -14 LUFS / EQ等）」などの内部仕様は書かず、リスナー視点の情緒・シチュエーション・ジャンルのみ記載。
6. **【全チャンネル共通】サムネイル・タイトルの具体性（時間帯・天候・用途）**:
   - 時間帯（3 AM, Midnight, Sunset等）、天候（Rain, Foggy等）、具体的用途（Deep Sleep, Study With Me, Coding, Workout等）を明確に表現。
7. **全動画タイトル完全一意性**: 同一ch内でタイトルの完全一致・類似を排除し、テーマ・用途を明確に差別化。
8. **ネイティブ検索フレーズ準拠（直訳完全禁止）**: 機械翻訳や「耐久」という言葉の使用を完全禁止し、各言語の現地需要フレーズ（例: 韓国 `노동요`, ロシア `Музыка в машину`, ポルトガル `Música para Trabalhar` 等）を採用。
9. **季節キーワード完全排除**: 通年（Evergreen）運用の為、`summer`, `spring`, `autumn`, `fall`, `winter` や「夏」「春」「秋」「冬」を完全排除。
10. **曲名・ファイル名の完全同期 ＆ 重複時自動リネーム規約**:
    - 一意な曲名にリネームし、ファイル名（`.mp4`, `.wav`）と1対1で完全一致させる。
    - **重複解決と報告**: 曲名が被っている場合（例: `Track (1).wav` 等）は、チャンネルの世界観に合った一意のタイトルへ自動変更し、報告に記載する。変更後もそのまま動画化・アップロードを継続する。
11. **【絶対厳守】レンダリング前 自動バリデーションガード**:
    - 音源のサンプリングレート（`sr`）を必ず動的に判定・処理。
    - `1HOUR` 動画は計算総尺 60分00秒 未満、`30MIN` 動画は 30分00秒 未満の場合、レンダリング開始前に即時例外を投げて停止。不整合なレンダリングによる計算資源と時間の浪費を永久防止。
12. **【確定運用規約】Colabクラウドレンダリング ＆ 非公開（private）アップロード**:
    - レンダリングはGoogle Colab環境で実行し、Macローカルの負荷を完全排除。
    - レンダリング完了後のYouTube自動アップロードは、安全確認・最終チェックのため必ず **「非公開（private）」** 設定で投入する。
13. **言語・コメント**: デフォルト英語。日本語は `localizations` に格納。固定コメントにはタイムスタンプとエンゲージメント質問のみを記載する。


---

## 8. 実行前 必須照合チェックリスト（1対1照合義務）

コードを実行する前に、必ず本ルールに書かれている全要件を抽出し、プログラム内の実装箇所と1対1で突き合わせたチェックリストを作成・検証すること。
