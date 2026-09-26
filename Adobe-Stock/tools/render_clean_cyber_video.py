#!/usr/bin/env python3
"""
【サイバー・テック特化型 ストック動画生成エンジン v2 (固定アングル・純粋ループ仕様)】
ユーザーフィードバック反映:
- 冒頭のボケ（ラックフォーカス）を完全排除（最初から100%鮮明）
- ズームを完全排除（安定した構図を固定）
- 浮遊デジタルパーティクルとデータパルス（光の脈動）による純粋な環境モーション
- Web背景ループ・企業VPに最適なプロ仕様
"""

import os
import sys
import time
import math
import random
import subprocess
import csv
from PIL import Image, ImageFilter, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
VIDEOS_DIR = os.path.join(BASE_DIR, "outputs_videos")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")

os.makedirs(VIDEOS_DIR, exist_ok=True)

# 入力元画像（先ほど生成した高品質サイバー原画）
INPUT_IMG_NAME = "cyber_ai_neural_grid_step28_1789002363.png"
INPUT_IMG_PATH = os.path.join(OUTPUTS_DIR, INPUT_IMG_NAME)

OUTPUT_VIDEO_NAME = "cyber_ai_neural_grid_clean_ambient_1080p.mp4"
OUTPUT_VIDEO_PATH = os.path.join(VIDEOS_DIR, OUTPUT_VIDEO_NAME)

def render_clean_cyber_video():
    print("==========================================================")
    print("⚡ 【サイバー・テック動画 v2】ボケなし・ズームなし・純粋アンビエント")
    print("==========================================================")
    
    if not os.path.exists(INPUT_IMG_PATH):
        print(f"エラー: 元画像が見つかりません: {INPUT_IMG_PATH}")
        sys.exit(1)
        
    t0 = time.time()
    src_img = Image.open(INPUT_IMG_PATH).convert("RGB")
    orig_w, orig_h = src_img.size
    print(f"✅ 入力原画を読み込みました: {orig_w}x{orig_h}")
    
    # 10秒・24fps = 240フレーム
    fps = 24
    duration_sec = 10
    total_frames = fps * duration_sec
    target_w = 1920
    target_h = 1080
    
    # 高品質Lanczos補間で1080pキャンバスを直接作成（黒ずみゼロ・完全固定）
    base_frame = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    print(f"✅ 1080p完全固定キャンバスを作成: {target_w}x{target_h} (ズーム・ボケなし)")
    
    # デジタルパーティクルのシード生成（美しく浮遊する光の粒子）
    random.seed(12345)
    num_particles = 60
    particles = []
    for _ in range(num_particles):
        particles.append({
            "x": random.uniform(0, target_w),
            "y": random.uniform(0, target_h),
            "radius": random.uniform(1.8, 5.0),
            "speed_x": random.uniform(-0.3, 0.3),
            "speed_y": random.uniform(-0.6, -0.15), # ゆっくりと上方へ漂う
            "brightness": random.uniform(0.5, 0.95),
            "pulse_speed": random.uniform(0.1, 0.25),
            "phase": random.uniform(0, math.pi * 2),
            "color": random.choice([
                (0, 240, 255),    # ネオンシアン
                (80, 200, 255),   # エレクトリックブルー
                (170, 120, 255),  # サイバーパープル
                (220, 245, 255)   # 白寄りの発光コア
            ])
        })

    # ffmpeg パイプ
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{target_w}x{target_h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-crf", "16",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUTPUT_VIDEO_PATH
    ]
    
    print(f"🚀 レンダリング開始 ({total_frames}フレーム)...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    for i in range(total_frames):
        t = i / (total_frames - 1)
        
        # 1. ベースフレーム（ズームなし・ボケなし・完全シャープ）
        frame = base_frame.copy()
        
        # 2. データパルス（光の脈動・呼吸）
        # ネオングリッド全体の光が呼吸するようにゆっくりと波打つ
        pulse_intensity = 0.10 + 0.07 * math.sin(t * math.pi * 2.5)
        pulse_layer = Image.new("RGB", (target_w, target_h), (0, int(200 * pulse_intensity), int(255 * pulse_intensity)))
        frame = Image.blend(frame, pulse_layer, 0.08)
        
        # 3. 浮遊デジタルパーティクルの描画（最初から鮮明）
        particle_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(particle_layer)
        
        for p in particles:
            # 位置更新（シームレスに画面内をループ）
            p["x"] = (p["x"] + p["speed_x"]) % target_w
            p["y"] = (p["y"] + p["speed_y"]) % target_h
            
            # 自然な明滅
            flicker = p["brightness"] * (0.75 + 0.25 * math.sin(i * p["pulse_speed"] + p["phase"]))
            r = p["radius"]
            alpha = int(255 * flicker)
            c = p["color"] + (alpha,)
            
            bbox = (p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r)
            p_draw.ellipse(bbox, fill=c)
            
        frame.paste(particle_layer, (0, 0), particle_layer)
        
        # ffmpegへパイプ転送
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    
    elapsed = time.time() - t0
    print(f"\n🎉 レンダリング完了！ (所要時間: {elapsed:.1f}秒)")
    print(f"📁 出力動画: {OUTPUT_VIDEO_PATH}")
    
    # メタデータCSV登録
    record_csv()

def record_csv():
    keywords = [
        "cyber security", "artificial intelligence", "big data", "technology background",
        "digital network", "data stream", "neural network", "glowing particles", "blue neon",
        "cyan lights", "abstract tech", "cyber space", "b roll", "1080p", "copy space",
        "ambient motion", "loop background", "clean composition", "cloud computing", "corporate video"
    ]
    title = "Abstract Cyber Security Neural Network Data Grid with Floating Neon Particles"
    
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            OUTPUT_VIDEO_NAME,
            title,
            ", ".join(keywords),
            "Technology",
            "",
            "Yes"
        ])
    print(f"📝 CSVメタデータを更新しました: {MAIN_CSV}")

if __name__ == "__main__":
    render_clean_cyber_video()
