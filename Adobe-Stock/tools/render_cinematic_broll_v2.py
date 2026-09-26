#!/usr/bin/env python3
"""
【シネマティックBロール制作エンジン v2】
素材としてプロが実際に買いたくなる「機能的・演出的な動き」を完全再現
1. 黒ずみ完全排除: 高品質Lanczosリサンプリングで美しいグラデーションを保持
2. ラックフォーカス（Rack Focus）: 冒頭の美しいボケ（タイトル用コピースペース）から鮮明なピントへ
3. シネマティック光漏れ（Golden Sunlight Leak & Ambient Bloom）: 窓からの柔らかな光の揺らぎ
4. 超微細・優雅なシネマティックドリー移動（10秒 24fps 1080p H.264）
"""

import os
import sys
import time
import math
import subprocess
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
VIDEOS_DIR = os.path.join(BASE_DIR, "outputs_videos")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")

os.makedirs(VIDEOS_DIR, exist_ok=True)

# 入力元画像（ステップ数28の高品位原画）
INPUT_IMG_NAME = "arch_minimal_luxury_lounge_step28_1789000608.png"
INPUT_IMG_PATH = os.path.join(OUTPUTS_DIR, INPUT_IMG_NAME)

OUTPUT_VIDEO_NAME = "arch_minimal_luxury_lounge_rackfocus_cinematic_1080p.mp4"
OUTPUT_VIDEO_PATH = os.path.join(VIDEOS_DIR, OUTPUT_VIDEO_NAME)

def generate_light_leak_mask(width, height, center_x, center_y, radius, intensity=0.35):
    """
    シネマティックな光漏れ（サンフレア/アンビエントブルーム）のレイヤーを作成
    """
    # 柔らかな光球を生成
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # 多重の楕円グラデーションで自然な光芒を作る
    steps = 15
    for i in range(steps, 0, -1):
        r = radius * (i / steps)
        alpha = int(255 * (1.0 - (i / steps) ** 1.5) * intensity)
        bbox = (center_x - r, center_y - r * 0.7, center_x + r, center_y + r * 0.7)
        draw.ellipse(bbox, fill=alpha)
        
    mask = mask.filter(ImageFilter.GaussianBlur(radius=radius * 0.25))
    
    # 黄金色の温かい光（シネマティックゴールド）
    glow = Image.new("RGB", (width, height), (255, 220, 160))
    glow.putalpha(mask)
    return glow

def render_cinematic_broll():
    print("==========================================================")
    print("🎬 【シネマティックBロール制作】黒ずみ排除 × ラックフォーカス × 光漏れ")
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
    
    # 黒ずみを防ぐため、まずは高品質Lanczosで作業解像度（2560x1440）に綺麗に拡張
    work_w = 2560
    work_h = int(work_w * (orig_h / orig_w))
    base_img = src_img.resize((work_w, work_h), Image.Resampling.LANCZOS)
    print(f"✅ 高品質Lanczos補間で作業キャンバスを作成: {work_w}x{work_h} (黒ずみゼロ保証)")
    
    # 事前にラックフォーカス用の「最大ボケ画像」を生成（高速化のため）
    max_blur_img = base_img.filter(ImageFilter.GaussianBlur(radius=18))
    
    # ffmpeg パイプの立ち上げ
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
    
    # カメラワーク（極めてゆっくりとした優雅なドリーイン: 1.00 -> 1.06倍）
    start_zoom = 1.00
    end_zoom = 1.06
    
    crop_aspect = target_w / target_h
    base_crop_h = work_h
    base_crop_w = int(work_h * crop_aspect)
    
    for i in range(total_frames):
        # 進行度 (0.0 -> 1.0)
        t = i / (total_frames - 1)
        
        # 1. カメラワーク計算 (緩やかなEase-out)
        ease_t = math.sin(t * (math.pi / 2))
        zoom = start_zoom + (end_zoom - start_zoom) * ease_t
        cur_w = base_crop_w / zoom
        cur_h = base_crop_h / zoom
        
        # 微細なセンタリング移動
        cx = (work_w - cur_w) * (0.35 + 0.30 * ease_t)
        cy = (work_h - cur_h) * 0.50
        crop_box = (int(cx), int(cy), int(cx + cur_w), int(cy + cur_h))
        
        # 2. ラックフォーカス（被写界深度・ピント送り計算）
        # 最初の2.5秒(60フレーム)はボケ → 4.5秒(108フレーム)にかけて鮮明にピントが合う
        if i < 40:
            blur_blend = 1.0
        elif i < 110:
            # 滑らかにピントが合う (Cosine Ease-in-out)
            p = (i - 40) / 70.0
            blur_blend = (1.0 + math.cos(p * math.pi)) / 2.0
        else:
            blur_blend = 0.0
            
        # フレーム切り出し
        sharp_crop = base_img.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        if blur_blend > 0.01:
            blurred_crop = max_blur_img.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
            frame = Image.blend(sharp_crop, blurred_crop, blur_blend)
        else:
            frame = sharp_crop
            
        # 3. シネマティック光漏れ（窓からの太陽光の揺らぎ・フレア）
        # 光源位置（左上の窓際付近）
        flare_x = target_w * (0.20 + 0.08 * t)
        flare_y = target_h * (0.25 + 0.03 * t)
        
        # 光の呼吸（緩やかな明滅パルス）
        pulse = 0.28 + 0.12 * math.sin(t * math.pi * 1.8)
        flare_radius = int(target_w * 0.65)
        
        light_leak = generate_light_leak_mask(target_w, target_h, flare_x, flare_y, flare_radius, intensity=pulse)
        frame.paste(light_leak, (0, 0), light_leak)
        
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
        "rack focus", "defocused to focused", "modern architecture", "minimalist interior",
        "sunlight bloom", "light leak", "warm atmosphere", "luxury lounge", "concrete wall",
        "wooden louvers", "cinematic b roll", "1080p", "opening title background", "copy space",
        "peaceful", "slow motion", "real estate commercial", "contemporary design", "high end"
    ]
    title = "Cinematic Rack Focus Opening of Modern Luxury Architecture with Warm Sunlight Bloom"
    
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow([
            OUTPUT_VIDEO_NAME,
            title,
            ", ".join(keywords),
            "Buildings and Architecture",
            "",
            "Yes"
        ])
    print(f"📝 CSVメタデータを更新しました: {MAIN_CSV}")

if __name__ == "__main__":
    render_cinematic_broll()
