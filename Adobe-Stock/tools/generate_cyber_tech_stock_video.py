#!/usr/bin/env python3
"""
【サイバー・テック特化型 ストック動画生成エンジン】
企業のDX/AI/サイバーセキュリティ/Webヘッダー需要に最適化した高単価Bロール動画
1. SSD-1B（ステップ数28）によるネオンブルー＆シアンの幾何学テック空間生成
2. 黒ずみゼロの高品質Lanczos展開（美しいグローグラデーションを保持）
3. データパルス（光の脈動・スキャン波）＋ 浮遊デジタルパーティクル ＋ ラックフォーカス
4. 10秒・フルHD（1080p / 24fps）・H.264
5. Adobe StockメタデータCSV自動登録
"""

import os
import sys
import time
import math
import random
import subprocess
import csv
import torch
from PIL import Image, ImageFilter, ImageDraw
from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
VIDEOS_DIR = os.path.join(BASE_DIR, "outputs_videos")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# サイバー・テック需要特化プロンプト（3:7余白・企業VP向け）
PROMPT_DATA = {
    "id": "cyber_ai_neural_grid",
    "title": "Abstract Cyber Security and AI Neural Data Grid with Glowing Particles and Copy Space",
    "keywords": [
        "cyber security", "artificial intelligence", "big data", "technology background",
        "digital network", "data stream", "neural network", "glowing particles", "blue neon",
        "cyan lights", "abstract tech", "cyber space", "b roll", "1080p", "copy space",
        "opening title", "rack focus", "future tech", "cloud computing", "corporate video"
    ],
    "category": "Technology",
    "prompt": (
        "Asymmetrical composition, deep dark navy background, large negative copy space for text. "
        "A sophisticated abstract cyber security and AI neural network data space. "
        "Glowing cyan, electric blue and subtle violet geometric light lines forming an elegant perspective grid. "
        "Floating luminous data particles and optical fiber light trails. "
        "High-end corporate tech aesthetic, sleek 3D render, deep depth of field, sharp clean neon lines, "
        "no messy artifacts, 8k resolution, cinematic atmosphere."
    ),
    "negative_prompt": (
        "worst quality, low quality, messy blobs, chaotic oversaturation, text, watermark, "
        "grainy, distorted geometry, low resolution, blurry noise"
    )
}

def load_pipeline():
    print("🚀 [1/4] SSD-1B モデルをメモリにロードしています...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"   ↳ 実行デバイス: {device.upper()} (Apple Silicon GPU)")
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    pipe.enable_attention_slicing()
    print("✅ ロード完了（サイバー空間向けステップ数28設定）\n")
    return pipe

def render_cyber_video(image_path, output_video_path, duration_sec=10, fps=24, target_w=1920, target_h=1080):
    print(f"🎬 [3/4] サイバー・シネマティック動画をレンダリング中 ({duration_sec}秒, {fps}fps)...")
    t0 = time.time()
    
    src_img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = src_img.size
    
    # 黒ずみ完全根絶: 高品質Lanczosで作業解像度（2560x1440）に綺麗に拡張
    work_w = 2560
    work_h = int(work_w * (orig_h / orig_w))
    base_img = src_img.resize((work_w, work_h), Image.Resampling.LANCZOS)
    
    # ラックフォーカス用ボケ画像
    max_blur_img = base_img.filter(ImageFilter.GaussianBlur(radius=16))
    
    total_frames = duration_sec * fps  # 240フレーム
    
    # デジタルパーティクルのシード生成（浮遊する光の粒子）
    random.seed(42)
    num_particles = 45
    particles = []
    for _ in range(num_particles):
        particles.append({
            "x": random.uniform(0, target_w),
            "y": random.uniform(0, target_h),
            "radius": random.uniform(2.0, 5.5),
            "speed_x": random.uniform(-0.4, 0.4),
            "speed_y": random.uniform(-0.8, -0.2), # 上方へゆっくり漂う
            "brightness": random.uniform(0.4, 0.9),
            "color": random.choice([(0, 240, 255), (120, 180, 255), (180, 120, 255)])
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
        output_video_path
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    start_zoom = 1.00
    end_zoom = 1.07
    crop_aspect = target_w / target_h
    base_crop_h = work_h
    base_crop_w = int(work_h * crop_aspect)
    
    for i in range(total_frames):
        t = i / (total_frames - 1)
        ease_t = math.sin(t * (math.pi / 2))
        
        # 1. カメラドリーイン
        zoom = start_zoom + (end_zoom - start_zoom) * ease_t
        cur_w = base_crop_w / zoom
        cur_h = base_crop_h / zoom
        
        cx = (work_w - cur_w) * (0.20 + 0.60 * ease_t)
        cy = (work_h - cur_h) * 0.50
        crop_box = (int(cx), int(cy), int(cx + cur_w), int(cy + cur_h))
        
        # 2. ラックフォーカス (0〜2.5秒はボケ → 4.5秒で鮮明)
        if i < 40:
            blur_blend = 1.0
        elif i < 110:
            p = (i - 40) / 70.0
            blur_blend = (1.0 + math.cos(p * math.pi)) / 2.0
        else:
            blur_blend = 0.0
            
        sharp_crop = base_img.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
        if blur_blend > 0.01:
            blurred_crop = max_blur_img.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
            frame = Image.blend(sharp_crop, blurred_crop, blur_blend)
        else:
            frame = sharp_crop
            
        # 3. データパルス（光の脈動・スキャン波）
        # シアンの光波が呼吸するように画面を優しく包む
        pulse_intensity = 0.12 + 0.08 * math.sin(t * math.pi * 3.0)
        pulse_layer = Image.new("RGB", (target_w, target_h), (0, int(210 * pulse_intensity), int(255 * pulse_intensity)))
        frame = Image.blend(frame, pulse_layer, 0.10)
        
        # 4. 浮遊デジタルパーティクルの描画（ピントが合った後に鮮明に見える）
        if blur_blend < 0.8:
            particle_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            p_draw = ImageDraw.Draw(particle_layer)
            p_visibility = (1.0 - blur_blend)
            
            for p in particles:
                # 移動
                p["x"] = (p["x"] + p["speed_x"]) % target_w
                p["y"] = (p["y"] + p["speed_y"]) % target_h
                
                # 微細な明滅
                flicker = p["brightness"] * (0.8 + 0.2 * math.sin(i * 0.2 + p["radius"])) * p_visibility
                r = p["radius"]
                alpha = int(255 * flicker)
                c = p["color"] + (alpha,)
                
                bbox = (p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r)
                p_draw.ellipse(bbox, fill=c)
                
            frame.paste(particle_layer, (0, 0), particle_layer)
            
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print(f"✅ サイバー動画生成完了 ({time.time() - t0:.1f}秒): {os.path.basename(output_video_path)}\n")

def record_csv(video_name, pdata):
    print("📝 [4/4] Adobe Stock提出用CSVにメタデータを登録中...")
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            video_name,
            pdata["title"],
            ", ".join(pdata["keywords"]),
            pdata["category"],
            "",
            "Yes"
        ])
    print(f"✅ メタデータ登録完了: {MAIN_CSV}\n")

def main():
    print("==========================================================")
    print("⚡ 【ブルーオーシャン戦略】サイバー・テック特化 Bロール動画")
    print("==========================================================")
    
    pipe = load_pipeline()
    timestamp = int(time.time())
    fid = PROMPT_DATA["id"]
    
    raw_img_name = f"{fid}_step28_{timestamp}.png"
    final_video_name = f"{fid}_cinematic_1080p_{timestamp}.mp4"
    
    raw_img_path = os.path.join(OUTPUTS_DIR, raw_img_name)
    final_video_path = os.path.join(VIDEOS_DIR, final_video_name)
    
    # 1. 画像生成（ステップ数28、ネオンの直線と粒子を高密度生成）
    print(f"🎨 サイバー空間生成中 (ステップ数: 28, 解像度: 1024x576)...")
    t0 = time.time()
    result = pipe(
        prompt=PROMPT_DATA["prompt"],
        negative_prompt=PROMPT_DATA["negative_prompt"],
        num_inference_steps=28,
        guidance_scale=7.5,
        width=1024,
        height=576,
        generator=torch.Generator("cpu").manual_seed(98765)
    ).images[0]
    
    result.save(raw_img_path)
    print(f"✅ 原画生成完了 ({time.time() - t0:.1f}秒): {raw_img_name}\n")
    
    del pipe
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
        
    # 2. シネマティック動画レンダリング（データパルス・浮遊粒子・ラックフォーカス）
    render_cyber_video(raw_img_path, final_video_path, duration_sec=10, fps=24)
    
    # 3. CSV登録
    record_csv(final_video_name, PROMPT_DATA)
    
    print("==========================================================")
    print("🎉 サイバー・テック特化動画が完成しました！")
    print(f"・完成動画: {final_video_path}")
    print("==========================================================")

if __name__ == "__main__":
    main()
