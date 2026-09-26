---
name: velvet-sunset-production
description: Ch2 (Velvet Sunset Audio) のSunset Pop & R&B長尺動画（30分〜1時間）をマスタリング済み音源・2.5秒DJクロスフェード・極細オレンジ波形・4K静止画で完全自動ビルドする手順パッケージ。
---

# Velvet Sunset Pop & R&B Production Skill

本スキルは、**Ch2（Velvet Sunset Audio: Sunset Pop & R&B / Charlie Puth & Justin Bieber Style）の長尺動画**を、マスタリング済み音源のロードから2.5秒 等エネルギーDJクロスフェード、4K非現実アート背景、極細64本サンセットオレンジ発光波形、動画レンダリングまで一貫して完全自動実行するための専門手順パッケージです。

---

## 1. 音源マスタリング＆シームレス接続規格 (Audio Standards)

1. **採用音源**:
   - `02_Velvet_Sunset_Channel/mastered_audio/wav/` 配下の【Smooth Groove R&B Mastering】適用済みマスター音源。
2. **マスタリング仕様**:
   - `60Hz +3.0dB`, `200Hz +1.5dB`, `2.5kHz +2.0dB`, `10kHz +3.5dB` ➔ `alimiter=0.95:level=disabled` 直結。
3. **2.5秒 等エネルギーDJクロスフェード**:
   - $\cos/\sin$ カーブによる等エネルギーブレンド（`CROSSFADE_SEC = 2.5`）を適用。
4. **動画尺**:
   - `1800.0秒`（30分00秒以上）。

---

## 2. 映像・ビジュアル規格 (Visual Standards)

* **解像度**: `3840 x 2160` (16:9 4K UHD), `30 fps`, `h264_videotoolbox` / `AAC 320kbps`
* **背景アセット**: 4K 静止画（日常の都市・交差点 × 透明道路の違和感 / 人物ゼロ）
* **波形ビジュアライザー**:
   - 画面下部 64本極細丸角バー ＋ サンセットオレンジ発光（`255, 140, 50`）
* **フォント**: `Futura.ttc` (`index=2`, Bold, 100px / #FFFFFF) ＋ Sunset Orange Glow

---

## 3. 自動ビルド実行手順

`master_video_pipeline.py` を使用して全自動生成：

```bash
/Users/base/Automated-Projects/YouTube/venv/bin/python3 -c "
from pathlib import Path
from YouTube.shared.scripts.master_video_pipeline import generate_channel_video

tracks = sorted(list(Path('YouTube/02_Velvet_Sunset_Channel/mastered_audio/wav').glob('*.wav')))
bg_img = Path('YouTube/02_Velvet_Sunset_Channel/cover_art/sunset_cover.jpg')
out_mp4 = Path('YouTube/02_Velvet_Sunset_Channel/output/velvet_sunset_30min.mp4')

generate_channel_video('ch2', tracks, bg_img, out_mp4)
"
```
