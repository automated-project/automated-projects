---
trigger: model_decision
---

# Ch 1 (Haven Chill Audio) 長尺シームレス動画 制作タスク仕様書 (Cozy Lofi Production Spec)

本ドキュメントは、**Ch 1（Haven Chill Audio）における長尺（1時間〜3時間）完全シームレス動画（Nostalgic Anime Lofi & Cozy Felt Piano）の自動ビルド手順**です。

---

## 1. 音響マスタリング＆DJクロスフェード規格

* **音源種別**: アナログLofi、フェルトピアノ（Felt Piano）、ノスタルジックアンビエント
* **マスタリング基準**:
  - ラウドネス: `-14.0 LUFS` / True Peak `-1.5dBFS`
  - トーン: 35Hzローカット、180Hzウォームブースト、3.2kHzソフトカット、8.5kHzテープサチュレーション
* **シームレス接続**:
  - 各曲末尾の無音テール（-46dB以下）自動トリミング
  - **2.5秒 等エネルギーDJクロスフェード（Equal-Power $\cos/\sin$ ブレンド・無音ギャップ完全ゼロ）**

---

## 2. 映像・ビジュアル規格 (Cozy Painterly Anime BGV)

* **解像度 & レート**: `1920x1080` (16:9 Full HD), `15 fps`, `h264 / aac`
* **ビジュアル**: 美しい絵画調アニメ背景（緑豊かな温室、雨の窓辺、木造大図書館等）
* **【動画内不変性】**: タイマーUI、曲名、チャンネル名、文字テロップ焼き込み完全ゼロ（純粋なBGV）

---

## 3. 自動ビルド実行手順

```bash
/Users/base/Automated-Projects/YouTube/venv/bin/python3 /Users/base/Automated-Projects/YouTube/01_Chill_Channel/scripts/build_lofi_1hour_video.py
```
