---
trigger: model_decision
---

# Ch 3 (AuraMelody Audio) Melodic EDM Shorts 自動アップロード計画 (TASK_EDM_SHORTS_UPLOAD)

本ドキュメントは、第3チャンネル「**AuraMelody Audio**」（Pure Uplifting Melodic EDM）におけるYouTube Shorts動画の即時アップロード実行計画書です。

---

## 1. アップロード対象アセット & 仕様

| 項目 | 設定内容 |
|---|---|
| **対象チャンネル** | **AuraMelody Audio** (`uplifting` / Ch 3) |
| **動画ファイル** | [`YouTube/03_Uplifting_Channel/output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4) |
| **動画スペック** | 1080x1920 (9:16 縦型) / 60fps / 15秒完全シームレスループ / AAC 192k |
| **ビジュアル** | 夏のプリズム光・クリスタルブルー瞳のヘッドホン美少女 ＋ ネオンシアン波形ビジュアライザー |
| **認証トークン** | [`YouTube/shared/credentials/token_auramelody.json`](file:///Users/base/Automated-Projects/YouTube/shared/credentials/token_auramelody.json) |

---

## 2. メタデータ設計 (100% Global English / 規約完全準拠)

### ① タイトル
```text
✨ SUMMER MELODIC EDM (15s Seamless Loop) #Shorts #EDM
```

### ② 概要欄 (Description)
```text
✨ Pure Uplifting Melodic EDM / Progressive House (15s Seamless Loop).

🎧 Full 1-Hour Continuous Mix available on channel:
➡️ https://youtu.be/o8ygRO9KVuQ

🎁 【FREE CREATOR LICENSE】
Stream-Safe & Content ID Free. You can freely use this track in your YouTube videos, Shorts & TikToks!
Credit: AuraMelody Audio

#Shorts #MelodicEDM #EDM #ProgressiveHouse #AviciiStyle #SummerBeats #ElectronicMusic #StudyMusic #GymMusic
```

### ③ タグ (Tags)
`Shorts, Melodic EDM, Progressive House, Uplifting EDM, Avicii Style, Kygo Style, Summer EDM, Free BGM, No Copyright Music, Gaming Music`

### ④ カテゴリ & 公開設定
* **Category ID**: `10` (Music)
* **Privacy Status**: `public` (即時公開)

---

## 3. 実行ステップ & 手順

1. **Step 1: アップロードスクリプトの整備**:
   * [`YouTube/03_Uplifting_Channel/scripts/upload_shorts_with_metadata.py`](file:///Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/scripts/upload_shorts_with_metadata.py) を最新の認証マネージャー・メタデータに更新。
2. **Step 2: YouTube APIによる自律アップロード実行**:
   * 動画IDをピンポイントで取得し、最小限の1リクエストでアップロード完了。
3. **Step 3: 結果確認 & URL提示**:
   * 公開されたShorts動画のURLおよびステータスをユーザーに提示。
