---
trigger: always_on
---

# Automated-Projects タスク・マスターロードマップ (MASTER EXECUTION ROADMAP)

本ファイルは、本プロジェクト群（YouTube 3大音楽特化チャンネル、itch.io/Gumroad販売）における**確定方針・全体実行計画**を統括するマスターロードマップである。

---

## 1. 収益化・自動化の基本方針

1. **YouTube 3大音楽チャンネルによる広告収益の最大化**:
   - ターゲット・シチュエーション・時間帯を完全分離した3チャンネルで網羅。
   - 4K高解像度静止画 × 1点の美しい違和感（非日常空間）でブランドを統一。
2. **完全自動化パイプラインの確立**:
   - `master_video_pipeline.py` を唯一の実行コアとし、音源検証・マスタリング・DJクロスフェード・4Kレンダリング・メタデータ生成を一気通貫で処理。

---

## 2. プラットフォーム別 具体的仕様 & 計画

### ① YouTube 3大チャンネル運用方針
1. **Ch 1: `chill` — Haven Chill Audio (Midnight & Rainy Dark Lofi)**:
   - **コンセプト**: 深夜の安心な部屋・書斎 × 窓の外の静かな違和感（巨大な月 / 星空）。
   - **音楽性**: 深夜雨音＆静寂フェルトピアノ（65-72 BPM）、波形完全OFF、2時間長尺。
2. **Ch 2: `phonk` — Velvet Sunset Audio (Sunset Pop & R&B)**:
   - **コンセプト**: 夕暮れの都市交差点 × 透明道路（深淵の違和感）。
   - **音楽性**: Charlie Puth / Justin Bieber 風 Sunset Pop & R&B（96-106 BPM / 色気ボーカル）、極細オレンジ波形、30分〜1時間長尺。
3. **Ch 3: `auramelody` — AuraMelody Audio (Sunshine Feel-Good Pop)**:
   - **コンセプト**: 朝の都市カフェテラス × 目の前に広がる波打ち際（爽快な違和感）。
   - **音楽性**: Sunshine Pop（125-130 BPM / ポジティブ・多幸感）、極細シアン波形、1時間長尺。

---

## 3. 仕様書マスターインデックス

* [`PROJECT_RULES.md`](file:///Users/base/Automated-Projects/.agents/rules/PROJECT_RULES.md): 最上位運用規約
* [`YouTube/.agents/rules/01_youtube_automation.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/01_youtube_automation.md): YouTube共通マスター規約
* [`YouTube/.agents/rules/02_youtube_channel_specs.md`](file:///Users/base/Automated-Projects/YouTube/.agents/rules/02_youtube_channel_specs.md): チャンネル別ポータル
* **Ch 1**: [`01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/01_Chill_Channel/.agents/rules/CHANNEL_SPEC.md)
* **Ch 2**: [`02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/.agents/rules/CHANNEL_SPEC.md)
* **Ch 3**: [`03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/.agents/rules/CHANNEL_SPEC.md)
