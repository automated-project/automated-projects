#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio) 24/7 YouTube ライブ配信起動スクリプト
- 1時間完全シームレス波ループ動画 (LIVE_STREAM_CH3_OCEAN_WAVES_1HOUR_OFFICIAL.mp4) を無限ループ配信
- YouTube RTMP サーバーへの低遅延・高安定ストリーミング
- 自動再接続・クラッシュ復旧機能完備
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

# デフォルトパス設定
VIDEO_FILE = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/LIVE_STREAM_CH3_OCEAN_WAVES_1HOUR_OFFICIAL.mp4")
RTMP_URL_BASE = "rtmp://a.rtmp.youtube.com/live2"


def start_stream(stream_key: str, loop_forever: bool = True):
    if not stream_key:
        print("[ERROR] ストリームキーが指定されていません。--key または環境変数 YOUTUBE_STREAM_KEY を設定してください。")
        sys.exit(1)
        
    if not VIDEO_FILE.exists():
        print(f"[ERROR] 配信対象の動画ファイルが見つかりません: {VIDEO_FILE}")
        sys.exit(1)
        
    rtmp_destination = f"{RTMP_URL_BASE}/{stream_key.strip()}"
    
    print("==================================================")
    print("🔴 24/7 ライブ配信を開始します (Ch 3: AuraMelody Audio)")
    print(f"🎬 配信動画: {VIDEO_FILE.name}")
    print(f"📡 配信先: {RTMP_URL_BASE}/**** (Key protected)")
    print("==================================================")
    
    # FFmpeg 配信コマンド
    # -re: リアルタイム読み込み (実時間に合わせてストリーミング)
    # -stream_loop -1: 無限ループ再生
    # -c:v copy / -c:a copy: レンダリング済み動画のためCPU負荷ほぼゼロでパケット転送
    # -flvflags no_duration_filesize: ライブストリーム最適化
    cmd = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1" if loop_forever else "0",
        "-i", str(VIDEO_FILE),
        "-c:v", "copy",
        "-c:a", "copy",
        "-f", "flv",
        "-flvflags", "no_duration_filesize",
        rtmp_destination
    ]
    
    retry_count = 0
    max_retries = 999999  # 24/7 配信のため実質無制限
    
    while retry_count < max_retries:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] FFmpeg ストリーミング プロセスを起動します...")
            process = subprocess.Popen(cmd)
            process.wait()
            
            if process.returncode != 0:
                print(f"[WARN] 配信プロセスが終了コード {process.returncode} で停止しました。5秒後に自動再接続します...")
            else:
                print("[INFO] 配信プロセスが正常終了しました。")
                if not loop_forever:
                    break
                    
            time.sleep(5)
            retry_count += 1
            
        except KeyboardInterrupt:
            print("\n[INFO] ユーザー操作によりライブ配信を停止しました。")
            if 'process' in locals() and process.poll() is None:
                process.terminate()
            break
        except Exception as e:
            print(f"[ERROR] 予期せぬエラーが発生しました: {e}")
            time.sleep(10)
            retry_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ch 3 24/7 ライブ配信ランナー")
    parser.add_argument("--key", type=str, default=os.getenv("YOUTUBE_STREAM_KEY", ""), help="YouTube Studio から取得したストリームキー")
    parser.add_argument("--no-loop", action="store_true", help="1回のみ再生して終了するテストモード")
    
    args = parser.parse_args()
    start_stream(stream_key=args.key, loop_forever=not args.no_loop)
