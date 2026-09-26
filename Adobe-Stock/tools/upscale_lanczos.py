#!/usr/bin/env python3
"""
高品質Lanczos補間アップスケールスクリプト (Adobe Stock 4K基準対応)
"""

import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")

os.makedirs(UPSCALED_DIR, exist_ok=True)

# アップスケール対象（本日のZ-Image Turbo 4作品）
target_files = [
    "z_image_chrome.png",
    "z_image_concrete_shadow.png",
    "z_image_smoke_slate.png",
    "z_image_silicone_emerald.png"
]

print("Starting High-Quality Lanczos Upscaling (4096 x 2304)...")

for filename in target_files:
    src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"Skipping (not found): {filename}")
        continue
    
    base_name = os.path.splitext(filename)[0]
    dst_path = os.path.join(UPSCALED_DIR, f"{base_name}_lanczos.png")
    
    img = Image.open(src_path)
    # 4096 x 2304 に拡大（アスペクト比16:9を完全維持）
    upscaled = img.resize((4096, 2304), Image.Resampling.LANCZOS)
    upscaled.save(dst_path, format="PNG", compress_level=1)
    
    file_size_mb = os.path.getsize(dst_path) / (1024 * 1024)
    print(f"Upscaled: {filename} -> {os.path.basename(dst_path)} ({file_size_mb:.2f} MB)")

print("\nAll Lanczos upscaling completed successfully!")
