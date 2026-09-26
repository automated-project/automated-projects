#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Tropical Beach Sunshine Pop 4K Mix ビルダー
- 定数・変数を分離したマスター共通パイプライン (YouTube/shared/scripts/master_video_pipeline.py) を使用
- 尺: 21曲フル尺 (過剰カットなし / 約61分)
- 背景動画: cover_art/Tropical_ocean_waves_rolling_ashore_20260923124532.mp4
- 波形: 白色・48本丸角波形ビジュアライザー
"""

import os
import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.master_video_pipeline import build_video_pipeline

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_DIR = BASE_DIR / "mastered_audio/wav"
BG_VIDEO = BASE_DIR / "cover_art/Tropical_ocean_waves_rolling_ashore_20260923124532.mp4"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "1HOUR_TROPICAL_SUNSHINE_POP_MIX_4K.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "1HOUR_TROPICAL_SUNSHINE_POP_MIX_4K_chapters.txt"

# 21曲のトラックリスト
TRACK_LIST = [
    "Dancing_Into_Day.wav",
    "Saturday_Sunny_Acoustic.wav",
    "Funky_Good_Mood_Beat.wav",
    "Standing_Eight_Feet_Tall.wav",
    "Sunlit_Heaven.wav",
    "Motown_Bouncy_Groove.wav",
    "Roadside_Stars.wav",
    "Sweet_Acoustic_Breeze.wav",
    "Kings_of_the_Open_Sky.wav",
    "Caught_In_A_Morning_Smile.wav",
    "Chasing_Every_Shadow.wav",
    "Drifting_on_the_Golden_Tide.wav",
    "Make_The_Whole_World_Shine.wav",
    "Barefoot_on_Silver_Shores.wav",
    "Heartbeat_Stereo_Anthem.wav",
    "Carefree_Summer_Windows.wav",
    "Chasing_The_Golden_Light.wav",
    "Chasing_Every_Cloud.wav",
    "Written_in_the_Sky.wav",
    "Golden_Hour_Euphoria.wav",
    "Chasing_the_Golden_Mile.wav"
]

def main():
    tracks = [AUDIO_DIR / t for t in TRACK_LIST]
    
    # マスター共通パイプラインを実行
    build_video_pipeline(
        track_list=tracks,
        bg_media_path=BG_VIDEO,
        output_video_path=OUT_VIDEO,
        output_chapters_path=CHAPTERS_FILE,
        fps=30,
        visualizer_config={
            "enabled": True,
            "fill_color": (255, 255, 255, 220),
            "outline_color": (255, 255, 255, 255)
        }
    )

if __name__ == "__main__":
    main()
