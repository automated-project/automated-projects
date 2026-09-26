# -*- coding: utf-8 -*-
"""
tracks_master.json から各チャンネルのチャプターテキスト（*_chapters.txt）を自動エクスポートするスクリプト
"""

import json
from pathlib import Path

MASTER_PATH = Path("/Users/base/Automated-Projects/YouTube/shared/metadata/tracks_master.json")
BASE_DIR = Path("/Users/base/Automated-Projects/YouTube")

OUTPUT_MAPPING = {
    ("gameverse", "vol1"): BASE_DIR / "01_Dark_Fantasy_Channel/output_videos/1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1_chapters.txt",
    ("auramelody", "vol2"): BASE_DIR / "03_Coding_Synth_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_chapters.txt"
}

def export_chapters():
    print("=== EXPORTING CHAPTERS FROM TRACKS MASTER ===")
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for (ch_key, alb_key), out_path in OUTPUT_MAPPING.items():
        out_path.parent.mkdir(parents=True, exist_ok=True)
        alb_info = data["channels"][ch_key]["albums"][alb_key]
        lines = []
        for t in alb_info["tracks"]:
            lines.append(f"{t['time']} - {t['title']}")
            
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(lines) + "\n")
            
        print(f"  ✓ Exported {len(lines)} chapters to {out_path}")
        
    print("==============================================")

if __name__ == "__main__":
    export_chapters()
