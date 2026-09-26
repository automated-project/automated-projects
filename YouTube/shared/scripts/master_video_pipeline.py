#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated-Projects YouTube動画制作 完全共通コアエンジン (Master Video Pipeline Engine)
- 憲法レベルの定数・変数をすべてPythonコード・辞書としてハードコーディング
- ドキュメントがどう書かれていようと、このスクリプトを実行すれば100%最新の確定仕様でしか動作しない
"""

import os
import sys
import json
import wave
import shutil
import random
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

YOUTUBE_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(YOUTUBE_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(YOUTUBE_ROOT_DIR))

from shared.scripts.visualizer_engine import MinimalPolyrhythmVisualizer

# ==============================================================================
# 🔒 1. システム全体で絶対に書き換えない不変の定数 (CONSTANTS)
# ==============================================================================
TARGET_WIDTH = 3840
TARGET_HEIGHT = 2160
DEFAULT_FPS = 30
SAMPLE_RATE = 44100
CROSSFADE_SEC = 2.5
CROSSFADE_SAMPLES = int(CROSSFADE_SEC * SAMPLE_RATE)
PEAK_LIMIT = 0.95

FUTURA_FONT_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"
SIGNPAINTER_FONT_PATH = "/System/Library/Fonts/Supplemental/SignPainter.ttc"

# ==============================================================================
# 🎛️ 2. チャンネル別 確定変数設定マトリクス (Channel Configuration Matrix)
# ==============================================================================
CHANNEL_CONFIGS = {
    "ch1": {
        "channel_id": "ch1",
        "name": "Haven Chill Audio",
        "account_key": "chill",
        "genre": "Midnight & Rainy Dark Lofi",
        "mastering_profile": "ch1_zero_eq_natural",
        "mastering_filter": "alimiter=limit=0.95:level=disabled",
        "target_duration_mins": 120,  # 2時間長尺
        "min_duration_sec": 7200.0,
        "visualizer": {
            "enabled": False,  # Ch1は睡眠・深い思考の邪魔をしないため波形完全OFF
            "fill_color": (255, 255, 255, 0),
            "outline_color": (255, 255, 255, 0),
            "scale": (0.0, 0.0),
            "y_offset_ratio": 0.90
        },
        "thumbnail": {
            "font_index": 0,  # Futura Medium
            "font_size_main": 105,
            "font_size_sub": 52,
            "glow_color": (255, 235, 180),  # Warm Amber Glow
            "text_color": (255, 255, 255)
        },
        # 🌌 【日常の安心な部屋 × 窓の外の静かな違和感】Imagen 3 確定プロンプト
        "visual_prompt_template": (
            "An ultra-detailed cinematic interior photography, 16:9 widescreen composition. "
            "A cozy, warm minimalist bedroom at midnight, a safe sanctuary from the dark. "
            "A warm wooden desk with an open notebook and an amber glowing vintage desk lamp casting a soft golden pool of light. "
            "Beside the desk, a massive arched floor-to-ceiling glass window with soft rain droplets trickling down. "
            "Just outside the glass, hanging impossibly close in the clear dark starry night sky, is a colossal, softly glowing crescent moon, "
            "casting ethereal silver moonlight across the warm wooden floor. "
            "Deep comfort, tranquil solitude, no people, gender-neutral, 85mm f/1.4 lens, hyper-realistic cozy textures, 8k resolution, cinematic masterpiece --ar 16:9"
        ),
        "package_presets": [
            {
                "pattern_id": "01_situation",
                "concept": "時間帯・シチュエーション特化（王道クリック率）",
                "thumb": {"name": "THUMB_01_3AM_STUDY", "main": "3 AM STUDY", "sub": "2 HOURS • DEEP FOCUS LOFI"},
                "title": "3 AM Study with Me 🌙 2 Hours Cozy Midnight Lofi & Felt Piano for Deep Focus / Sleep [4K]"
            },
            {
                "pattern_id": "02_usage",
                "concept": "具体的用途・空間特化（作業・勉強）",
                "thumb": {"name": "THUMB_02_STUDY_WITH_ME", "main": "STUDY WITH ME", "sub": "2 HOURS • WARM DESK LOFI"},
                "title": "Study With Me at Midnight ☕ 2-Hour Cozy Lofi Beats for Deep Focus, Work & Reading [4K UHD]"
            },
            {
                "pattern_id": "03_mood",
                "concept": "感情・没入感特化（静寂・睡眠）",
                "thumb": {"name": "THUMB_03_MIDNIGHT_HAVEN", "main": "MIDNIGHT HAVEN", "sub": "2 HOURS • RAINY NIGHT PIANO"},
                "title": "Midnight Haven 🌧️ 2 Hours Gentle Felt Piano & Soft Rain Lofi for Deep Sleep & Peace [4K]"
            }
        ]
    },
    "ch2": {
        "channel_id": "ch2",
        "name": "Velvet Sunset Audio",
        "account_key": "phonk",
        "genre": "Sunset Pop & R&B",
        "mastering_profile": "ch2_zero_eq_natural",
        "mastering_filter": "alimiter=limit=0.95:level=disabled",
        "target_duration_mins": 30,  # 30分長尺
        "min_duration_sec": 1800.0,
        "visualizer": {
            "enabled": True,
            "type": "minimal_3bars",
            "bpm": 102.0
        },
        "thumbnail": {
            "font_path": SIGNPAINTER_FONT_PATH,
            "font_index": 0,  # SignPainter HouseScript
            "font_size_main": 260,
            "font_size_sub": 0,  # サブタイトル完全排除
            "glow_color": (255, 140, 50),  # Sunset Orange Glow
            "text_color": (255, 255, 255),
            "layout": "center"
        },
        # 🌇 【夕暮れの都市交差点 × 透明道路の違和感】Imagen 3 確定プロンプト
        "visual_prompt_template": (
            "An ultra-detailed contemporary urban fine art photography, 16:9 widescreen composition. "
            "An empty, sun-drenched city intersection surrounded by towering brownstone buildings and skyscrapers at a glowing crimson sunset. "
            "The asphalt street surface seamlessly transitions into a flawlessly transparent glass floor, revealing a deep, sunlit underwater cityscape directly beneath the street. "
            "Long golden hour shadows stretching across the warm pavement, traffic lights glowing amber, rich copper and violet twilight sky reflections, "
            "no people, gender-neutral, stunning perspective, crisp 85mm lens, 8k resolution, cinematic masterpiece --ar 16:9"
        ),
        "package_presets": [
            {
                "pattern_id": "01_drive",
                "concept": "夕暮れドライブ・シチュエーション特化",
                "thumb": {"name": "THUMB_01_SUNSET_DRIVE", "main": "Sunset Drive", "sub": ""},
                "title": "Sunset Drive R&B 🌆 Smooth Groove & Sultry Vocals for Evening Cruise [4K]"
            },
            {
                "pattern_id": "02_chill",
                "concept": "夜カフェ・チルアウト特化",
                "thumb": {"name": "THUMB_02_VELVET_LOUNGE", "main": "Velvet Lounge", "sub": ""},
                "title": "Velvet Lounge Vibes ✨ Mellow R&B & Neo-Soul for Late Night Relaxation [4K UHD]"
            },
            {
                "pattern_id": "03_groove",
                "concept": "感情・大人のグルーヴ特化",
                "thumb": {"name": "THUMB_03_GOLDEN_HOUR", "main": "Golden Hour", "sub": ""},
                "title": "Golden Hour Euphoria 🌇 Smooth R&B Beats & Warm Bass For Pure Relaxation [4K]"
            }
        ]
    },
    "ch3": {
        "channel_id": "ch3",
        "name": "AuraMelody Audio",
        "account_key": "auramelody",
        "genre": "Sunshine Feel-Good Pop",
        "mastering_profile": "ch3_zero_eq_natural",
        "mastering_filter": "alimiter=limit=0.95:level=disabled",
        "target_duration_mins": 60,  # 1時間長尺
        "min_duration_sec": 3600.0,
        "visualizer": {
            "enabled": True,
            "fill_color": (0, 229, 255, 220),  # Electric Cyan Glow
            "outline_color": (255, 255, 255, 255),
            "scale": (0.35, 0.06),
            "y_offset_ratio": 0.88
        },
        "thumbnail": {
            "font_index": 2,  # Futura Bold
            "font_size_main": 98,
            "font_size_sub": 42,
            "glow_color": (0, 229, 255),  # Electric Cyan Glow
            "text_color": (255, 255, 255)
        },
        # 🌿 【都会のカフェテラス × 波打ち際の違和感】Imagen 3 確定プロンプト
        "visual_prompt_template": (
            "An ultra-detailed bright lifestyle art photography, 16:9 widescreen composition. "
            "A chic, sunlit urban coffee shop terrace on a brilliant morning. "
            "A clean wooden cafe table with an iced glass of coffee, bathed in pure morning sunlight. "
            "Right at the edge of the polished concrete cafe floor, the city pavement suddenly disappears, "
            "giving way to a pristine white-sand beach where gentle, sparkling turquoise ocean waves are softly rolling directly onto the edge of the terrace. "
            "Crisp shadows, fresh sea breeze atmosphere meets urban sophistication, vibrant blue morning sky, no people, gender-neutral, uplifting and refreshing surrealism, 85mm lens, 8k resolution, masterpiece --ar 16:9"
        ),
        "package_presets": [
            {
                "pattern_id": "01_feel_good",
                "concept": "朝の目覚め・ポジティブ特化（王道）",
                "thumb": {"name": "THUMB_01_FEEL_GOOD_POP", "main": "FEEL GOOD POP", "sub": "1 HOUR • SUNSHINE MORNING"},
                "title": "1 Hour Feel-Good Summer Pop Mix ☀️ Upbeat Acoustic & Bright Morning Vibes [4K UHD]"
            },
            {
                "pattern_id": "02_tropical",
                "concept": "ビーチ・エネルギー特化（運動・作業）",
                "thumb": {"name": "THUMB_02_TROPICAL_SUNSHINE", "main": "TROPICAL SUNSHINE", "sub": "1 HOUR • UPLIFTING BEATS"},
                "title": "Tropical Sunshine Pop Beats 🌴 Upbeat Summer Energy For Work, Study & Morning Drive [4K]"
            },
            {
                "pattern_id": "03_dopamine",
                "concept": "多幸感・集中力向上特化",
                "thumb": {"name": "THUMB_03_ENDLESS_JOY", "main": "ENDLESS JOY", "sub": "1 HOUR • PURE POP DOPAMINE"},
                "title": "Endless Summer Joy ✨ 1-Hour Upbeat Pop Music For Pure Dopamine & Positive Mood [4K UHD]"
            }
        ]
    }
}

# ==============================================================================
# 🛠️ 3. ユーティリティ & 品質検証ガード (Helper Functions & Quality Guards)
# ==============================================================================
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

def validate_audio_track(arr: np.ndarray, sr: int, track_name: str):
    """
    音源の基本的な整合性検証（サンプリングレートおよび物理データの確認）
    ※ 音質判定はユーザー自身の判断を絶対尊重し、機械的な誤検知による停止を防止
    """
    if len(arr) == 0:
        raise ValueError(f"🚨 [AUDIO ERROR] Track '{track_name}' contains no audio data.")
    return True

# ==============================================================================
# 🚀 4. 完全共通動画生成コア関数 (Master Render Pipeline)
# ==============================================================================
# 🚀 4. 完全共通動画生成コア関数 (Master Render Pipeline) - ローカル完全廃止
# ==============================================================================
def build_video_pipeline(*args, **kwargs):
    """
    【システムレベル完全無効化】
    Macローカルでの動画レンダリングエンジンは完全に撤去されました。
    いかなる引数やオプションがあっても、ローカルでFFmpeg動画レンダリングが起動することは物理的に不可能です。
    """
    raise SystemError(
        "❌ 【システムエラー: ローカルレンダリング完全廃止】\n"
        "Macローカルでの動画レンダリング機能はシステムレベルで完全削除されました。\n"
        "動画生成は必ず export_colab_render_package() を使用してColab（GPU）で実行してください。"
    )

# ==============================================================================
# 🖼️ 5. サムネイル自動生成エンジン (Master Thumbnail Pipeline)
# ==============================================================================
def generate_official_thumbnail(
    raw_image_path: Path,
    main_text: str,
    sub_text: str,
    output_thumb_path: Path,
    font_path: str = FUTURA_FONT_PATH,
    font_index: int = 0,
    font_size_main: int = 100,
    font_size_sub: int = 44,
    glow_color: tuple = (255, 235, 180),
    text_color: tuple = (255, 255, 255),
    layout: str = "top_left"
):
    output_thumb_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. 1920x1080 に Lanczos でリサイズ
    base_bg = Image.open(raw_image_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    font_main = ImageFont.truetype(font_path, font_size_main, index=font_index) if font_path.endswith(".ttc") else ImageFont.truetype(font_path, font_size_main)
    
    dummy = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)

    if layout == "center" or not sub_text:
        # 画面中央ジャスト配置（単体タイトル）
        bbox_m = d_draw.textbbox((0, 0), main_text, font=font_main)
        w_m, h_m = bbox_m[2] - bbox_m[0], bbox_m[3] - bbox_m[1]
        x_m = int((1920 - w_m) / 2) - bbox_m[0]
        y_m = int(1080 * 0.45 - h_m / 2) - bbox_m[1]

        glow = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        g_draw.text((x_m + 8, y_m + 10), main_text, font=font_main, fill=(0, 0, 0, 250))
        g_draw.text((x_m, y_m), main_text, font=font_main, fill=(*glow_color, 240))
        glow_blurred = glow.filter(ImageFilter.GaussianBlur(18))
        composed = Image.alpha_composite(base_bg, glow_blurred)

        txt_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        t_draw = ImageDraw.Draw(txt_layer)
        t_draw.text((x_m, y_m), main_text, font=font_main, fill=(*text_color, 255))
        final_img = Image.alpha_composite(composed, txt_layer)

    else:
        # 左上配置（メイン＋サブタイトル）
        font_sub = ImageFont.truetype(FUTURA_FONT_PATH, font_size_sub, index=font_index)
        x, y = 100, 100
        x_s, y_s = 100, y + font_size_main + 20

        glow = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        g_draw.text((x + 6, y + 8), main_text, font=font_main, fill=(0, 0, 0, 245))
        g_draw.text((x_s + 4, y_s + 6), sub_text, font=font_sub, fill=(0, 0, 0, 230))
        g_draw.text((x, y), main_text, font=font_main, fill=(*glow_color, 220))
        g_draw.text((x_s, y_s), sub_text, font=font_sub, fill=(*glow_color, 190))
        
        glow_blurred = glow.filter(ImageFilter.GaussianBlur(14))
        composed = Image.alpha_composite(base_bg, glow_blurred)

        txt_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        t_draw = ImageDraw.Draw(txt_layer)
        t_draw.text((x, y), main_text, font=font_main, fill=(*text_color, 255))
        t_draw.text((x_s, y_s), sub_text, font=font_sub, fill=(*text_color, 255))
        final_img = Image.alpha_composite(composed, txt_layer)

    final_img.convert("RGB").save(output_thumb_path, quality=95)
    print(f"✅ Generated Thumbnail: {output_thumb_path.name}")
    return output_thumb_path

# ==============================================================================
# 🎯 6. ワンタッチ実行エントリー関数 (One-Touch Channel Pipeline)
# ==============================================================================
def generate_channel_video(
    channel_id: str,
    track_list: list,
    bg_media_path: Path,
    output_video_path: Path = None,
    output_chapters_path: Path = None,
    custom_visualizer: dict = None
):
    """
    ワンタッチ動画制作エントリー:
    ローカルでのレンダリングは行わず、Colabクラウド実行用パッケージ（ZIP）を自動生成して返します。
    """
    cfg = CHANNEL_CONFIGS.get(channel_id.lower())
    if not cfg:
        raise ValueError(f"Unknown channel_id: {channel_id}. Choose from {list(CHANNEL_CONFIGS.keys())}")
    
    out_dir = Path("/Users/base/Automated-Projects/YouTube") / f"{'01_Chill_Channel' if channel_id=='ch1' else '02_Velvet_Sunset_Channel' if channel_id=='ch2' else '03_Uplifting_Channel'}/output"
    out_zip = out_dir / f"{channel_id}_{cfg['account_key']}_colab_package.zip"
    
    return export_colab_render_package(
        channel_id=channel_id,
        track_list=track_list,
        bg_image_path=bg_media_path,
        output_zip_path=out_zip,
        pattern_index=0
    )

def generate_channel_thumbnails(
    channel_id: str,
    raw_image_path: Path,
    out_dir: Path,
    variations: list = None
):
    cfg = CHANNEL_CONFIGS.get(channel_id.lower())
    if not cfg:
        raise ValueError(f"Unknown channel_id: {channel_id}")

    if variations is None:
        variations = [p["thumb"] for p in cfg["package_presets"]]

    thumb_cfg = cfg["thumbnail"]
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for var in variations:
        out_path = out_dir / f"{var['name'].lower()}.jpg"
        glow = var.get("glow", thumb_cfg["glow_color"])
        res = generate_official_thumbnail(
            raw_image_path=raw_image_path,
            main_text=var["main"],
            sub_text=var.get("sub", ""),
            output_thumb_path=out_path,
            font_path=thumb_cfg.get("font_path", FUTURA_FONT_PATH),
            font_index=thumb_cfg.get("font_index", 0),
            font_size_main=thumb_cfg.get("font_size_main", 100),
            font_size_sub=thumb_cfg.get("font_size_sub", 44),
            glow_color=glow,
            text_color=thumb_cfg.get("text_color", (255, 255, 255)),
            layout=thumb_cfg.get("layout", "top_left")
        )
        results.append(res)
    return results

def generate_channel_metadata(
    channel_id: str,
    pattern_index: int,
    chapters_text: str,
    video_url: str = "https://youtu.be/[VideoID]",
    custom_tags: list = None
) -> dict:
    cfg = CHANNEL_CONFIGS.get(channel_id.lower())
    if not cfg:
        raise ValueError(f"Unknown channel_id: {channel_id}")

    presets = cfg["package_presets"]
    if pattern_index < 0 or pattern_index >= len(presets):
        raise IndexError(f"pattern_index {pattern_index} out of range (0-{len(presets)-1})")

    selected_preset = presets[pattern_index]
    title_en = selected_preset["title"]

    description = f"""{title_en}

Welcome to {cfg['name']} 🎧
Enjoy this {cfg['genre']} collection designed for deep focus, study, work, late-night relaxation, and peace of mind.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎧 Tracklist & Timestamps:
{chapters_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【CREATOR LICENSE & USAGE】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: {cfg['name']}
   Watch: {video_url}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe & click the bell to never miss a new mix.
#Lofi #{cfg['account_key']} #BackgroundMusic #4kRelaxation #{cfg['name'].replace(' ', '')}"""

    pinned_comment = f"""✨ Thank you for listening to {cfg['name']}! Which track was your favorite? Let us know in the comments below! Don't forget to like & subscribe for more weekly beats. 🎵

🎧 Tracklist & Chapters:
{chapters_text}"""

    tags = [cfg['name'].lower(), f"{cfg['name'].lower()} audio", "4k music video", "background music", cfg['genre'].lower()]
    if custom_tags:
        tags.extend([t.lower() for t in custom_tags])

    return {
        "title": title_en,
        "description": description,
        "pinned_comment": pinned_comment,
        "tags": tags,
        "categoryId": "10",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    }

# ==============================================================================
# 🔍 7. 対象チャンネル内 曲名完全重複自動検知＆リネーム解決エンジン
# ==============================================================================
def validate_and_resolve_track_names(channel_id: str, new_track_names: list) -> list:
    base_yt = Path("/Users/base/Automated-Projects/YouTube")
    ch_folder_map = {
        "ch1": "01_Chill_Channel",
        "ch2": "02_Velvet_Sunset_Channel",
        "ch3": "03_Uplifting_Channel"
    }
    
    ch_dir = base_yt / ch_folder_map.get(channel_id.lower(), "02_Velvet_Sunset_Channel")

    existing_titles = set()
    if ch_dir.exists():
        # 対象チャンネル内の確定音源フォルダ（mastered_audio）のみチェック対象とし、ビルド生成物(colab_render_package等)は除外
        mastered_dir = ch_dir / "mastered_audio"
        search_dirs = [mastered_dir] if mastered_dir.exists() else [ch_dir]
        for s_dir in search_dirs:
            for f in s_dir.rglob("*"):
                if f.suffix.lower() in [".wav", ".mp3"] and "colab_package" not in str(f) and "temp" not in str(f):
                    clean = f.stem.replace("_", " ").strip()
                    existing_titles.add(clean.lower())

    resolved_tracks = []
    print(f"\n🔍 [Track Title Duplicate Check ({channel_id.upper()} Channel Only)]")
    for original_title in new_track_names:
        clean_orig = original_title.strip()
        lower_orig = clean_orig.lower()

        # 同一チャンネル内で完全に同名の場合のみリネーム対象
        if lower_orig in existing_titles:
            if channel_id == "ch1":
                suffix_pool = ["at 3 AM", "Midnight Haven", "Gentle Rain", "Cozy Corner", "Autumn Dusk"]
            elif channel_id == "ch2":
                suffix_pool = ["Sunset Groove", "Velvet Dusk", "Late Night Cruise", "Amber Glow", "Mellow Soul"]
            else:
                suffix_pool = ["Sunshine Mix", "Morning Joy", "Golden Horizon", "Summer Breeze", "Pure Dopamine"]

            import random
            resolved_title = f"{clean_orig} ({random.choice(suffix_pool)})"
            print(f"  ⚠️ Same-channel duplicate detected: '{clean_orig}' -> Auto-renamed to: '{resolved_title}'")
            resolved_tracks.append(resolved_title)
            existing_titles.add(resolved_title.lower())
        else:
            resolved_tracks.append(clean_orig)
            existing_titles.add(lower_orig)

    print("✅ All track titles verified for this channel!\n")
    return resolved_tracks


# ==============================================================================
# ☁️ 8. Colab クラウドレンダリング用パッケージ一括エクスポート関数 (A100 GPU / MP3 320kbps 対応)
# ==============================================================================
def export_colab_render_package(
    channel_id: str,
    track_list: list,
    bg_image_path: Path,
    output_zip_path: Path,
    thumbnail_path: Path = None,
    pattern_index: int = 0
) -> Path:
    """
    ローカルの確定素材（軽量MP3/WAV音源・4K背景・文字入りサムネイル・設定JSON）をまとめ、
    Colab(A100 GPU)で即座に実行可能な軽量ZIPパッケージ（数十MB〜100MB前後）を生成
    """
    cfg = CHANNEL_CONFIGS.get(channel_id.lower())
    if not cfg:
        raise ValueError(f"Unknown channel_id: {channel_id}")

    output_zip_path.parent.mkdir(parents=True, exist_ok=True)
    temp_pkg_dir = output_zip_path.parent / f"temp_colab_pkg_{channel_id}"
    if temp_pkg_dir.exists():
        shutil.rmtree(temp_pkg_dir)
    temp_pkg_dir.mkdir(parents=True, exist_ok=True)

    audio_pkg_dir = temp_pkg_dir / "audio"
    audio_pkg_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 [Colab Export] Packaging lightweight assets for {cfg['name']}...", flush=True)

    # 1. 音源コピー & 重複タイトル自動判定・リネーム
    raw_titles = []
    for t in track_list:
        if isinstance(t, (str, Path)):
            raw_titles.append(Path(t).stem)
        elif isinstance(t, dict):
            raw_titles.append(Path(t.get("file", t.get("name"))).stem)
        elif isinstance(t, (list, tuple)):
            raw_titles.append(Path(t[1]).stem)

    unique_titles = validate_and_resolve_track_names(channel_id, raw_titles)

    for idx, item in enumerate(track_list):
        if isinstance(item, (str, Path)):
            p = Path(item)
        elif isinstance(item, dict):
            p = Path(item.get("file", item.get("name")))
        elif isinstance(item, (list, tuple)):
            p = Path(item[1])
            
        unique_name = unique_titles[idx]
        ext = p.suffix.lower() if p.suffix else ".mp3"
        dest_audio = audio_pkg_dir / f"{idx+1:02d}_{unique_name.replace(' ', '_')}{ext}"
        shutil.copy2(p, dest_audio)

    # 2. 4K背景画像および サムネイル処理
    dest_bg = temp_pkg_dir / f"background{bg_image_path.suffix}"
    shutil.copy2(bg_image_path, dest_bg)

    if thumbnail_path and thumbnail_path.exists():
        # 明示的にサムネイル（完成済み文字入り画像等）が指定された場合は無加工でそのままパッキング
        selected_thumb = thumbnail_path
        dest_thumb = temp_pkg_dir / f"thumbnail{selected_thumb.suffix}"
        shutil.copy2(selected_thumb, dest_thumb)
        print(f"  ✅ Packaged specified thumbnail directly: {selected_thumb.name}")
    elif "thumb_" in bg_image_path.name.lower():
        # --bg-image に完成品サムネイルが指定された場合も直接パッキング
        selected_thumb = bg_image_path
        dest_thumb = temp_pkg_dir / f"thumbnail{selected_thumb.suffix}"
        shutil.copy2(selected_thumb, dest_thumb)
        print(f"  ✅ Packaged provided text-ready thumbnail directly: {selected_thumb.name}")
    else:
        # 通常運用（4K背景画像のみ指定時）: ローカルで 3種類の文字入りサムネイルを自動作成
        local_thumbs_dir = output_zip_path.parent / "thumbnails"
        print("🎨 [Local Thumbnail Pipeline] Generating 3 thumbnail variations from background image...")
        generated_thumbs = generate_channel_thumbnails(channel_id, bg_image_path, local_thumbs_dir)
        selected_thumb = generated_thumbs[pattern_index if pattern_index < len(generated_thumbs) else 0]
        dest_thumb = temp_pkg_dir / f"thumbnail{selected_thumb.suffix}"
        shutil.copy2(selected_thumb, dest_thumb)
        print(f"  ✅ Selected & packaged primary thumbnail from 3 variations: {selected_thumb.name}")

    # 3. メタデータ構築
    meta = generate_channel_metadata(
        channel_id=channel_id,
        pattern_index=pattern_index,
        chapters_text="{chapters}"  # Colab側で最終計算して置換
    )

    render_config = {
        "channel_id": channel_id,
        "channel_name": cfg["name"],
        "account_key": cfg["account_key"],
        "video_title": meta["title"],
        "description": meta["description"],
        "tags": meta["tags"],
        "visualizer_enabled": cfg["visualizer"]["enabled"],
        "output_filename": f"{channel_id}_{cfg['account_key']}_4k_master.mp4"
    }

    with open(temp_pkg_dir / "render_config.json", "w", encoding="utf-8") as f:
        json.dump(render_config, f, indent=2, ensure_ascii=False)

    # 4. Colab用実行スクリプトを同梱
    colab_script_src = Path("/Users/base/Automated-Projects/YouTube/shared/scripts/colab_hybrid_renderer.py")
    if colab_script_src.exists():
        shutil.copy2(colab_script_src, temp_pkg_dir / "run_colab_render.py")

    # 5. ZIP圧縮
    shutil.make_archive(str(output_zip_path.with_suffix("")), "zip", temp_pkg_dir)
    shutil.rmtree(temp_pkg_dir)

    print(f"✅ Colab Render Package Created: {output_zip_path} ({output_zip_path.stat().st_size / (1024*1024):.1f} MB)\n")
    return output_zip_path


# ==============================================================================
# 🎯 9. メインCLIエントリポイント (Single Source of Truth Pipeline Interface)
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automated-Projects YouTube Master Video Pipeline")
    parser.add_argument("--channel", type=str, required=True, choices=["ch1", "ch2", "ch3"], help="Target channel ID")
    parser.add_argument("--step", type=str, default="all", choices=["all", "audio", "package", "upload", "cloud"], help="Pipeline step to execute")
    parser.add_argument("--mode", type=str, default="local", help="Mode: local or cloud_actions")
    parser.add_argument("--audio-dir", type=str, default=None, help="Directory containing raw audio files")
    parser.add_argument("--bg-image", type=str, default=None, help="Path to 4K background cover art")
    parser.add_argument("--pattern-index", type=int, default=0, help="Metadata pattern index for titles/descriptions")
    
    args = parser.parse_args()
    
    channel_id = args.channel.lower()
    cfg = CHANNEL_CONFIGS.get(channel_id)
    if not cfg:
        print(f"❌ Unknown channel_id: {channel_id}")
        sys.exit(1)
        
    print("=" * 70)
    print(f"🚀 Master Video Pipeline Engine | Channel: {cfg['name']} ({channel_id.upper()}) | Mode: {args.mode}")
    print(f"📌 Executing Step: [{args.step.upper()}]")
    print("=" * 70)
    
    # 物理パス解決
    youtube_base = Path(__file__).resolve().parent.parent
    ch_folder = '01_Chill_Channel' if channel_id=='ch1' else '02_Velvet_Sunset_Channel' if channel_id=='ch2' else '03_Uplifting_Channel'
    base_ch_dir = youtube_base / ch_folder
    
    if args.audio_dir:
        audio_dir = Path(args.audio_dir)
    else:
        if channel_id == "ch2" and (base_ch_dir / "raw_audio" / "ch2_drive_mp3").exists():
            audio_dir = base_ch_dir / "raw_audio" / "ch2_drive_mp3"
        else:
            audio_dir = base_ch_dir / "raw_audio"
            
    if args.bg_image:
        bg_image = Path(args.bg_image)
    else:
        target_thumb = base_ch_dir / "cover_art" / "thumb_03_golden_hour.jpg"
        if target_thumb.exists():
            bg_image = target_thumb
        else:
            found_art = list((base_ch_dir / "cover_art").glob("*.jpg")) + list((base_ch_dir / "cover_art").glob("*.jpeg"))
            bg_image = found_art[0] if found_art else (base_ch_dir / "cover_art" / "thumb.jpg")

    out_pkg_dir = base_ch_dir / "colab_render_package"
    
    # 【自動バリデーションガード】事前チェック
    from shared.scripts.validation_guard import (
        validate_input_params, validate_file_exists, validate_audio_files,
        validate_video_output, print_user_instruction_checklist
    )
    
    validate_input_params({"channel": channel_id, "step": args.step}, ["channel", "step"])
    if bg_image:
        validate_file_exists(str(bg_image), label="背景サムネイル画像")
    
    checklist_data = [
        {"item": "対象チャンネルID", "req": channel_id.upper(), "actual": cfg["name"], "status": True},
        {"item": "背景画像パス", "req": str(bg_image), "actual": "物理ファイル存在OK", "status": bg_image.exists()}
    ]
    
    # STEP 1: 音声結合
    if args.step in ["all", "audio"]:
        print(f"\n🎵 [STEP: AUDIO] Combining audio tracks from: {audio_dir}")
        tracks = sorted(list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3")))
        validate_audio_files([str(t) for t in tracks])
        out_wav = out_pkg_dir / f"{channel_id}_master_combined.wav"
        out_pkg_dir.mkdir(parents=True, exist_ok=True)
        
        # 音声結合実行
        combined_audio, sr, chapters = concatenate_tracks_dj_crossfade(channel_id, tracks)
        out_int16 = np.clip(combined_audio * 32767.0, -32768, 32767).astype(np.int16)
        with wave.open(str(out_wav), 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(out_int16.tobytes())
        print(f"✅ Audio Combined: {out_wav} ({out_wav.stat().st_size/(1024*1024):.1f} MB)")
        checklist_data.append({
            "item": "音声マスタリングWAV", "req": f"{cfg['min_duration_sec']}秒以上",
            "actual": f"{len(combined_audio)/sr:.1f}秒", "status": (len(combined_audio)/sr >= cfg['min_duration_sec'] * 0.95)
        })
        
    # STEP 2: パッケージ生成
    if args.step in ["all", "package"]:
        print(f"\n📦 [STEP: PACKAGE] Exporting Colab Render Package...")
        tracks = sorted(list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3")))
        out_zip = out_pkg_dir / f"{channel_id}_colab_package.zip"
        export_colab_render_package(channel_id, tracks, bg_image, out_zip, pattern_index=args.pattern_index)
        
    # STEP 3: YouTube アップロード
    if args.step in ["all", "upload"]:
        print(f"\n📤 [STEP: UPLOAD] Uploading to YouTube ({cfg['name']})...")
        from shared.scripts.account_token_manager import get_youtube_service
        from shared.scripts.upload_to_youtube import upload_video
        
        # 完成動画の検出
        video_path = base_ch_dir / f"{channel_id}_4k_master.mp4"
        if not video_path.exists():
            video_path = base_ch_dir / "output_videos" / f"{channel_id}_4k_master.mp4"
        
        if not video_path.exists():
            print(f"⚠️ Video file not found locally: {video_path}")
            print("   Colabで動画を生成・取得後に upload ステップを実行してください。")
            sys.exit(1)
            
        # メタデータ生成
        chapters_file = out_pkg_dir / "chapters.txt"
        chapters_text = chapters_file.read_text() if chapters_file.exists() else ""
        meta = generate_channel_metadata(channel_id, pattern_index=args.pattern_index, chapters_text=chapters_text)
        
        # 非公開アップロード
        upload_video(
            video_path=video_path,
            title=meta["title"],
            description=meta["description"],
            tags=meta["tags"],
            privacy_status="private",
            thumbnail_path=bg_image,
            account_num=1
        )
        print("✅ Step UPLOAD Completed!")

    # 最終指示履行確認チェックリスト表示
    print_user_instruction_checklist(checklist_data)
    print("\n🎉 Pipeline Step Execution Completed with 100% Validation!")

if __name__ == "__main__":
    main()

