---
trigger: always_on
---

# YouTube 各チャンネル制作仕様書 統合ポータル (YouTube Channel Specifications Index)

本ファイルは、YouTube 3大音楽特化チャンネルの総合インデックスです。
各チャンネル固有の詳細仕様（プロンプト集、動画化プロンプト、楽曲プロンプト等）は、**各チャンネルの `.agents/rules/` 配下の専用仕様書**に完全集約・分離されています。

---

## 📂 チャンネル別仕様書一覧（.agents/rules/ 配下）

| チャンネル名 | フォルダ | 専用仕様書（.agents/rules/ 配下） | 主な内容 |
| :--- | :--- | :--- | :--- |
| **Ch 1: Haven Chill Audio** | [`01_Chill_Channel/`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel) | [`01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md) | 【深夜・安心な部屋×窓の外の静かな違和感】深夜雨音＆静寂フェルトピアノ（65-72 BPM）、波形完全OFF、15曲変数表 |
| **Ch 2: Velvet Sunset Audio** | [`02_Velvet_Sunset_Channel/`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel) | [`02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md) | 【夕方・都市交差点×透明道路の違和感】Charlie Puth/Justin Bieber風 Sunset Pop & R&B（96-106 BPM/色気ボーカル）、20曲変数表 |
| **Ch 3: AuraMelody Audio** | [`03_Uplifting_Channel/`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel) | [`03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md) | 【朝・都市カフェテラス×波打ち際の違和感】Sunshine Pop（125-130 BPM）、爽快Pop、15曲変数表 |

---

## 🌐 YouTube 共通マスター規約

全チャンネル共通の自動化・アップロード・音声マスタリング・AI生成物ルールは、以下を参照してください。
* [`01_youtube_automation.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/01_youtube_automation.md)
  - **最上位ルール**: すべてのAI生成物はGemini・Google系で生成・運用
  - 音声マスタリング基準（`-14.0 LUFS` / `True Peak -1.5dBFS`）
  - YouTube Data API v3 自動アップロード規約
