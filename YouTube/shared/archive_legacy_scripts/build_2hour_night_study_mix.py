#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 2-Hour Midnight Cozy Lofi Study Mix Builder (4K UHD)
- Background Video: cover_art/Woman_writing_in_room_20260923102023.mp4
- Pure Mastered Audio (No Veo background noise, In-Place NumPy 2.5s DJ Crossfade)
- Equidistant Break Tracks (Break track every 7th track = ~20 min intervals)
- Completely fresh track order (0 collisions with previous video)
- 'Three AM Notebook' completely excluded
- 4K Lanczos Hardware Accelerated Render
"""

import os
import sys
import wave
import subprocess
import shutil
import numpy as np
from pathlib import Path

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
LOFI_DIR = CHANNEL_DIR / "mastered_audio/wav/lofi_mix"
FOCUS_DIR = CHANNEL_DIR / "mastered_audio/wav/focus"
BREAK_DIR = CHANNEL_DIR / "mastered_audio/wav/break"

BG_VIDEO = CHANNEL_DIR / "cover_art/Woman_writing_in_room_20260923102023.mp4"
OUTPUT_DIR = CHANNEL_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_2hour_midnight_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "2HOUR_MIDNIGHT_STUDY_WITH_ME_LOFI_4K.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "2HOUR_MIDNIGHT_STUDY_WITH_ME_LOFI_4K_chapters.txt"
COMBINED_WAV = TEMP_DIR / "master_audio_2hour_midnight.wav"

# Categorized audio mapping
lofi_map = {
    'Fields of Amber Light': LOFI_DIR / '01_Fields_of_Amber_Light.wav',
    'Lanterns on the River': LOFI_DIR / '02_Lanterns_on_the_River.wav',
    'Late October Afternoon': LOFI_DIR / '03_Late_October_Afternoon.wav',
    'Leaving the Window Open': LOFI_DIR / '04_Leaving_the_Window_Open.wav',
    'Letters by the Window': LOFI_DIR / '05_Letters_by_the_Window.wav',
    'Midnight Wool Blanket': LOFI_DIR / '06_Midnight_Wool_Blanket.wav',
    'Paper Boats On The Canal': LOFI_DIR / '07_Paper_Boats_On_The_Canal.wav',
    'Paper Cranes and Rain': LOFI_DIR / '08_Paper_Cranes_and_Rain.wav',
    'Platform Five At Sunset': LOFI_DIR / '09_Platform_Five_At_Sunset.wav',
    'Platform at Dusk': LOFI_DIR / '10_Platform_at_Dusk.wav',
    'Porchlight at Midnight': LOFI_DIR / '11_Porchlight_at_Midnight.wav',
    'Portrait of Rainy Hours': LOFI_DIR / '12_Portrait_of_Rainy_Hours.wav',
    'Summer Porch At Twilight': LOFI_DIR / '13_Summer_Porch_At_Twilight.wav',
    'Sunday Morning Stream': LOFI_DIR / '14_Sunday_Morning_Stream.wav',
    'Sunlight Through The Blinds': LOFI_DIR / '15_Sunlight_Through_The_Blinds.wav',
    'The Garden at Dawn': LOFI_DIR / '16_The_Garden_at_Dawn.wav',
    'The Last Page Turned': LOFI_DIR / '17_The_Last_Page_Turned.wav',
    'Tokyo Window Seat': LOFI_DIR / '18_Tokyo_Window_Seat.wav',
    'Under the Canopy': LOFI_DIR / '19_Under_the_Canopy.wav',
    'Window Seat View': LOFI_DIR / '20_Window_Seat_View.wav',
}

focus_map = {
    'A Quiet Corner Table': FOCUS_DIR / 'A_Quiet_Corner_Table.wav',
    'After Hours Window': FOCUS_DIR / 'After_Hours_Window.wav',
    'After the Last Train': FOCUS_DIR / 'After_the_Last_Train.wav',
    'Coffee and Paperbacks': FOCUS_DIR / 'Coffee_and_Paperbacks.wav',
    'Coffee on the Fire Escape': FOCUS_DIR / 'Coffee_on_the_Fire_Escape.wav',
    'Midnight in Tokyo': FOCUS_DIR / 'Midnight_in_Tokyo.wav',
    'Moonlight Through Blinds': FOCUS_DIR / 'Moonlight_Through_Blinds.wav',
    'Notes on a Wooden Desk': FOCUS_DIR / 'Notes_on_a_Wooden_Desk.wav',
    'October Window': FOCUS_DIR / 'October_Window.wav',
    'Rain on the Glass': FOCUS_DIR / 'Rain_on_the_Glass.wav',
    'Soft Light on Ivory': FOCUS_DIR / 'Soft_Light_on_Ivory.wav',
    'Sunlight on Paper': FOCUS_DIR / 'Sunlight_on_Paper.wav',
    'Warm Light Through Blinds': FOCUS_DIR / 'Warm_Light_Through_Blinds.wav',
    'Water Beneath the Keys': FOCUS_DIR / 'Water_Beneath_the_Keys.wav',
}

break_map = {
    'After the Long Tide': BREAK_DIR / 'After_the_Long_Tide.wav',
    'Glass Cathedral': BREAK_DIR / 'Glass_Cathedral.wav',
    'Rain Upon Copper': BREAK_DIR / 'Rain_Upon_Copper.wav',
    'Where The River Stops': BREAK_DIR / 'Where_The_River_Stops.wav',
    'Where the Water Rests': BREAK_DIR / 'Where_the_Water_Rests.wav',
}

PLAYLIST = [
    # Block 1 (Focus / Lofi / Focus / Lofi / Focus / Lofi / BREAK)
    ('Rain on the Glass', focus_map['Rain on the Glass']),
    ('Porchlight at Midnight', lofi_map['Porchlight at Midnight']),
    ('Midnight in Tokyo', focus_map['Midnight in Tokyo']),
    ('Midnight Wool Blanket', lofi_map['Midnight Wool Blanket']),
    ('Notes on a Wooden Desk', focus_map['Notes on a Wooden Desk']),
    ('Paper Cranes and Rain', lofi_map['Paper Cranes and Rain']),
    ('Glass Cathedral', break_map['Glass Cathedral']),
    
    # Block 2
    ('Moonlight Through Blinds', focus_map['Moonlight Through Blinds']),
    ('Leaving the Window Open', lofi_map['Leaving the Window Open']),
    ('Coffee on the Fire Escape', focus_map['Coffee on the Fire Escape']),
    ('Portrait of Rainy Hours', lofi_map['Portrait of Rainy Hours']),
    ('October Window', focus_map['October Window']),
    ('Letters by the Window', lofi_map['Letters by the Window']),
    ('Rain Upon Copper', break_map['Rain Upon Copper']),
    
    # Block 3
    ('Soft Light on Ivory', focus_map['Soft Light on Ivory']),
    ('Fields of Amber Light', lofi_map['Fields of Amber Light']),
    ('After Hours Window', focus_map['After Hours Window']),
    ('Late October Afternoon', lofi_map['Late October Afternoon']),
    ('Coffee and Paperbacks', focus_map['Coffee and Paperbacks']),
    ('Lanterns on the River', lofi_map['Lanterns on the River']),
    ('Where The River Stops', break_map['Where The River Stops']),
    
    # Block 4
    ('After the Last Train', focus_map['After the Last Train']),
    ('Paper Boats On The Canal', lofi_map['Paper Boats On The Canal']),
    ('Warm Light Through Blinds', focus_map['Warm Light Through Blinds']),
    ('Platform at Dusk', lofi_map['Platform at Dusk']),
    ('A Quiet Corner Table', focus_map['A Quiet Corner Table']),
    ('Summer Porch At Twilight', lofi_map['Summer Porch At Twilight']),
    ('After the Long Tide', break_map['After the Long Tide']),
    
    # Block 5
    ('Water Beneath the Keys', focus_map['Water Beneath the Keys']),
    ('Platform Five At Sunset', lofi_map['Platform Five At Sunset']),
    ('Sunlight on Paper', focus_map['Sunlight on Paper']),
    ('Sunlight Through The Blinds', lofi_map['Sunlight Through The Blinds']),
    ('Sunday Morning Stream', lofi_map['Sunday Morning Stream']),
    ('Where the Water Rests', break_map['Where the Water Rests']),
    
    # Block 6 (Remaining 5 Lofi)
    ('The Garden at Dawn', lofi_map['The Garden at Dawn']),
    ('The Last Page Turned', lofi_map['The Last Page Turned']),
    ('Tokyo Window Seat', lofi_map['Tokyo Window Seat']),
    ('Under the Canopy', lofi_map['Under the Canopy']),
    ('Window Seat View', lofi_map['Window Seat View']),
    
    # Reprises / Encores (5 tracks -> Total 44 tracks)
    ('Rain on the Glass (Reprise)', focus_map['Rain on the Glass']),
    ('Porchlight at Midnight (Reprise)', lofi_map['Porchlight at Midnight']),
    ('Midnight in Tokyo (Reprise)', focus_map['Midnight in Tokyo']),
    ('Midnight Wool Blanket (Reprise)', lofi_map['Midnight Wool Blanket']),
    ('Notes on a Wooden Desk (Reprise)', focus_map['Notes on a Wooden Desk']),
]

def format_timestamp(sec: float) -> str:
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

def load_wav_as_float(path: Path):
    with wave.open(str(path), 'rb') as w:
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
    print("🌙 Ch 1: 2-Hour Midnight Study With Me 4K Mix Builder", flush=True)
    print(f"🎵 Total Tracks: {len(PLAYLIST)}", flush=True)
    print(f"🎥 Video Loop: {BG_VIDEO.name} (4K 3840x2160 Lanczos)", flush=True)
    print("==================================================", flush=True)

    sample_rate = 48000
    crossfade_sec = 2.5
    fade_samples = int(crossfade_sec * sample_rate)

    t_in = np.linspace(0, np.pi / 2, fade_samples, endpoint=False)
    in_curve = np.sin(t_in)[:, np.newaxis]
    out_curve = np.cos(t_in)[:, np.newaxis]

    track_audio_data = []
    chapters = []
    current_time = 0.0

    print("▶ Phase 1: Loading & Trimming tracks...", flush=True)
    for idx, (title, path) in enumerate(PLAYLIST):
        if not path.exists():
            print(f"❌ Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
            
        arr, sr = load_wav_as_float(path)
        if sr != sample_rate:
            print(f"Warning: Sample rate mismatch {sr} != {sample_rate} for {path.name}")

        # Smart trim silence
        mono = np.max(np.abs(arr), axis=1)
        threshold = 0.005 # -46dB
        above = np.where(mono > threshold)[0]
        if len(above) > 0:
            last_idx = min(len(arr), above[-1] + int(0.2 * sample_rate))
            arr = arr[:last_idx]

        dur = len(arr) / sample_rate
        timestamp_str = format_timestamp(current_time)
        chapters.append(f"{timestamp_str} - {title}")
        print(f"  [{idx+1:02d}/{len(PLAYLIST):02d}] {timestamp_str} | {title} ({dur:.1f}s)", flush=True)

        track_audio_data.append(arr)
        current_time += (dur - crossfade_sec) if idx > 0 else dur

    # Save chapters file
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(chapters) + "\n")
    print(f"\n✅ Chapters written to: {CHAPTERS_FILE}", flush=True)

    # Calculate total length
    total_samples = 0
    for idx, arr in enumerate(track_audio_data):
        if idx == 0:
            total_samples += len(arr)
        else:
            total_samples += (len(arr) - fade_samples)

    print(f"\n▶ Phase 2: In-place DJ Crossfading {len(track_audio_data)} tracks ({total_samples / sample_rate / 60:.2f} mins)...", flush=True)
    output_audio = np.zeros((total_samples, 2), dtype=np.float32)

    current_idx = 0
    for idx, arr in enumerate(track_audio_data):
        track_len = len(arr)
        if idx == 0:
            output_audio[0:track_len] += arr
            current_idx = track_len - fade_samples
        else:
            overlap = output_audio[current_idx:current_idx + fade_samples]
            output_audio[current_idx:current_idx + fade_samples] = overlap * out_curve + arr[:fade_samples] * in_curve
            output_audio[current_idx + fade_samples:current_idx + track_len] = arr[fade_samples:]
            current_idx += (track_len - fade_samples)

    # Master limiter check
    peak = np.max(np.abs(output_audio))
    print(f"  Max peak level: {peak:.4f}", flush=True)
    if peak > 0.98:
        print(f"  Applying safety limiter scaling: {0.95 / peak:.4f}", flush=True)
        output_audio *= (0.95 / peak)

    print(f"▶ Phase 3: Writing Master WAV -> {COMBINED_WAV.name}...", flush=True)
    int16_audio = (np.clip(output_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(COMBINED_WAV), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(int16_audio.tobytes())

    total_duration_sec = total_samples / sample_rate
    print(f"✅ Audio assembly complete! Duration: {total_duration_sec/60:.2f} mins ({total_duration_sec:.1f}s)", flush=True)

    # Render 4K Video with FFmpeg Hardware acceleration
    print(f"\n▶ Phase 4: Hardware Rendering 4K Video -> {OUT_VIDEO.name}...", flush=True)
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", str(BG_VIDEO),
        "-i", str(COMBINED_WAV),
        "-t", f"{total_duration_sec:.3f}",
        "-vf", "scale=3840:2160:flags=lanczos",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "h264_videotoolbox",
        "-b:v", "9500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_VIDEO)
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg error:\n{res.stdout}", file=sys.stderr)
        sys.exit(res.returncode)

    # Cleanup temp audio
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"🧹 Cleaned up temporary directory: {TEMP_DIR.name}", flush=True)

    print("\n==================================================", flush=True)
    print(f"🎉 2-HOUR 4K VIDEO RENDER SUCCESSFUL!", flush=True)
    print(f"📁 Video: {OUT_VIDEO}", flush=True)
    print(f"📄 Chapters: {CHAPTERS_FILE}", flush=True)
    print(f"⏱️ Duration: {total_duration_sec/60:.2f} mins ({format_timestamp(total_duration_sec)})", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    main()
