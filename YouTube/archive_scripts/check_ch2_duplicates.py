# -*- coding: utf-8 -*-
"""
Ch 2 (Phonk / Gym EDM) の全54ファイルの重複・類似性を完全精査するスクリプト
"""
import hashlib
from pathlib import Path

raw_dir = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel/raw_audio")
files = sorted([f for f in raw_dir.glob("**/*") if f.is_file() and f.suffix.lower() == ".mp4"])

print(f"Total MP4 files found in raw_audio: {len(files)}")

hashes = {}
duplicates = []

for f in files:
    with open(f, "rb") as fp:
        content = fp.read()
        h = hashlib.sha256(content).hexdigest()
        size = len(content)
        rel_path = f.relative_to(raw_dir)
        if h in hashes:
            duplicates.append((str(rel_path), hashes[h], size))
        else:
            hashes[h] = str(rel_path)

print(f"\n=== Hash Duplicates Found ({len(duplicates)} pairs) ===")
for dup, orig, size in duplicates:
    print(f"DUPLICATE: {dup} == {orig} ({size/1024/1024:.2f} MB)")

print(f"\nUnique files count: {len(hashes)}")
