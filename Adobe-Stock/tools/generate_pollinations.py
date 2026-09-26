#!/usr/bin/env python3
"""
Pollinations API を用いた画像自動生成 ＆ ローカルGPU超解像スクリプト
"""

import os
import sys
import time
import urllib.parse
import urllib.request
import subprocess
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
UPSCALE_SCRIPT = os.path.join(BASE_DIR, "tools", "upscale_all.sh")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

def generate_image(prompt: str, filename_base: str, width: int = 1920, height: int = 1080):
    timestamp = int(time.time())
    seed = random.randint(1000, 9999999)
    filename = f"{filename_base}_{timestamp}.jpg"
    target_path = os.path.join(OUTPUT_DIR, filename)

    encoded_prompt = urllib.parse.quote(prompt)
    # nologo=true で透かしなし、model=flux でFLUX.1を指定
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&seed={seed}&nologo=true"

    print(f"Generating: {filename_base}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=120) as response, open(target_path, "wb") as out_file:
        out_file.write(response.read())
    
    print(f"Saved: {target_path}")
    return target_path

def main():
    prompts = [
        (
            "volumetric_smoke_slate",
            "Macro shot, shallow depth of field. Pure volumetric white smoke and delicate vapor swirling slowly against a dark muted slate texture background. Strong directional rim lighting and volumetric light rays cutting through mist, deep soft shadows, ambient occlusion. Ample empty copy space on the left side, clean negative space. Static composition, no text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space. 8k resolution, cinematic commercial stock photo."
        ),
        (
            "translucent_silicone_softbody",
            "Macro shot, shallow depth of field, blurred background. Smooth organic curved abstract soft body made of translucent silicone gel and frosted matte glass. Volumetric lighting, subtle internal glow, deep emerald and brass color accents. Ample empty copy space on the right, clean negative space. No text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space. Minimalist studio lighting, raytraced reflections, 8k resolution commercial quality."
        ),
        (
            "monstera_shadow_raw_concrete",
            "Subtle textured cool grey raw concrete wall surface backdrop. Dramatic cinematic lighting, shadows of monstera leaves and window blinds casting sharp soft-edge shadow play across the wall. Raytraced ambient occlusion, ample clean empty copy space on the right, fixed framing, 8k aesthetic. No text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space."
        )
    ]

    generated_files = []
    for name, p in prompts:
        try:
            path = generate_image(p, name)
            generated_files.append((name, path, p))
            time.sleep(2) # 礼儀正しいリクエスト間隔
        except Exception as e:
            print(f"Error generating {name}: {e}")

    print("\n--- Starting Automatic Upscaling (GPU) ---")
    subprocess.run(["/bin/zsh", UPSCALE_SCRIPT, OUTPUT_DIR, UPSCALED_DIR])
    print("All pipeline finished successfully!")

if __name__ == "__main__":
    main()
