---
trigger: model_decision
---

# Ch 3 (AuraMelody Audio) 24/7 ライブ配信タスク仕様書 (Live Stream Spec)

本ドキュメントは、**Ch 3（AuraMelody Audio: Uplifting / Melodic EDM）における24時間365日常時ライブ配信（24/7 Live Stream）の運用仕様および配信管理手順**です。

---

## 1. 配信ソース動画規格 (Source Video Spec)

* **動画パス**: `/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/LIVE_STREAM_CH3_OCEAN_WAVES_1HOUR_OFFICIAL.mp4`
* **尺**: `3689.25秒`（1時間01分29秒 完全シームレス波ループ）
* **解像度 & フレームレート**: `1920x1080` (16:9 Full HD), `24 fps`
* **ビデオコーデック**: `h264 (High Profile, yuv420p)`
* **オーディオコーデック**: `aac (192 kbps, 44.1 kHz, Stereo)`
* **平均ビットレート**: `約 8.3 Mbps`

---

## 2. ストリーミング・パイプライン規格 (FFmpeg RTMP Pipeline)

* **RTMP エンドポイント**: `rtmp://a.rtmp.youtube.com/live2`
* **ストリーミングコマンド仕様**:
  ```bash
  ffmpeg -re -stream_loop -1 -i /Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/LIVE_STREAM_CH3_OCEAN_WAVES_1HOUR_OFFICIAL.mp4 -c:v copy -c:a copy -f flv -flvflags no_duration_filesize rtmp://a.rtmp.youtube.com/live2/<STREAM_KEY>
  ```
* **超低負荷設計の原則**:
  - `-c:v copy -c:a copy` により、再エンコードを一切行わず、事前レンダリング済みH.264/AACパケットを直接RTMP転送。
  - CPU / GPU使用率はほぼ0%（常時安定稼働）。
* **クラッシュ・瞬断復旧（Auto-Reconnect）**:
  - ネットワーク瞬断やYouTube側の一時的切断を検知した場合、5秒待機後に自動再接続。

---

## 3. 起動 & 停止手順 (Operations Manual)

### ① 配信起動コマンド
```bash
/Users/base/Automated-Projects/YouTube/venv/bin/python3 /Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/scripts/start_live_stream.py --key <STREAM_KEY>
```

### ② バックグラウンド常駐（Daemon起動）
```bash
nohup /Users/base/Automated-Projects/YouTube/venv/bin/python3 /Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/scripts/start_live_stream.py --key <STREAM_KEY> > /Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/live_stream.log 2>&1 &
```

### ③ 停止コマンド
```bash
pkill -f "start_live_stream.py"
pkill -f "LIVE_STREAM_CH3_OCEAN_WAVES_1HOUR_OFFICIAL.mp4"
```
