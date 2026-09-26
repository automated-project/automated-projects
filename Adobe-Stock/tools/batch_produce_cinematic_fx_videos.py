#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
【Adobe Stock 新世代 シネマティック高度演出動画量産エンジン】
用途が明確な「具体的シーン」×「6つの新・高度光学加工」
1. 雨のカフェ × リアル雨滴・ガラス水滴 (Raindrops on Glass)
2. 高級ホテルラウンジ × シネマティック光漏れ (Film Light Leaks)
3. 暖炉・キャンドル × 温かい浮遊火の粉 (Cozy Fireplace Embers)
4. ハイテクオフィス × アナモルフィック光線 (Anamorphic Cinema Streak)
5. 高級香水・ステージ × 流れるアトモスフェリックスモーク (Drift Fog)
6. クリスタルジュエリー × 虹色プリズム分光 (Prism Caustics & Shimmer)
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
from PIL import Image, ImageDraw, ImageFilter
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

# 用途が直感的に伝わる「具象シーン」×「専用エフェクト」の定義
SCENE_TARGETS = [
    {
        "id": "scene_rainy_cafe_window",
        "title": "Cozy Rainy Night Coffee Shop Window with Glowing Bokeh Lights and Raindrops",
        "category": "Lifestyle",
        "fx_type": "raindrops",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. Looking through a rain-slicked cafe window at night. Warm glowing amber indoor lighting, soft defocused bokeh city lights outside. Cozy wooden table corner in foreground. Moody cinematic photography, 8k resolution, shallow depth of field.",
        "keywords": "rainy night, rain window, coffee shop, cozy cafe, raindrops on glass, amber bokeh, warm atmosphere, lofi mood, chill background, b roll, 1080p, copy space, relaxation, peaceful ambiance, cinematic video"
    },
    {
        "id": "scene_luxury_hotel_lounge_sunset",
        "title": "Modern Luxury Hotel Lounge with Warm Golden Hour Sunset and Film Light Leaks",
        "category": "Buildings and Architecture",
        "fx_type": "light_leak",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. High-end modern luxury hotel lounge interior. Floor-to-ceiling windows with breathtaking warm golden sunset light streaming across polished wood floors and designer furniture. Architectural photography, 8k, serene elegance.",
        "keywords": "luxury hotel, hotel lounge, sunset light, golden hour, light leak, modern interior, real estate commercial, high end living, warm sunlight, b roll, 1080p, copy space, peaceful morning, architectural elegance"
    },
    {
        "id": "scene_cozy_fireplace_living",
        "title": "Cozy Dark Wood Living Room Fireplace with Warm Glowing Embers Floating Upward",
        "category": "Lifestyle",
        "fx_type": "cozy_embers",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A rustic modern stone fireplace in a cozy dark wood cabin living room, burning firewood with glowing yellow-orange flames and hot embers, atmospheric warm illumination, moody cinematic, 8k, shallow focus.",
        "keywords": "fireplace, cozy cabin, fire embers, burning wood, winter mood, warm lighting, campfire sparks, relaxation background, b roll, 1080p, copy space, hearth, holiday comfort, peaceful home"
    },
    {
        "id": "scene_modern_tech_office_night",
        "title": "Futuristic Corporate Glass Office at Night with Horizontal Anamorphic Blue Flare",
        "category": "Technology",
        "fx_type": "anamorphic",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A sleek corporate high-rise tech office interior at night, minimalist glass partitions overlooking glowing blue city skyline lights, pristine reflection on dark polished floor. 8k, cinematic sci-fi corporate.",
        "keywords": "corporate office, tech enterprise, night skyline, anamorphic flare, glass reflections, blue lighting, modern workplace, business presentation, future tech, b roll, 1080p, copy space, professional commercial"
    },
    {
        "id": "scene_luxury_perfume_smoke_stage",
        "title": "Luxury Perfume Bottle on Black Marble Stage with Subtle Cinematic Drifting Fog",
        "category": "Lifestyle",
        "fx_type": "drift_fog",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A luxury glass perfume bottle standing on a polished black marble stage, dramatic rim lighting casting elegant highlights, dark moody studio background, premium commercial product photography, 8k.",
        "keywords": "perfume bottle, product stage, black marble, atmospheric fog, luxury cosmetics, dramatic lighting, drifting smoke, premium display, b roll, 1080p, copy space, fragrance commercial, elegant presentation"
    },
    {
        "id": "scene_crystal_jewelry_prism_rainbow",
        "title": "Luxury Diamond Crystal Jewelry on White Silk with Shimmering Prism Rainbow Caustics",
        "category": "Lifestyle",
        "fx_type": "prism_rainbow",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. Exquisite sparkling diamond crystal facets resting on draped pure white silk, radiant pure light casting subtle prismatic rainbow spectrum caustics, clean high-key commercial jewelry photography, 8k.",
        "keywords": "diamond crystal, luxury jewelry, prism caustics, rainbow spectrum, white silk, sparkling facets, bridal luxury, elegant shimmer, beauty commercial, b roll, 1080p, copy space, high end display"
    }
]

def load_pipeline():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🚀 SSD-1B モデルをロード中... (デバイス: {device.upper()})")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    pipe.to(device)
    pipe.vae.enable_tiling()
    pipe.vae.enable_slicing()
    print("✅ モデルロード完了！ (VAE タイリング/スライシング有効)\n")
    return pipe

def render_cinematic_fx_video(raw_img_path: Path, output_video_path: Path, target_info: dict):
    src_img = Image.open(raw_img_path).convert("RGB")
    fps = 24
    duration_sec = 10
    total_frames = fps * duration_sec
    target_w, target_h = 1920, 1080
    
    base_frame = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    fx_type = target_info["fx_type"]
    
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

    random.seed(target_info.get("seed", 101))
    
    # -------------------------------------------------------------
    # 各エフェクト固有のパラメータ準備
    # -------------------------------------------------------------
    if fx_type == "raindrops":
        # 雨粒の初期配置 (滴る水滴と固定の水滴)
        drops = []
        for _ in range(75):
            drops.append({
                "x": random.uniform(20, target_w - 20),
                "y": random.uniform(0, target_h),
                "r": random.uniform(2.5, 6.0),
                "speed": random.uniform(0.4, 2.2),
                "tail": random.uniform(4, 18),
                "alpha": random.uniform(140, 220)
            })
            
    elif fx_type == "cozy_embers":
        # 暖炉の火の粉 (揺らぎながら上昇)
        embers = []
        for _ in range(50):
            embers.append({
                "x": random.uniform(target_w * 0.2, target_w * 0.8),
                "y": random.uniform(target_h * 0.4, target_h),
                "vx": random.uniform(-0.4, 0.4),
                "vy": random.uniform(-1.2, -0.4),
                "r": random.uniform(1.8, 4.2),
                "phase": random.uniform(0, 6.28),
                "color": random.choice([(255, 180, 50), (255, 120, 20), (255, 220, 100)])
            })

    for i in range(total_frames):
        t = i / (total_frames - 1)
        frame = base_frame.copy()
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # ---------------------------------------------------------
        # 1. 雨滴・ガラス水滴 (Raindrops on Glass)
        # ---------------------------------------------------------
        if fx_type == "raindrops":
            # 雨で少し湿った大気のソフトブラー・呼吸
            amb_glow = int(12 + 6 * math.sin(t * math.pi * 2.0))
            draw.rectangle([(0, 0), (target_w, target_h)], fill=(20, 30, 45, amb_glow))
            
            for d in drops:
                d["y"] = (d["y"] + d["speed"]) % target_h
                x, y, r = d["x"], d["y"], d["r"]
                a = int(d["alpha"])
                # 水滴の頭 (ハイライト)
                draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(240, 245, 255, a), outline=(100, 120, 150, a // 2))
                # 滴るしっぽ (トレイル)
                draw.line([(x, y - d["tail"]), (x, y)], fill=(200, 220, 240, a // 3), width=max(1, int(r * 0.6)))
                # 小さな光の反射点
                draw.ellipse([(x - r*0.4, y - r*0.4), (x, y)], fill=(255, 255, 255, min(255, a + 40)))

        # ---------------------------------------------------------
        # 2. シネマティック光漏れ (Film Light Leaks)
        # ---------------------------------------------------------
        elif fx_type == "light_leak":
            # 画面右上と左下から、温かいオレンジ・ゴールドのフレアがゆっくり出入り
            leak_pulse = 0.5 + 0.5 * math.sin(t * math.pi * 1.8)
            leak_alpha = int(45 * leak_pulse)
            
            # 右上からのウォームサンバースト
            leak_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            l_draw = ImageDraw.Draw(leak_layer)
            l_draw.ellipse([(target_w - 600, -300), (target_w + 300, 600)], fill=(255, 170, 70, leak_alpha))
            l_draw.ellipse([(target_w - 400, -150), (target_w + 150, 400)], fill=(255, 220, 130, leak_alpha + 15))
            # 左下のソフトアンバーフィル
            l_draw.ellipse([(-200, target_h - 400), (400, target_h + 200)], fill=(255, 140, 60, int(leak_alpha * 0.7)))
            overlay = Image.alpha_composite(overlay, leak_layer)

        # ---------------------------------------------------------
        # 3. 暖炉の火の粉 (Cozy Fireplace Embers)
        # ---------------------------------------------------------
        elif fx_type == "cozy_embers":
            # 暖炉の炎の照り返し (部屋全体が呼吸するように赤く揺らめく)
            fire_flicker = 0.06 + 0.03 * (math.sin(i * 0.25) + 0.5 * math.sin(i * 0.43))
            fire_glow = Image.new("RGB", (target_w, target_h), (int(255 * fire_flicker), int(120 * fire_flicker), int(20 * fire_flicker)))
            frame = Image.blend(frame, fire_glow, 0.10)
            
            for em in embers:
                em["x"] += em["vx"] + 0.3 * math.sin(i * 0.15 + em["phase"])
                em["y"] += em["vy"]
                if em["y"] < target_h * 0.2:
                    em["y"] = target_h * 0.95
                    em["x"] = random.uniform(target_w * 0.2, target_w * 0.8)
                
                # パルス発光
                fl = 0.7 + 0.3 * math.sin(i * 0.2 + em["phase"])
                c = em["color"]
                a = int(240 * fl)
                r = em["r"]
                draw.ellipse([(em["x"] - r, em["y"] - r), (em["x"] + r, em["y"] + r)], fill=c + (a,))
                draw.ellipse([(em["x"] - r*0.5, em["y"] - r*0.5), (em["x"] + r*0.5, em["y"] + r*0.5)], fill=(255, 255, 230, a))

        # ---------------------------------------------------------
        # 4. アナモルフィック・シネマ光線 (Anamorphic Streak)
        # ---------------------------------------------------------
        elif fx_type == "anamorphic":
            # 光源から真横に走る極細のシアン・ブルー光線
            sweep_pos = 0.5 + 0.3 * math.sin(t * math.pi * 2.0)
            center_y = int(target_h * sweep_pos)
            
            streak_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            st_draw = ImageDraw.Draw(streak_layer)
            # コアの極細ビーム
            st_draw.line([(0, center_y), (target_w, center_y)], fill=(0, 220, 255, 140), width=2)
            # 上下の淡いシネマティックグロー
            for dy in range(-12, 13):
                ga = int(45 * math.exp(-(dy**2) / 30.0))
                st_draw.line([(0, center_y + dy), (target_w, center_y + dy)], fill=(50, 150, 255, ga), width=1)
            overlay = Image.alpha_composite(overlay, streak_layer)

        # ---------------------------------------------------------
        # 5. アトモスフェリック・フォグ (Atmospheric Drift Smoke)
        # ---------------------------------------------------------
        elif fx_type == "drift_fog":
            # 床面を這うようにゆっくりと右へ流れる濃密な霧
            fog_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            f_draw = ImageDraw.Draw(fog_layer)
            fog_shift = int(t * 220)
            
            for fx in range(-300 + fog_shift, target_w + 300, 220):
                wave_y = int(target_h * 0.72 + 35 * math.sin(t * 3.0 + fx * 0.02))
                f_draw.ellipse([(fx - 180, wave_y - 80), (fx + 180, wave_y + 120)], fill=(220, 225, 240, 20))
                f_draw.ellipse([(fx - 120, wave_y - 50), (fx + 120, wave_y + 80)], fill=(240, 245, 255, 15))
            overlay = Image.alpha_composite(overlay, fog_layer)

        # ---------------------------------------------------------
        # 6. 虹色プリズム分光 (Prism Caustics & Shimmer)
        # ---------------------------------------------------------
        elif fx_type == "prism_rainbow":
            # プリズムによる虹色スペクトルが斜めに揺らめく
            prism_shift = 40 * math.sin(t * math.pi * 2.5)
            colors = [
                (255, 60, 60, 25),    # 赤
                (255, 180, 50, 25),   # 橙
                (255, 255, 60, 25),   # 黄
                (60, 230, 100, 25),   # 緑
                (50, 180, 255, 25),   # 青
                (180, 70, 255, 25)    # 紫
            ]
            p_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            pr_draw = ImageDraw.Draw(p_layer)
            
            for idx, col in enumerate(colors):
                offset_x = int(target_w * 0.55 + idx * 18 + prism_shift)
                pr_draw.polygon([
                    (offset_x, 0), (offset_x + 14, 0),
                    (offset_x - 300, target_h), (offset_x - 314, target_h)
                ], fill=col)
            overlay = Image.alpha_composite(overlay, p_layer)
            draw = ImageDraw.Draw(overlay)
            
            # ダイヤのキラリとした瞬き (スターシマー)
            spark = math.sin(i * 0.28)
            if spark > 0.5:
                sa = int(255 * (spark - 0.5) / 0.5)
                cx, cy = int(target_w * 0.65), int(target_h * 0.52)
                draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 255, 255, sa), width=2)
                draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 255, 255, sa), width=2)

        # 合成してFFmpegへパイプ出力
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
    print(f"🎬 【用途直結×6大新エフェクト】Adobe Stock 動画量産バッチ ({TODAY_STR})")
    print(f"シーン数: {len(SCENE_TARGETS)} 本 | 出力先: {VIDEOS_DIR}")
    print("==========================================================\n")
    
    pipe = load_pipeline()
    negative_prompt = "blurry, low quality, distorted, crooked, text, watermark, signature, cartoon, anime, plastic 3d render, oversaturated, lowres"

    for idx, item in enumerate(SCENE_TARGETS, 1):
        item_id = item["id"]
        title = item["title"]
        raw_img_path = RAW_DIR / f"{item_id}_raw.png"
        video_name = f"{item_id}_1080p.mp4"
        video_path = VIDEOS_DIR / video_name
        
        print(f"\n----------------------------------------------------------")
        print(f"[{idx}/{len(SCENE_TARGETS)}] 【{item['category']} / FX: {item['fx_type'].upper()}】 {title}")
        print(f"----------------------------------------------------------")
        
        # 1. SSD-1B による具体的シーン原画生成 (1152x648)
        if not raw_img_path.exists():
            print("🎨 具体的シーン原画生成中 (1152x648, 20 steps, VAEタイリング)...")
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
            
        # 2. 10秒 1080p 新・高度アンビエント動画レンダリング
        print(f"⚡ 新エフェクト [{item['fx_type']}] レンダリング中 (固定アングル・H.264)...")
        t_vid = time.time()
        render_cinematic_fx_video(raw_img_path, video_path, item)
        print(f"✅ 動画出力完了: {video_path} ({time.time() - t_vid:.1f}秒)")
        
        # 3. CSVメタデータ更新
        record_csv(video_name, title, item["keywords"], item["category"])
        
        # 4. アーティファクトディレクトリへの同期
        artifact_video = ARTIFACT_DIR / video_name
        artifact_img = ARTIFACT_DIR / f"{item_id}_raw.png"
        import shutil
        shutil.copyfile(video_path, artifact_video)
        shutil.copyfile(raw_img_path, artifact_img)

        # 5. メモリ解放
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()

    print("\n==========================================================")
    print("🎉 6つの新エフェクト動画バッチがすべて完了しました！")
    print(f"📁 保存先フォルダ: {VIDEOS_DIR}")
    print(f"📝 メタデータ更新完了: {MAIN_CSV}")
    print("==========================================================")

if __name__ == "__main__":
    main()
