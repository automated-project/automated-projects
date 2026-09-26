#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 完全自動 3本Shorts レンダリング & YouTubeアップロード
- 1. Hydraulic_Vise.wav (Power Rack / Heavy Workout)
- 2. Shadow_Predator_808.wav (Dark Combat Arena / Beast Mode)
- 3. Cyber_Prism_Overclock.wav (Cyberpunk Rain / Night Training)
- Futura Bold ネオングロー直載せ ＋ 重低音連動パルス ＋ 48本丸角波形
- API事前タイトル重複チェック ＆ 多言語ローカライズ ＆ 固定コメント
"""

import os
import sys
import time
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
MASTERED_WAV_DIR = BASE_DIR / "mastered_audio/wav"
BG_SHORTS_DIR = BASE_DIR / "cover_art/bg_shorts"
OUT_DIR = BASE_DIR / "output_videos/shorts"
TEMP_DIR = BASE_DIR / "output_videos/temp_3_shorts_build"

OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

# 波形ビジュアライザー設定
NUM_BARS = 48
BAR_WIDTH = 12
BAR_GAP = 6
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 340
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

SHORTS_QUEUE = [
    {
        "id": "shorts_new_01_hydraulic_vise",
        "wav_name": "Hydraulic_Vise.wav",
        "bg_name": "bg_power_rack.jpeg",
        "start_sec": 26.0,
        "duration_sec": 22.0,
        "text_main": "MAX WEIGHT OVERDRIVE",
        "text_sub": "HEAVY BASS MOTIVATION",
        "glow_color": (255, 30, 50),
        "file_name": "SHORTS_CH2_HYDRAULIC_VISE.mp4",
        "base_title_en": "⚡ MAX WEIGHT OVERDRIVE — Heavy Bass Gym Phonk [Free BGM] #Shorts #gym",
        "title_ja": "【筋トレ用BGM】超高重量対応・極太キックの破壊的Gym Phonk ⚡ フリーBGM #Shorts #筋トレ",
        "title_ko": "[고중량 헬스 폰크] 묵직한 베이스 비트 • 헬스장 텐션업 Gym Phonk #Shorts #헬스",
        "title_ru": "⚡ Тяжелый бас для жима и приседа — Gym Phonk Drop [Free BGM] #Shorts #gym",
        "title_pt": "⚡ Grave Pesado para Treino Pesado — Gym Phonk Drop [Free BGM] #Shorts #treino",
        "title_es": "⚡ Bajo Extremo para Cargar Pesado en el Gym — Gym Phonk [Free BGM] #Shorts #gym",
        "desc_en": (
            "⚡ Cold, crushing heavy bass phonk engineered for heavy lifts and peak workout motivation.\n"
            "Feel the sub-bass pressure and conquer your sets!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "🔥 Check our sister chill channel: @Haven-Chill-Audio\n\n"
            "#GymPhonk #WorkoutMotivation #HeavyBass #Fitness #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "⚡ 高重量トレーニング・追い込みのための破壊的重低音サウンド。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "#筋トレ #ワークアウト #超重低音 #フィットネス #フリーBGM #Shorts"
        ),
        "comment_text": "🔥 100% Free to use for your gym & fitness videos! Subscribe for weekly heavy bass drops! ⚡",
        "tags": ["shorts", "gym phonk", "heavy bass", "workout music", "gym motivation", "free bgm", "bass boosted", "phonkforge audio"]
    },
    {
        "id": "shorts_new_02_shadow_predator",
        "wav_name": "Shadow_Predator_808.wav",
        "bg_name": "bg_dark_combat_shorts.jpeg",
        "start_sec": 8.0,
        "duration_sec": 22.0,
        "text_main": "BRUTAL BEAST ADRENALINE",
        "text_sub": "EXTREME 808 BASS DROP",
        "glow_color": (255, 45, 45),
        "file_name": "SHORTS_CH2_SHADOW_PREDATOR.mp4",
        "base_title_en": "🔥 BRUTAL BEAST ADRENALINE — Aggressive Workout Phonk [Free DL] #Shorts #workout",
        "title_ja": "【戦闘態勢】アドレナリン爆発。獰猛な808ベースラインPHONK 🔥 フリー音源 #Shorts #ワークアウト",
        "title_ko": "[비스트 각성] 아드レ날린 폭발 808 베이스 짐 폰크 #Shorts #운동",
        "title_ru": "🔥 Режим хищника — Жесткий и мощный 808 Gym Phonk [Free DL] #Shorts #тренировка",
        "title_pt": "🔥 Modo Predador Ativado — 808 Bass Gym Phonk [Free DL] #Shorts #academia",
        "title_es": "🔥 Modo Bestia 808 — Phonk Agresivo para Entrenar [Free DL] #Shorts #fitness",
        "desc_en": (
            "🔥 Aggressive 808 heavy bass phonk designed for high-intensity training and beast mode focus.\n"
            "Unleash maximum power and break your personal records!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "#BeastMode #GymPhonk #WorkoutMusic #808Bass #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "🔥 限界を超える集中力と闘争心を引き出す、獰猛な808重低音ビート。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "#筋トレ #アドレナリン #ワークアウト #重低音 #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for creators! Let us know your PR target in the comments below! 🔥",
        "tags": ["shorts", "beast mode", "gym phonk", "workout music", "808 bass", "free bgm", "powerlifting", "phonkforge audio"]
    },
    {
        "id": "shorts_new_03_cyber_prism",
        "wav_name": "Cyber_Prism_Overclock.wav",
        "bg_name": "bg_cyberpunk_rain_shorts.jpeg",
        "start_sec": 7.0,
        "duration_sec": 22.0,
        "text_main": "CYBER OVERCLOCK PHONK",
        "text_sub": "HARDSTYLE HEAVY BASS",
        "glow_color": (0, 220, 255),
        "file_name": "SHORTS_CH2_CYBER_PRISM.mp4",
        "base_title_en": "⚡ CYBER OVERCLOCK PHONK — Hardstyle Heavy Bass [Free BGM] #Shorts #fitness",
        "title_ja": "【超集中BGM】脳を覚醒させるサイバー重低音ハードスタイルPHONK ⚡ フリーBGM #Shorts #筋トレ",
        "title_ko": "[사이버 오버클럭] 심장 뛰게 만드는 하드스타일 헤비 베이스 폰크 #Shorts #헬스장",
        "title_ru": "⚡ Киберпанк тренировки — Hardstyle Heavy Bass Phonk [Free BGM] #Shorts #спорт",
        "title_pt": "⚡ Treino Cyberpunk — Hardstyle Heavy Bass Phonk [Free BGM] #Shorts #maromba",
        "title_es": "⚡ Estilo Cyberpunk — Hardstyle Heavy Bass Phonk [Free BGM] #Shorts #gymtok",
        "desc_en": (
            "⚡ Futuristic Cyber Overclock Heavy Bass Phonk for extreme gym workouts and late-night focus.\n"
            "Drive your intensity to maximum levels!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "#CyberPhonk #Hardstyle #GymMotivation #HeavyBass #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "⚡ 研ぎ澄まされたサイバー空間の重低音。夜間トレーニングや限界突破に。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "#筋トレ #ハードスタイル #集中力 #重低音 #フリーBGM #Shorts"
        ),
        "comment_text": "🔥 100% Free & Royalty-Free! Hit LIKE 👍 if this drop energized your workout! ⚡",
        "tags": ["shorts", "cyber phonk", "hardstyle", "gym phonk", "heavy bass", "workout music", "free bgm", "phonkforge audio"]
    }
]

def load_futura_font(size, index=4):
    try:
        return ImageFont.truetype(FUTURA_PATH, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(FUTURA_PATH, size, index=0)
        except Exception:
            return ImageFont.load_default()

def create_text_overlay(width, height, text_main, text_sub, glow_color):
    font_main = load_futura_font(56, index=4)  # Bold
    font_sub = load_futura_font(32, index=1)   # Medium

    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)

    y_main = 280
    y_sub = 355

    bbox_m = font_main.getbbox(text_main)
    w_m = bbox_m[2] - bbox_m[0]
    x_m = (width - w_m) // 2

    bbox_s = font_sub.getbbox(text_sub)
    w_s = bbox_s[2] - bbox_s[0]
    x_s = (width - w_s) // 2

    glow_draw.text((x_m, y_main), text_main, font=font_main, fill=(glow_color[0], glow_color[1], glow_color[2], 240))
    glow_draw.text((x_s, y_sub), text_sub, font=font_sub, fill=(glow_color[0], glow_color[1], glow_color[2], 200))
    
    glow_blurred = glow_img.filter(ImageFilter.GaussianBlur(radius=10))

    text_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    text_overlay = Image.alpha_composite(text_overlay, glow_blurred)
    draw = ImageDraw.Draw(text_overlay)
    
    draw.text((x_m, y_main), text_main, font=font_main, fill=(255, 255, 255, 255))
    draw.text((x_s, y_sub), text_sub, font=font_sub, fill=(240, 240, 240, 230))

    return text_overlay

def render_shorts_video(item):
    print(f"\n==================================================")
    print(f"▶ RENDERING SHORTS: {item['id']}")
    print(f"  Track: {item['wav_name']} | BG: {item['bg_name']}")
    print(f"==================================================")

    wav_path = MASTERED_WAV_DIR / item["wav_name"]
    bg_path = BG_SHORTS_DIR / item["bg_name"]
    out_path = OUT_DIR / item["file_name"]
    hook_wav = TEMP_DIR / f"hook_{item['id']}.wav"

    if not wav_path.exists():
        print(f"❌ Error: Audio file not found: {wav_path}")
        return False
    if not bg_path.exists():
        print(f"❌ Error: Background file not found: {bg_path}")
        return False

    # 1. 音源切り出し
    with wave.open(str(wav_path), 'rb') as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        s_sample = int(item["start_sec"] * sr)
        e_sample = s_sample + int(item["duration_sec"] * sr)
        wf.setpos(s_sample)
        raw = wf.readframes(e_sample - s_sample)

    hook_audio = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_channels).copy()

    fade_samples = int(sr * 0.25)
    fo = np.linspace(1.0, 0.0, fade_samples)[:, None]
    hook_audio[-fade_samples:] = (hook_audio[-fade_samples:].astype(np.float32) * fo).astype(np.int16)

    with wave.open(str(hook_wav), 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(hook_audio.tobytes())

    duration = len(hook_audio) / sr
    audio_mono = 0.5 * (hook_audio[:, 0].astype(np.float32) + hook_audio[:, 1].astype(np.float32)) / 32768.0
    samples_per_frame = sr // FPS
    total_frames = len(audio_mono) // samples_per_frame

    # 2. 背景画像準備
    orig_bg = Image.open(bg_path).convert("RGBA")
    img_w, img_h = orig_bg.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        orig_bg = orig_bg.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        orig_bg = orig_bg.crop((0, top, img_w, top + new_h))

    OVER_W = int(WIDTH * 1.06)
    OVER_H = int(HEIGHT * 1.06)
    bg_oversized = orig_bg.resize((OVER_W, OVER_H), Image.Resampling.LANCZOS)

    text_overlay = create_text_overlay(WIDTH, HEIGHT, item["text_main"], item["text_sub"], item["glow_color"])

    fft_size = 2048
    freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    freq_weights = np.zeros(NUM_BARS)
    for b in range(NUM_BARS):
        f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
        freq_weights[b] = (f_center / 100.0) ** 0.50 * 18.0
    bass_idx = np.where((freqs >= 40) & (freqs <= 160))[0]

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(hook_wav),
        "-c:v", "h264_videotoolbox",
        "-b:v", "4000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_path)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    prev_heights = np.zeros(NUM_BARS)
    prev_pulse = 0.0
    hanning_win = np.hanning(fft_size)

    for f_idx in range(total_frames):
        start_s = f_idx * samples_per_frame
        chunk = audio_mono[start_s : start_s + fft_size]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))

        windowed = chunk * hanning_win
        spectrum = np.abs(np.fft.rfft(windowed)) / (fft_size / 2)

        bass_energy = np.mean(spectrum[bass_idx]) * 15.0
        target_pulse = np.clip((bass_energy - 0.12) * 1.5, 0.0, 1.0)
        if target_pulse > prev_pulse:
            pulse = target_pulse
        else:
            pulse = prev_pulse * 0.78
        prev_pulse = pulse

        scale = 1.00 + (pulse ** 1.2) * 0.035
        cur_w = int(WIDTH * scale)
        cur_h = int(HEIGHT * scale)
        crop_x = (OVER_W - cur_w) // 2
        crop_y = (OVER_H - cur_h) // 2

        frame = bg_oversized.crop((crop_x, crop_y, crop_x + cur_w, crop_y + cur_h)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        target_heights = np.zeros(NUM_BARS)
        for b in range(NUM_BARS):
            idx_range = np.where((freqs >= freq_bins[b]) & (freqs < freq_bins[b+1]))[0]
            if len(idx_range) > 0:
                val = np.mean(spectrum[idx_range])
            else:
                closest_idx = np.argmin(np.abs(freqs - (freq_bins[b] + freq_bins[b+1])/2))
                val = spectrum[closest_idx]
            adj = np.clip(val * freq_weights[b], 0.0, 1.0)
            target_heights[b] = MIN_BAR_HEIGHT + (adj ** 0.85) * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)

        smooth_heights = np.zeros(NUM_BARS)
        for b in range(NUM_BARS):
            if target_heights[b] >= prev_heights[b]:
                smooth_heights[b] = target_heights[b]
            else:
                smooth_heights[b] = max(MIN_BAR_HEIGHT, prev_heights[b] * 0.82)
        prev_heights = smooth_heights

        vis_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_vis = ImageDraw.Draw(vis_overlay)
        for b in range(NUM_BARS):
            h = int(smooth_heights[b])
            x0 = START_X + b * (BAR_WIDTH + BAR_GAP)
            x1 = x0 + BAR_WIDTH
            y1 = BASE_Y
            y0 = BASE_Y - h
            draw_vis.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=(255, 255, 255, 220), outline=(255, 255, 255, 255), width=1)

        frame = Image.alpha_composite(frame, vis_overlay)
        frame = Image.alpha_composite(frame, text_overlay)

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

    if hook_wav.exists():
        hook_wav.unlink()

    print(f"✅ Render Complete: {out_path} ({duration:.2f}s)")
    return True

def fetch_existing_titles(yt):
    print("[+] Fetching existing channel video titles for collision check...")
    existing = set()
    try:
        res = yt.search().list(part="snippet", forMine=True, type="video", maxResults=50).execute()
        for item in res.get("items", []):
            existing.add(item["snippet"]["title"])
        print(f"[+] Found {len(existing)} existing titles.")
    except Exception as e:
        print(f"⚠️ Warning during title fetch: {e}")
    return existing

def resolve_unique(title, existing):
    if title not in existing:
        return title
    variants = [
        title.replace("🔥", "⚡"),
        title.replace("⚡", "🔥"),
        title.replace("[Free BGM]", "[Free DL]"),
        title.replace("[Free DL]", "[Free BGM]"),
        title + " ⚡",
        title + " 🔥",
        title.replace("#Shorts", "#Shorts #viral")
    ]
    for v in variants:
        if v not in existing:
            return v
    return title + f" #{int(time.time())%1000}"

def upload_all_shorts():
    print("\n==================================================")
    print("🚀 PHONK SHORTS: UPLOADING TO YOUTUBE")
    print("==================================================")

    yt = get_youtube_service("phonkforge")
    existing_titles = fetch_existing_titles(yt)
    results = []

    for idx, item in enumerate(SHORTS_QUEUE):
        v_path = OUT_DIR / item["file_name"]
        if not v_path.exists():
            print(f"❌ File not found: {v_path}")
            continue

        print(f"\n[{idx+1}/{len(SHORTS_QUEUE)}] Uploading: {item['file_name']}")
        unique_title = resolve_unique(item["base_title_en"], existing_titles)
        existing_titles.add(unique_title)
        print(f"  Title: {unique_title}")

        localizations = {
            "ja": {"title": item["title_ja"], "description": item["desc_ja"]},
            "ko": {"title": item["title_ko"], "description": item["desc_en"]},
            "ru": {"title": item["title_ru"], "description": item["desc_en"]},
            "pt": {"title": item["title_pt"], "description": item["desc_en"]},
            "es": {"title": item["title_es"], "description": item["desc_en"]}
        }

        body = {
            "snippet": {
                "title": unique_title,
                "description": item["desc_en"],
                "tags": item["tags"],
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            },
            "localizations": localizations
        }

        media = MediaFileUpload(str(v_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        req = yt.videos().insert(part="snippet,status,localizations", body=body, media_body=media)

        res = None
        while res is None:
            st, res = req.next_chunk()
            if st:
                print(f"    Progress: {int(st.progress() * 100)}%")

        vid = res.get("id")
        print(f"  ✅ Upload Successful! ID: {vid} (https://www.youtube.com/shorts/{vid})")

        time.sleep(2)
        try:
            yt.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": vid,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": item["comment_text"]
                            }
                        }
                    }
                }
            ).execute()
            print("  ✅ Pinned Comment posted successfully")
        except Exception as e:
            print(f"  ⚠️ Note on comment post: {e}")

        results.append({
            "id": vid,
            "title": unique_title,
            "url": f"https://www.youtube.com/shorts/{vid}"
        })

        if idx < len(SHORTS_QUEUE) - 1:
            print("  ⏳ Waiting 4s before next upload...")
            time.sleep(4)

    print("\n==================================================")
    print("🎉 ALL 3 SHORTS SUCCESSFULLY UPLOADED & PUBLISHED!")
    print("==================================================")
    for r in results:
        print(f"  • {r['title']}: {r['url']}")
    print("==================================================")

def main():
    for item in SHORTS_QUEUE:
        render_shorts_video(item)
    upload_all_shorts()

if __name__ == "__main__":
    main()
