#!/usr/bin/env python3
"""
Draw Things (FLUX.1) HTTP API 連携 & 自動4倍アップスケールスクリプト
"""

import os
import sys
import json
import time
import base64
import random
import urllib.request
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
UPSCALE_SCRIPT = os.path.join(BASE_DIR, "tools", "upscale_all.sh")

API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

def generate_with_drawthings(prompt: str, filename_base: str, width: int = 1024, height: int = 576, steps: int = 4):
    timestamp = int(time.time())
    seed = random.randint(1, 2147483647)
    filename = f"{filename_base}_{timestamp}.jpg"
    target_path = os.path.join(OUTPUT_DIR, filename)

    payload = {
        "prompt": prompt,
        "negative_prompt": "text, letters, words, typography, watermark, logo, blurry, noisy, low quality, products, props, watch, bottles, people, animals",
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed
    }

    print(f"==========================================")
    print(f"Sending prompt to Draw Things (FLUX.1)...")
    print(f"Filename: {filename}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"==========================================")

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    start_time = time.time()
    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))

    elapsed = time.time() - start_time
    print(f"Generation finished in {elapsed:.1f} seconds.")

    images = result.get("images", [])
    if not images:
        raise RuntimeError("No image returned from Draw Things API")

    img_data = base64.b64decode(images[0])
    with open(target_path, "wb") as f:
        f.write(img_data)

    print(f"Successfully saved to: {target_path}")

    # 4倍アップスケールを実行
    print("\n--- Starting Automatic GPU Upscaling (4x) ---")
    subprocess.run(["/bin/zsh", UPSCALE_SCRIPT, OUTPUT_DIR, UPSCALED_DIR])
    print(f"Upscaling complete! Check: {UPSCALED_DIR}")
    return target_path

if __name__ == "__main__":
    test_prompt = (
        "Macro shot, shallow depth of field. Pure volumetric white smoke and delicate vapor "
        "swirling slowly against a dark muted slate texture background. Strong directional rim lighting "
        "and volumetric light rays cutting through mist, deep soft shadows, ambient occlusion. "
        "Ample empty copy space on the left side, clean negative space. Static composition, "
        "no text, textless, no letters, no words, no typography, blank surface only, no products, "
        "no props, completely empty space. 8k resolution, cinematic commercial stock photo."
    )
    generate_with_drawthings(test_prompt, "flux_volumetric_smoke_slate")
