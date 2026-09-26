#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 2時間超 高速ビルドスクリプト (In-place NumPy + VideoToolbox + 自動クリーンアップ)
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
LOFI_DIR = CHANNEL_DIR / "mastered_audio/wav/lofi_mix"
FOCUS_DIR = CHANNEL_DIR / "mastered_audio/wav/focus"
BREAK_DIR = CHANNEL_DIR / "mastered_audio/wav/break"

BG_VIDEO = CHANNEL_DIR / "cover_art/Girl_studying_at_desk_20260922021250.mp4"
OUTPUT_DIR = CHANNEL_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_2hour_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "2HOUR_COZY_LOFI_STUDY_MIX.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "2HOUR_COZY_LOFI_STUDY_MIX_chapters.txt"
COMBINED_WAV = TEMP_DIR / "master_audio_2hour.wav"

PLAYLIST = [
    # Block 1
    ("Fields of Amber Light", LOFI_DIR / "01_Fields_of_Amber_Light.wav"),
    ("A Quiet Corner Table", FOCUS_DIR / "A_Quiet_Corner_Table.wav"),
    ("Lanterns on the River", LOFI_DIR / "02_Lanterns_on_the_River.wav"),
    ("After Hours Window", FOCUS_DIR / "After_Hours_Window.wav"),
    ("Late October Afternoon", LOFI_DIR / "03_Late_October_Afternoon.wav"),
    ("After the Last Train", FOCUS_DIR / "After_the_Last_Train.wav"),
    ("After the Long Tide", BREAK_DIR / "After_the_Long_Tide.wav"),
    
    # Block 2
    ("Leaving the Window Open", LOFI_DIR / "04_Leaving_the_Window_Open.wav"),
    ("Coffee and Paperbacks", FOCUS_DIR / "Coffee_and_Paperbacks.wav"),
    ("Letters by the Window", LOFI_DIR / "05_Letters_by_the_Window.wav"),
    ("Coffee on the Fire Escape", FOCUS_DIR / "Coffee_on_the_Fire_Escape.wav"),
    ("Midnight Wool Blanket", LOFI_DIR / "06_Midnight_Wool_Blanket.wav"),
    ("Midnight in Tokyo", FOCUS_DIR / "Midnight_in_Tokyo.wav"),
    ("Glass Cathedral", BREAK_DIR / "Glass_Cathedral.wav"),
    
    # Block 3
    ("Paper Boats On The Canal", LOFI_DIR / "07_Paper_Boats_On_The_Canal.wav"),
    ("Moonlight Through Blinds", FOCUS_DIR / "Moonlight_Through_Blinds.wav"),
    ("Paper Cranes and Rain", LOFI_DIR / "08_Paper_Cranes_and_Rain.wav"),
    ("Notes on a Wooden Desk", FOCUS_DIR / "Notes_on_a_Wooden_Desk.wav"),
    ("Platform Five At Sunset", LOFI_DIR / "09_Platform_Five_At_Sunset.wav"),
    ("October Window", FOCUS_DIR / "October_Window.wav"),
    ("Rain Upon Copper", BREAK_DIR / "Rain_Upon_Copper.wav"),
    
    # Block 4
    ("Platform at Dusk", LOFI_DIR / "10_Platform_at_Dusk.wav"),
    ("Rain on the Glass", FOCUS_DIR / "Rain_on_the_Glass.wav"),
    ("Porchlight at Midnight", LOFI_DIR / "11_Porchlight_at_Midnight.wav"),
    ("Soft Light on Ivory", FOCUS_DIR / "Soft_Light_on_Ivory.wav"),
    ("Portrait of Rainy Hours", LOFI_DIR / "12_Portrait_of_Rainy_Hours.wav"),
    ("Sunlight on Paper", FOCUS_DIR / "Sunlight_on_Paper.wav"),
    ("Where The River Stops", BREAK_DIR / "Where_The_River_Stops.wav"),
    
    # Block 5
    ("Summer Porch At Twilight", LOFI_DIR / "13_Summer_Porch_At_Twilight.wav"),
    ("Three AM Notebook", FOCUS_DIR / "Three_AM_Notebook.wav"),
    ("Sunday Morning Stream", LOFI_DIR / "14_Sunday_Morning_Stream.wav"),
    ("Warm Light Through Blinds", FOCUS_DIR / "Warm_Light_Through_Blinds.wav"),
    ("Sunlight Through The Blinds", LOFI_DIR / "15_Sunlight_Through_The_Blinds.wav"),
    ("Water Beneath the Keys", FOCUS_DIR / "Water_Beneath_the_Keys.wav"),
    ("Where the Water Rests", BREAK_DIR / "Where_the_Water_Rests.wav"),
    
    # Finale & Encore
    ("The Garden at Dawn", LOFI_DIR / "16_The_Garden_at_Dawn.wav"),
    ("The Last Page Turned", LOFI_DIR / "17_The_Last_Page_Turned.wav"),
    ("Tokyo Window Seat", LOFI_DIR / "18_Tokyo_Window_Seat.wav"),
    ("Under the Canopy", LOFI_DIR / "19_Under_the_Canopy.wav"),
    ("Window Seat View", LOFI_DIR / "20_Window_Seat_View.wav"),
    ("A Quiet Corner Table (Encore)", FOCUS_DIR / "A_Quiet_Corner_Table.wav"),
    ("Coffee and Paperbacks (Encore)", FOCUS_DIR / "Coffee_and_Paperbacks.wav"),
    ("Fields of Amber Light (Encore)", LOFI_DIR / "01_Fields_of_Amber_Light.wav"),
    ("Sunday Morning Stream (Encore)", LOFI_DIR / "14_Sunday_Morning_Stream.wav"),
]

def format_timestamp(sec: float) -> str:
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    else:
        return f"{mins:02d}:{secs:02d}"

def load_wav_as_float(file_path: Path):
    with wave.open(str(file_path), "rb") as w:
        n_channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        n_frames = w.getnframes()
        data = w.readframes(n_frames)
        arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        arr = arr.reshape(-1, n_channels)
        return arr, framerate

def main():
    sys.stdout.reconfigure(line_buffering=True)
    print("==================================================", flush=True)
    print("🎧 2-Hour Cozy Lofi & Warm Piano Mix Builder (In-Place NumPy + VideoToolbox)", flush=True)
    print(f"🎵 Total Tracks: {len(PLAYLIST)}", flush=True)
    print("==================================================", flush=True)

    sample_rate = 48000
    crossfade_sec = 2.5
    crossfade_samples = int(crossfade_sec * sample_rate)

    t = np.linspace(0, np.pi / 2, crossfade_samples, endpoint=False, dtype=np.float32)
    fade_out_curve = np.cos(t)[:, np.newaxis]
    fade_in_curve = np.sin(t)[:, np.newaxis]

    print("📂 Loading audio tracks...", flush=True)
    loaded_audios = []
    total_raw_samples = 0
    for i, (title, track_path) in enumerate(PLAYLIST, start=1):
        audio, sr = load_wav_as_float(track_path)
        loaded_audios.append((title, audio))
        total_raw_samples += len(audio)

    num_transitions = len(loaded_audios) - 1
    total_master_samples = total_raw_samples - (num_transitions * crossfade_samples)
    print(f"✅ Master Audio Samples: {total_master_samples} ({format_timestamp(total_master_samples / sample_rate)})", flush=True)

    master_audio = np.zeros((total_master_samples, 2), dtype=np.float32)
    chapters = []
    current_pos = 0

    print("🔄 Fast in-place DJ crossfade stitching...", flush=True)
    for i, (title, audio) in enumerate(loaded_audios):
        track_len = len(audio)
        if i == 0:
            chapters.append(f"{format_timestamp(0.0)} - {title}")
            master_audio[0:track_len] = audio
            current_pos = track_len
        else:
            track_start_sec = (current_pos - crossfade_samples) / sample_rate
            chapters.append(f"{format_timestamp(track_start_sec)} - {title}")

            blend_start = current_pos - crossfade_samples
            tail = master_audio[blend_start:current_pos]
            head = audio[:crossfade_samples]
            master_audio[blend_start:current_pos] = (tail * fade_out_curve) + (head * fade_in_curve)

            rem_len = track_len - crossfade_samples
            master_audio[current_pos : current_pos + rem_len] = audio[crossfade_samples:]
            current_pos += rem_len

    total_sec = total_master_samples / sample_rate
    print(f"✅ Audio Assembly Complete! Duration: {format_timestamp(total_sec)} ({total_sec/60:.1f} mins)", flush=True)

    # Save Master WAV in chunks
    print(f"💾 Saving master audio WAV to {COMBINED_WAV}...", flush=True)
    master_audio_int16 = (np.clip(master_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    
    with wave.open(str(COMBINED_WAV), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        chunk_size = 2000000
        for offset in range(0, len(master_audio_int16), chunk_size):
            chunk = master_audio_int16[offset:offset+chunk_size]
            w.writeframes(chunk.tobytes())
    print("✅ Master audio WAV saved!", flush=True)

    # Save Chapters
    print(f"📝 Saving chapters to {CHAPTERS_FILE}...", flush=True)
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(chapters) + "\n")
    print("✅ Chapters file saved!", flush=True)

    # Render Final 4K UHD Video using ffmpeg (VideoToolbox hardware acceleration)
    print(f"\n🎬 Rendering final 2-hour 4K UHD video (3840x2160) with VideoToolbox...", flush=True)
    print(f"   Output file: {OUT_VIDEO}", flush=True)

    cmd_video = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(BG_VIDEO),
        "-i", str(COMBINED_WAV),
        "-filter_complex", "[0:v]scale=3840:2160:flags=lanczos,fps=24[vout]",
        "-map", "[vout]",
        "-map", "1:a",
        "-c:v", "h264_videotoolbox",
        "-b:v", "9500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(OUT_VIDEO)
    ]

    res = subprocess.run(cmd_video, capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Error during video rendering:", flush=True)
        print(res.stderr, flush=True)
        sys.exit(1)

    # Cleanup temp WAV to free 1.4GB storage
    if COMBINED_WAV.exists():
        COMBINED_WAV.unlink()
        print(f"🧹 Cleaned up temporary WAV: {COMBINED_WAV}", flush=True)

    print("\n" + "="*60, flush=True)
    print(f"🎉 2-HOUR VIDEO BUILD COMPLETE!", flush=True)
    print(f"   Output Video: {OUT_VIDEO}", flush=True)
    print(f"   Duration: {format_timestamp(total_sec)} ({total_sec/60:.1f} mins)", flush=True)
    print(f"   Chapters: {CHAPTERS_FILE}", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    main()
