# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) の全音源ファイルをリストアップし、重複や類似曲名を精査するスクリプト
"""
import os
from pathlib import Path

base_dir = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")

for folder in ["raw_audio", "mastered_audio", "extracted_audio"]:
    target = base_dir / folder
    if target.exists():
        files = sorted([f for f in target.glob("**/*") if f.is_file() and f.suffix.lower() in [".mp3", ".wav", ".m4a", ".mp4"]])
        print(f"\n==========================================")
        print(f"=== Folder: {folder} (Total: {len(files)} files) ===")
        print(f"==========================================")
        for i, f in enumerate(files, 1):
            rel_path = f.relative_to(target)
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"[{i:02d}] {rel_path} ({size_mb:.2f} MB)")
