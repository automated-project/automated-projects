---
name: cozy-lofi-production
description: Ch1 (Haven Chill Audio) のノスタルジックLofi＆温もりフェルトピアノ長尺動画（1〜2時間）をマスタリング済み音源・2.5秒DJクロスフェード・4K静止画（波形完全OFF）で完全自動ビルドする手順パッケージ。
---

# Cozy Lofi & Felt Piano Production Skill

本スキルは、**Ch1（Haven Chill Audio）における長尺（1時間〜2時間）完全シームレス動画（Midnight Lofi & Cozy Felt Piano）**を、マスタリング済み音源のロードから2.5秒 等エネルギーDJクロスフェード、4K非現実アート背景（安心な部屋×窓の外の巨大な月）、波形完全OFF、動画レンダリングまで一貫して完全自動実行するための専門手順パッケージです。

---

## 1. 音源マスタリング＆シームレス接続規格 (Audio Standards)

1. **採用音源**:
   - `01_Chill_Channel/mastered_audio/wav/` 配下の【Warm Tape Midnight Mastering】適用済みマスター音源。
2. **マスタリング仕様**:
   - `35Hz HPF`, `180Hz +1.8dB`, `8.5kHz -1.8dB`, `15kHz LPF` ➔ `alimiter=0.95:level=disabled` 直結。
3. **2.5秒 等エネルギーDJクロスフェード**:
   - $\cos/\sin$ カーブによる等エネルギーブレンド（`CROSSFADE_SEC = 2.5`）を適用。
4. **動画尺**:
   - `7200.0秒`（2時間00秒以上）。

---

## 2. 映像・ビジュアル規格 (Visual Standards)

* **解像度**: `3840 x 2160` (16:9 4K UHD), `30 fps`, `h264_videotoolbox` / `AAC 320kbps`
* **背景アセット**: 4K 静止画（安心で暖かい部屋 × 窓の外の巨大な月 / 人物完全ゼロ）
* **波形ビジュアライザー**: **完全OFF（睡眠・深い思考の邪魔をしない静寂美）**
* **フォント**: `Futura.ttc` (`index=0`, Medium, 105px / #FFFFFF) ＋ Warm Amber Glow

---

## 3. 自動ビルド実行手順

`master_video_pipeline.py` を使用して全自動生成：

```bash
/Users/base/Automated-Projects/YouTube/venv/bin/python3 -c "
from pathlib import Path
from YouTube.shared.scripts.master_video_pipeline import generate_channel_video

tracks = sorted(list(Path('YouTube/01_Chill_Channel/mastered_audio/wav').glob('*.wav')))
bg_img = Path('YouTube/01_Chill_Channel/cover_art/chill_cover.jpg')
out_mp4 = Path('YouTube/01_Chill_Channel/output/haven_chill_2hour.mp4')

generate_channel_video('ch1', tracks, bg_img, out_mp4)
"
```
