#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
【Adobe Stock 完全自動 日次ストック動画量産エンジン】
SSD-1B (Apple Silicon MPS) × Lanczos 1080p × アンビエントモーション × FFmpeg
・1日5〜10本ペースの幅広い売れ筋ジャンルを自動生成
・日付ごとのフォルダ（outputs_videos/YYYY-MM-DD/）へ整理格納
・ボケなし・ズームなし・固定アングル・純粋な環境モーション仕様
・Adobe Stock提出用 CSV メタデータを完全自動更新
"""

import os
import sys
import time
import math
import random
import subprocess
import csv
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler

BASE_DIR = Path("/Users/base/Automated-Projects/Adobe-Stock")
TODAY_STR = datetime.now().strftime("%Y-%m-%d")

VIDEOS_DIR = BASE_DIR / "outputs_videos" / TODAY_STR
RAW_DIR = BASE_DIR / "outputs" / TODAY_STR
MAIN_CSV = BASE_DIR / "adobe_stock_submission.csv"
ARTIFACT_DIR = Path("/Users/base/.gemini/antigravity/brain/8eb2cb2e-3be6-4d02-8825-f672dd1efde3")

VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 厳選・売れ筋6大ジャンルの定義
STOCK_TARGETS = [
    {
        "id": "tech_neural_ai_data_stream",
        "title": "Abstract AI Neural Network and Cyber Data Stream with Floating Cyan Particles",
        "category": "Technology",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A sleek futuristic artificial intelligence data grid with glowing neural pathways, deep dark navy blue background, radiant cyan and teal energy pulses. No warped lines, clean geometric perspective, raytracing. 8k, photorealistic commercial stock footage background.",
        "particle_colors": [(0, 240, 255), (60, 180, 255), (140, 100, 255), (230, 250, 255)],
        "pulse_color": (0, 180, 240),
        "keywords": "artificial intelligence, neural network, big data, cyber security, data stream, tech background, digital network, glowing particles, cyan neon, cloud computing, b roll, 1080p, copy space, abstract tech, loop video, corporate presentation, future tech"
    },
    {
        "id": "arch_luxury_marble_sunlight_atrium",
        "title": "Minimalist Luxury Architecture Hall with Warm Morning Sunlight and Ambient Dust Motes",
        "category": "Buildings and Architecture",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A modern luxury architectural interior gallery with smooth white Carrara marble columns and polished limestone floor. Warm morning natural sunlight streaming through high glass windows, casting soft geometric shadows. No distorted geometry, perfectly straight lines. 8k, architectural commercial stock photography.",
        "particle_colors": [(255, 235, 180), (255, 215, 140), (240, 240, 240), (255, 250, 220)],
        "pulse_color": (255, 200, 120),
        "keywords": "modern architecture, luxury interior, marble atrium, sunlight shadows, minimalist interior, empty space, copy space, elegant hall, real estate, high end, 3d render, warm lighting, b roll, 1080p, contemporary design, living room, corporate lobby"
    },
    {
        "id": "fintech_gold_geometric_network",
        "title": "Abstract Fintech Global Business Network with Floating Golden Data Sparks",
        "category": "Business",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. An abstract luxury corporate fintech background featuring sleek brushed brass and champagne gold geometric rings floating in a deep matte charcoal space. Subtle financial graph lines and elegant metallic textures. 8k resolution, photorealistic commercial grade.",
        "particle_colors": [(255, 200, 80), (230, 170, 50), (255, 230, 150), (255, 245, 220)],
        "pulse_color": (220, 160, 40),
        "keywords": "fintech, financial technology, global business, investment, banking, corporate background, gold geometric, luxury business, wealth management, data network, b roll, 1080p, copy space, professional presentation, stock footage, trading analysis"
    },
    {
        "id": "biotech_medical_dna_nanoparticles",
        "title": "Futuristic Clean Biotech Laboratory Background with Glowing Ice Blue Nanoparticles",
        "category": "Science",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A clean modern biotech laboratory background with translucent frosted glass structures, abstract DNA double helix silhouette in the background, pure white and soft ice blue tones. Sterile, pristine, high precision lighting. 8k, medical scientific commercial stock.",
        "particle_colors": [(100, 220, 255), (160, 240, 255), (255, 255, 255), (70, 180, 240)],
        "pulse_color": (80, 200, 255),
        "keywords": "biotechnology, medical science, healthcare background, dna helix, laboratory, pharmacy, scientific research, clean medical, ice blue, nanoparticles, b roll, 1080p, copy space, clinical presentation, modern health, genetics, medicine"
    },
    {
        "id": "eco_sustainability_green_energy",
        "title": "Modern Clean Energy and Eco Sustainability Concept with Floating Emerald Light Motes",
        "category": "Environment",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A modern minimalist sustainability concept background. Sleek white architectural curved surface with subtle translucent emerald green leaf vein patterns, natural daylight, eco-friendly futuristic environment. 8k resolution, crisp commercial stock.",
        "particle_colors": [(80, 230, 140), (40, 190, 100), (160, 255, 190), (240, 255, 240)],
        "pulse_color": (50, 200, 110),
        "keywords": "sustainability, clean energy, eco friendly, green technology, esg investment, carbon neutral, renewable energy, modern architecture, nature tech, b roll, 1080p, copy space, environmental presentation, green concept, ecology, future energy"
    },
    {
        "id": "luxury_cosmetics_water_podium",
        "title": "Minimalist Luxury Cosmetics Podium on Water Surface with Subtle Light Ripples",
        "category": "Lifestyle",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A serene minimalist cylindrical podium made of smooth warm sand-colored travertine stone, positioned on calm crystal water with subtle gentle caustics and reflections. Soft diffused studio lighting, deep elegant shadows. 8k resolution, premium luxury product display.",
        "particle_colors": [(255, 210, 180), (255, 180, 160), (255, 240, 225), (240, 220, 200)],
        "pulse_color": (230, 180, 160),
        "keywords": "cosmetic podium, product display, travertine stone, water surface, luxury packaging, spa wellness, minimalist pedestal, empty stage, beauty background, copy space, b roll, 1080p, elegant lighting, commercial stock, skincare, clean aesthetic"
    }
]

def load_ssd1b_pipeline():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🚀 [1/3] SSD-1B モデルをロード中... (デバイス: {device.upper()})")
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    pipe.to(device)
    
    # MPS メモリ不足 (OOM) を防止する VAE タイリング & スライシングを有効化
    pipe.vae.enable_tiling()
    pipe.vae.enable_slicing()
    print("✅ モデルロード完了！ (VAE タイリング & スライシング有効化済み)\n")
    return pipe

def render_ambient_video(raw_img_path: Path, output_video_path: Path, target_info: dict):
    src_img = Image.open(raw_img_path).convert("RGB")
    fps = 24
    duration_sec = 10
    total_frames = fps * duration_sec
    target_w, target_h = 1920, 1080
    
    # 完全固定の1080pベースフレーム
    base_frame = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    cat = target_info["category"]
    
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
        str(output_video_path)
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # ジャンルごとの初期化パラメータ
    random.seed(target_info.get("seed", 42))
    
    if cat == "Technology":
        # 1. サイバー: 水平スキャンライン + グリッドデジタルパルス
        scan_speed = 1.2
        nodes = [{"x": random.randint(100, target_w-100), "y": random.randint(100, target_h-100), "phase": random.uniform(0, 6.28)} for _ in range(12)]
        
    elif cat == "Buildings and Architecture":
        # 2. 建築: 太陽光の緩やかな角度移動 (Sunlight Drift) + 極小リアルダスト
        dust_particles = [{"x": random.uniform(0, target_w), "y": random.uniform(0, target_h), "vx": random.uniform(-0.1, 0.1), "vy": random.uniform(-0.15, -0.05), "size": random.uniform(1.0, 2.2), "alpha": random.uniform(60, 140)} for _ in range(45)]
        
    elif cat == "Business":
        # 3. フィンテック: 金属光沢スペキュラースイープ (Metallic Sheen) + ゴールドストリーク
        streaks = [{"y": random.randint(150, target_h-150), "len": random.randint(80, 220), "speed": random.uniform(1.5, 3.5), "x": random.randint(0, target_w)} for _ in range(6)]
        
    elif cat == "Science":
        # 4. バイオテック: 光学レンズボケオーブ (Optical Bokeh Orbs)
        orbs = [{"x": random.uniform(100, target_w-100), "y": random.uniform(100, target_h-100), "r": random.uniform(25, 75), "vx": random.uniform(-0.15, 0.15), "vy": random.uniform(-0.25, -0.08), "alpha": random.uniform(18, 45)} for _ in range(14)]
        
    elif cat == "Environment":
        # 5. エコ: 木漏れ日の柔らかな揺らめき (Sunlight Dapple & Organic Waves)
        pass
        
    elif cat == "Lifestyle":
        # 6. コスメ: 水面のコースティクス (Water Caustics) + キラリと光るスターシマー
        shimmers = [{"x": random.randint(50, target_w-50), "y": random.randint(target_h//2, target_h-50), "cycle": random.uniform(0.1, 0.3), "phase": random.uniform(0, 6.28)} for _ in range(15)]

    for i in range(total_frames):
        t = i / (total_frames - 1)
        frame = base_frame.copy()
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        if cat == "Technology":
            # --- 【Technology】サイバースキャンライン ＆ デジタルノード ---
            scan_y = int(((t * scan_speed) % 1.0) * target_h)
            for dy in range(-15, 16):
                alpha = int(90 * math.exp(-(dy**2) / 45.0))
                draw.line([(0, scan_y + dy), (target_w, scan_y + dy)], fill=(0, 240, 255, alpha))
            
            # デジタルノードの十文字パルス
            for n in nodes:
                glow = math.sin(i * 0.18 + n["phase"])
                if glow > 0.4:
                    gl_alpha = int(220 * (glow - 0.4) / 0.6)
                    nx, ny = n["x"], n["y"]
                    draw.line([(nx - 8, ny), (nx + 8, ny)], fill=(120, 220, 255, gl_alpha), width=2)
                    draw.line([(nx, ny - 8), (nx, ny + 8)], fill=(120, 220, 255, gl_alpha), width=2)
                    draw.ellipse([(nx - 2, ny - 2), (nx + 2, ny + 2)], fill=(255, 255, 255, gl_alpha))

        elif cat == "Buildings and Architecture":
            # --- 【Architecture】太陽光の角度移動 ＆ リアルな微小ダスト ---
            # 朝の斜光がゆっくりと右へスライド
            sun_shift = int(t * 140)
            sun_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(sun_layer)
            s_draw.polygon([
                (0 + sun_shift, 0), (650 + sun_shift, 0),
                (1200 + sun_shift, target_h), (500 + sun_shift, target_h)
            ], fill=(255, 230, 160, 22))
            overlay = Image.alpha_composite(overlay, sun_layer)
            draw = ImageDraw.Draw(overlay)
            
            # 微小ダスト（太陽光の中を静かに舞う）
            for d in dust_particles:
                d["x"] = (d["x"] + d["vx"]) % target_w
                d["y"] = (d["y"] + d["vy"]) % target_h
                r = d["size"]
                draw.ellipse([(d["x"] - r, d["y"] - r), (d["x"] + r, d["y"] + r)], fill=(255, 245, 220, int(d["alpha"])))

        elif cat == "Business":
            # --- 【Business / Fintech】金属光沢スペキュラースイープ ＆ ゴールドストリーク ---
            # 45度の高級感ある光沢が左から右へスーッと流れる
            sweep_x = int((t * 1.3 - 0.2) * (target_w + target_h))
            for offset in range(-25, 26):
                alpha = int(45 * math.exp(-(offset**2) / 100.0))
                p1 = (sweep_x + offset, 0)
                p2 = (sweep_x + offset - target_h, target_h)
                draw.line([p1, p2], fill=(255, 220, 130, alpha), width=2)
                
            # 細いゴールドストリーク
            for s in streaks:
                s["x"] = (s["x"] + s["speed"]) % target_w
                draw.line([(s["x"], s["y"]), (s["x"] + s["len"], s["y"])], fill=(255, 200, 80, 140), width=1)

        elif cat == "Science":
            # --- 【Science / Biotech】光学ボケオーブ (Microscope Bokeh) ---
            for o in orbs:
                o["x"] = (o["x"] + o["vx"]) % target_w
                o["y"] = (o["y"] + o["vy"]) % target_h
                r = o["r"]
                fade = 0.7 + 0.3 * math.sin(i * 0.08 + o["r"])
                cur_alpha = int(o["alpha"] * fade)
                # 内側が柔らかく光る二重オーブ
                draw.ellipse([(o["x"] - r, o["y"] - r), (o["x"] + r, o["y"] + r)], fill=(120, 210, 255, cur_alpha))
                draw.ellipse([(o["x"] - r*0.5, o["y"] - r*0.5), (o["x"] + r*0.5, o["y"] + r*0.5)], fill=(220, 245, 255, cur_alpha + 15))

        elif cat == "Environment":
            # --- 【Environment】木漏れ日の揺らめき (Dappled Sunlight & Organic Waves) ---
            # 緩やかに明滅する自然界の光
            wave_alpha = int(35 + 20 * math.sin(t * math.pi * 3.0) + 10 * math.cos(t * math.pi * 5.0))
            draw.rectangle([(0, 0), (target_w, target_h)], fill=(100, 220, 140, wave_alpha))
            # 柔らかな光斑
            for ox in range(200, target_w, 350):
                oy = 200 + int(60 * math.sin(t * 3.0 + ox))
                draw.ellipse([(ox - 120, oy - 120), (ox + 120, oy + 120)], fill=(220, 255, 200, 25))

        elif cat == "Lifestyle":
            # --- 【Lifestyle / Cosmetics】水面の光の網目 (Caustics) ＆ スターシマー ---
            # 下部（水面エリア）に緩やかなコースティクス干渉縞
            caustics_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            c_draw = ImageDraw.Draw(caustics_layer)
            for cy in range(target_h // 2, target_h, 30):
                c_alpha = int(25 + 15 * math.sin(t * 4.0 + cy * 0.05))
                c_draw.line([(0, cy), (target_w, cy + int(10 * math.sin(t * 5.0 + cy)))], fill=(255, 240, 220, c_alpha), width=3)
            overlay = Image.alpha_composite(overlay, caustics_layer)
            draw = ImageDraw.Draw(overlay)
            
            # キラリと光るスターシマー (十字の星)
            for sh in shimmers:
                spark = math.sin(i * sh["cycle"] + sh["phase"])
                if spark > 0.6:
                    s_alpha = int(255 * (spark - 0.6) / 0.4)
                    sx, sy = sh["x"], sh["y"]
                    draw.line([(sx - 6, sy), (sx + 6, sy)], fill=(255, 245, 230, s_alpha), width=2)
                    draw.line([(sx, sy - 6), (sx, sy + 6)], fill=(255, 245, 230, s_alpha), width=2)
                    draw.ellipse([(sx - 2, sy - 2), (sx + 2, sy + 2)], fill=(255, 255, 255, s_alpha))

        # フレーム合成
        frame.paste(overlay, (0, 0), overlay)
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()

def record_csv(video_filename: str, title: str, keywords: str, category: str):
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            video_filename,
            title,
            keywords,
            category,
            "",
            "Yes"
        ])

def main():
    print("==========================================================")
    print(f"🎬 Adobe Stock 日次動画量産バッチ ({TODAY_STR})")
    print(f"ジャンル数: {len(STOCK_TARGETS)} 本 | 出力先: {VIDEOS_DIR}")
    print("==========================================================\n")
    
    # 原画が不足している場合のみSSD-1Bモデルをロード
    all_raws_exist = all((RAW_DIR / f"{it['id']}_raw.png").exists() for it in STOCK_TARGETS)
    pipe = None
    if not all_raws_exist:
        pipe = load_ssd1b_pipeline()
        negative_prompt = "blurry, low quality, distorted, crooked lines, text, watermark, signature, cartoon, anime, plastic 3d render, lowres"

    for idx, item in enumerate(STOCK_TARGETS, 1):
        item_id = item["id"]
        title = item["title"]
        raw_img_path = RAW_DIR / f"{item_id}_raw.png"
        video_name = f"{item_id}_1080p.mp4"
        video_path = VIDEOS_DIR / video_name
        
        print(f"\n----------------------------------------------------------")
        print(f"[{idx}/{len(STOCK_TARGETS)}] 【{item['category']}】 {title}")
        print(f"----------------------------------------------------------")
        
        # 1. SSD-1B 原画（未生成の場合のみ生成）
        if not raw_img_path.exists():
            print("🎨 原画生成中 (1152x648, 20 steps, VAEタイリング)...")
            t_gen = time.time()
            res = pipe(
                prompt=item["prompt"],
                negative_prompt=negative_prompt,
                width=1152,
                height=648,
                num_inference_steps=20,
                guidance_scale=7.5
            )
            raw_img = res.images[0]
            raw_img.save(raw_img_path, "PNG")
            print(f"✅ 原画保存完了: {raw_img_path} ({time.time() - t_gen:.1f}秒)")
        else:
            print(f"⏩ 既存の原画を使用: {raw_img_path}")
            
        # 3. 10秒 1080p アンビエント動画レンダリング
        print("⚡ 10秒アンビエント動画レンダリング中 (固定アングル・Lanczos・H.264)...")
        t_vid = time.time()
        render_ambient_video(raw_img_path, video_path, item)
        print(f"✅ 動画出力完了: {video_path} ({time.time() - t_vid:.1f}秒)")
        
        # 4. CSVメタデータ更新
        record_csv(video_name, title, item["keywords"], item["category"])
        
        # 5. アーティファクトディレクトリへの同期 (確認用)
        artifact_video = ARTIFACT_DIR / video_name
        artifact_img = ARTIFACT_DIR / f"{item_id}_raw.png"
        import shutil
        shutil.copyfile(video_path, artifact_video)
        shutil.copyfile(raw_img_path, artifact_img)

        # 6. メモリ解放 (MPSキャッシュクリア)
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()

    print("\n==========================================================")
    print("🎉 本日分の動画量産バッチがすべて完了しました！")
    print(f"📁 保存先フォルダ: {VIDEOS_DIR}")
    print(f"📝 メタデータ更新完了: {MAIN_CSV}")
    print("==========================================================")

if __name__ == "__main__":
    main()
