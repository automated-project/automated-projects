---
trigger: always_on
---

# YouTube 各チャンネル制作仕様書 統合ポータル (YouTube Channel Specifications Index)

本ファイルは、YouTube 3大音楽特化チャンネルの総合インデックスです。
各チャンネル固有の仕様（サムネイル規格、プロンプト、設定ファイル）は、**各チャンネルの `.agents/rules/` および `templates/`** に集約・分離されています。

---

## 📂 チャンネル別仕様書 ＆ テンプレートインデックス

| チャンネル名 | 専用仕様書（.agents/rules/） | テンプレート ＆ プロンプト（templates/） | 主な仕様・特徴 |
| :--- | :--- | :--- | :--- |
| **Ch 1: Haven Chill Audio** | [`01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md) | [`01_Chill_Channel/templates/config.json`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel/templates/config.json)<br>[`01_Chill_Channel/templates/prompts.md`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel/templates/prompts.md) | 【深夜・安心な部屋×窓の外の月/星空】<br>Midnight Lofi＆静寂フェルトピアノ、波形完全OFF、American Typewriter Bold 中央配置 |
| **Ch 2: Velvet Sunset Audio** | [`02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md) | [`02_Velvet_Sunset_Channel/templates/config.json`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/templates/config.json)<br>[`02_Velvet_Sunset_Channel/templates/prompts.md`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/templates/prompts.md) | 【夕方・都市交差点×透明道路】<br>Sunset Pop & R&B (96-106 BPM), 画面左下サンセットオレンジ極細波形, Bodoni 72 Bold 中央配置 |
| **Ch 3: AuraMelody Audio** | [`03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md) | [`03_Uplifting_Channel/templates/config.json`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/templates/config.json)<br>[`03_Uplifting_Channel/templates/prompts.md`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/templates/prompts.md) | 【朝・都市カフェテラス×波打ち際】<br>Sunshine Pop (125-130 BPM), 画面左下クリスタルシアン極細波形, Futura Bold 中央配置 |

---

## 🌐 YouTube 共通マスター規約

全チャンネル共通の統合運用ルール・モジュール構成・絶対禁止事項（No-Push等）は以下を参照してください。
* [`01_youtube_automation.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/01_youtube_automation.md)
