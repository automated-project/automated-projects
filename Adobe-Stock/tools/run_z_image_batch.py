#!/usr/bin/env python3
"""
Z-Image Turbo 3ジャンル連続生成 & 自動アップスケールスクリプト
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
UPSCALE_SCRIPT = os.path.join(BASE_DIR, "tools", "upscale_all.sh")

tasks = [
    {
        "name": "z_image_concrete_shadow",
        "prompt": "Subtle textured cool grey raw concrete wall surface backdrop. Dramatic cinematic lighting, shadows of monstera leaves and window blinds casting sharp soft-edge shadow play across the wall. Raytraced ambient occlusion, ample clean empty copy space on the right, fixed framing, 8k aesthetic. No text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space."
    },
    {
        "name": "z_image_smoke_slate",
        "prompt": "Macro shot, shallow depth of field. Pure volumetric white smoke and delicate vapor swirling slowly against a dark muted slate texture background. Strong directional rim lighting and volumetric light rays cutting through mist, deep soft shadows, ambient occlusion. Ample empty copy space on the left side, clean negative space. Static composition, no text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space. 8k resolution, cinematic commercial stock photo."
    },
    {
        "name": "z_image_silicone_emerald",
        "prompt": "Macro shot, shallow depth of field, blurred background. Smooth organic curved abstract soft body made of translucent silicone gel and frosted matte glass. Volumetric lighting, subtle internal glow, deep emerald and brass color accents. Ample empty copy space on the right, clean negative space. No text, textless, no letters, no words, no typography, blank surface only, no products, no props, completely empty space. Minimalist studio lighting, raytraced reflections, 8k resolution commercial quality."
    }
]

for idx, task in enumerate(tasks, 1):
    output_path = os.path.join(OUTPUT_DIR, f"{task['name']}.png")
    print(f"\n==========================================")
    print(f"[{idx}/3] Generating: {task['name']}")
    print(f"==========================================")
    
    cmd = [
        "mflux-generate-z-image-turbo",
        "-q", "4",
        "--steps", "8",
        "--width", "1024",
        "--height", "576",
        "--low-ram",
        "--prompt", task["prompt"],
        "--output", output_path
    ]
    
    start_t = time.time()
    res = subprocess.run(cmd)
    elapsed = time.time() - start_t
    if res.returncode == 0:
        print(f"Finished {task['name']} in {elapsed:.1f}s -> {output_path}")
    else:
        print(f"Error generating {task['name']} (code {res.returncode})")

print("\n--- Starting Automatic GPU 4x Upscaling ---")
subprocess.run(["/bin/zsh", UPSCALE_SCRIPT, OUTPUT_DIR, UPSCALED_DIR])
print("All tasks finished successfully!")
