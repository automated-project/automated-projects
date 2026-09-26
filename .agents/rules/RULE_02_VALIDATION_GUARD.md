# RULE 02: 全スクリプト引数・成果物自動検証ガード規格 (Validation Guard Standards)

本ドキュメントは、全スクリプトに記述を義務付ける**事前・事後バリデーションガード（Validation Guard）のコード規格**を定めたものである。

---

## 1. 自動チェックコードの義務付け要件

すべての実行スクリプト（Pythonスクリプト等）は、処理の開始時および終了時に以下の事前・事後バリデーションを実行しなければならない。

### ① 事前チェック (Pre-Validation Guard)
* **入力ファイルの存在確認**: ユーザーまたは仕様で指定された画像（サムネイル）、音声（WAV）、設定ファイルの物理パスが実際に存在するか。
* **引数・パラメータ範囲チェック**: 動画目標尺（例: 1時間/30分/15秒）、サンプリングレート、BPM、ビットレート等の数値変数が指定された範囲を満たしているか。
* **不正・空値の即時停止**: 必須引数が欠落している、あるいは `None` や空文字列の場合は、`ValueError` または `FileNotFoundError` を発生させて即時停止する。

### ② 事後チェック (Post-Validation Guard)
* **生成物（アウトプット）の物理検証**:
  * 生成された動画（MP4）、サムネイル（JPEG）、マスタリング音声（WAV）のファイルサイズが0バイトでないか。
  * 動画の解像度（4K UHD 3840x2160 または Shorts 1080x1920）および最終再生時間（例: 1時間動画の場合 3600秒以上）が指定した変数を100%満たしているか。
* **不適合時の処置**:
  * 検証に失敗した場合、成功を装わず、明確なエラーメッセージと共に例外（`AssertionError`）を投げてスクリプトを停止する。

---

## 2. 実装コード例（共通バリデーションモジュール推奨型）

```python
import os
import sys

def validate_input_assets(image_path: str, audio_files: list, target_duration_sec: float):
    """事前検証ガード"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"[Validation Error] サムネイル画像が存在しません: {image_path}")
    
    if not audio_files:
        raise ValueError("[Validation Error] 音声ファイルリストが空です。")
        
    for af in audio_files:
        if not os.path.exists(af):
            raise FileNotFoundError(f"[Validation Error] 音声ファイルが存在しません: {af}")

def validate_output_video(output_video_path: str, min_duration_sec: float):
    """事後検証ガード"""
    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"[Validation Error] 出力動画ファイルが生成されていません: {output_video_path}")
        
    file_size = os.path.getsize(output_video_path)
    if file_size < 1000:
        raise ValueError(f"[Validation Error] 出力動画のファイルサイズが異常に小さいです ({file_size} bytes): {output_video_path}")

    # ffprobe等で尺・解像度を検証
    # （不整合がある場合は AssertionError をスロー）
```
