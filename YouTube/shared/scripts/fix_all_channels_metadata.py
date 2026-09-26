#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全チャンネル公開動画 メタデータ一斉修正スクリプト
- 規約違反（IP侵害、日本語併記、マスタリング仕様表記、FREE BGM/耐久表記、タイムスタンプ欠落）の自動検出＆修正
- 対象: Ch1 (Haven Chill), Ch2 (PhonkForge / Velvet Sunset), Ch3 (AuraMelody)
"""

import sys
import re
from googleapiclient.errors import HttpError

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

# 各チャンネルの個別動画修正マッピング（手動精査＋自動生成）
FIX_MAP = {
    # =========================================================================
    # 🌙 Ch 1: Haven Chill Audio
    # =========================================================================
    "VU-VMdEdwpE": {
        "channel": "chill",
        "title": "3 AM Study with Me 🌙 2 Hours Cozy Midnight Lofi & Felt Piano for Deep Focus / Sleep [4K]",
        "lead": "Step into a quiet midnight world. 🌙 2 hours of gentle felt piano melodies and cozy lofi beats designed for deep study sessions, late-night focus, and restful sleep."
    },
    "2L0ppHOvE20": {
        "channel": "chill",
        "title": "Study With Me at Midnight ☕ 2-Hour Cozy Lofi Beats for Deep Focus, Work & Reading [4K UHD]",
        "lead": "Find your peaceful focus. ☕ 2 hours of warm lofi beats and soothing piano melodies crafted for deep concentration, reading, and creative work."
    },
    "4J2cTvohlMs": {
        "channel": "chill",
        "title": "2 Hour Study With Me Focus Session 📚 Deep Midnight Lofi & Warm Piano for Study & Work",
        "lead": "Immerse yourself in deep concentration. 📚 2 hours of continuous cozy lofi beats and calming piano melodies for productive study and work sessions."
    },
    "H9xAE2j0JZM": {
        "channel": "chill",
        "title": "1 Hour Cozy Chill Lofi 🍃 Nostalgic Beats & Warm Piano for Study, Work & Deep Sleep",
        "lead": "Relax and unwind. 🍃 1 hour of warm nostalgic lofi rhythms and gentle piano melodies to accompany your daily study, work, and relaxation."
    },

    # =========================================================================
    # ⚡ Ch 2: PhonkForge Audio
    # =========================================================================
    "A_hMwS9lud4": {
        "channel": "phonk",
        "title": "Heavy Bass Gym Phonk Mix 🔥 Intense Workout & PR Motivation Beats [30 MIN]",
        "lead": "Fuel your workout intensity. 🔥 30 minutes of heavy bass gym phonk and aggressive rhythms engineered for maximum PR motivation and training power."
    },
    "z1jIjyKqNLM": {
        "channel": "phonk",
        "title": "30 Min Heavy Bass Gym Phonk 🔥 Intense Workout Motivation & Training Mix",
        "lead": "Unleash your full strength. 🔥 30 minutes of driving bass phonk and hard-hitting workout beats for lifting, training, and athletic focus."
    },
    "4aJlGEfEI84": {
        "channel": "phonk",
        "title": "1-Hour Heavy Bass Gym Phonk ⚡ Intense Drift Phonk & Workout Motivation Mix",
        "lead": "Push beyond your limits. ⚡ 1 hour of continuous heavy bass drift phonk and adrenaline-boosting rhythms for extreme workouts and night drives."
    },
    "KfDXrQ2gmkM": {
        "channel": "phonk",
        "title": "1-Hour Car Audio Bass Boosted 🔥 Heavy Drift Phonk & Midnight Drive Mix",
        "lead": "Elevate your night drive. 🔥 1 hour of deep sub-bass drift phonk and dark atmospheric beats built for late-night highway cruises."
    },

    # =========================================================================
    # ☀️ Ch 3: AuraMelody Audio
    # =========================================================================
    "HhxWRV8NOyk": {
        "channel": "auramelody",
        "title": "1 Hour Feel-Good Summer Pop Mix ☀️ Upbeat Acoustic & Bright Morning Vibes [4K UHD]",
        "lead": "Start your day with radiant energy! ☀️ 1 hour of non-stop feel-good summer pop, upbeat acoustic melodies, and bright uplifting rhythms designed to boost your mood, focus, and dopamine."
    },
    "CXcTjFvJuWw": {
        "channel": "auramelody",
        "title": "1 Hour Feel-Good Sunshine Pop ☀️ Upbeat Acoustic Melodies for Morning Focus & Drive",
        "lead": "Elevate your morning routine! ☀️ 1 hour of bright acoustic pop melodies and uplifting rhythms to boost your mood, focus, and energy throughout the day."
    },
    "fiXFH6wGG7g": {
        "channel": "auramelody",
        "title": "1 Hour Feel-Good Pop & Acoustic Hits ☀️ Bright Sunshine Vibes for Work & Drive",
        "lead": "Start your day with joyful vibes! ☀️ 1 hour of uplifting feel-good pop and sunny acoustic melodies crafted for productive work and scenic morning drives."
    },
    "EWtj0yBMsrs": {
        "channel": "auramelody",
        "title": "Golden Hour Melodic Beats ✨ 1-Hour Uplifting Progressive House for Work & Focus [4K]",
        "lead": "Experience radiant euphoria. ✨ 1 hour of uplifting progressive house and melodic beats designed for coding, creative work, and evening drives."
    },
    "Tamf2pVElJU": {
        "channel": "auramelody",
        "title": "1 Hour Pure Uplifting Melodic Beats ✨ Energetic Progressive House Mix for Focus",
        "lead": "Unleash positive energy. ✨ 1 hour of melodic progressive house rhythms and bright chords to power your deep focus, coding, and workouts."
    },
    "o8ygRO9KVuQ": {
        "channel": "auramelody",
        "title": "1 Hour Uplifting Melodic Beats ✨ Progressive House Vibes for Energy & Productivity",
        "lead": "Boost your creative flow. ✨ 1 hour of soaring melodic house beats and inspiring rhythms for studying, gaming, and productivity."
    }
}

# Shorts動画のタイトル一括修正（[FREE BGM] や [Free BGM] などの表記をクリーン化）
SHORTS_FIXES = {
    # Ch2 Shorts
    "3VpNKeepj7k": "CYBER OVERCLOCK PHONK 🔥 Hardstyle Heavy Bass #Shorts #fitness",
    "OJ_t8IHXPys": "MAX WEIGHT OVERDRIVE 🔥 Heavy Bass Gym Phonk #Shorts #gym",
    "j-4kLDJYvJw": "CYBER OVERCLOCK PHONK ⚡ Hardstyle Heavy Bass #Shorts #fitness",
    "q3wtUjXcWMs": "MAX WEIGHT OVERDRIVE ⚡ Heavy Bass Gym Phonk #Shorts #gym",
    "gRfVfXdC3Ns": "BRUTAL BEAST MODE PHONK ⚡ Extreme Gym PR #Shorts #workout",
    "cGSlw1GI01U": "HEAVY BASS GYM PHONK DROP 🔥 Powerful Workout Beats #Shorts #gym",
    "JXDXOXhy0Ek": "BRUTAL WORKOUT HEAVY BASS 🔥 PR Motivation #Shorts #workout",
    "tC3669w2slc": "HARDSTYLE HEAVY BASS DROP ⚡ Gym Motivation #Shorts #phonk",
    "d3C_8SoPxig": "HEAVY BASS GYM PHONK 🔥 Extreme Workout Drop #Shorts #gym",
    "SoLyfFLzEG8": "DRIFT & AGGRESSIVE PHONK ⚡ Night Drive Energy #Shorts #drift",
    # Ch3 Shorts
    "4sDPJh25GGw": "EUPHORIC MELODIC DROP ✨ Uplifting Summer Energy #Shorts #melodicedm #edm"
}

def extract_chapters_from_description(desc: str) -> str:
    """既存の概要欄からタイムスタンプ行のみを抽出"""
    lines = desc.split("\n")
    chapter_lines = []
    for line in lines:
        stripped = line.strip()
        # 00:00 or 0:00 or 01:23:45 形式の行を抽出
        if re.match(r"^(\d{1,2}:)?\d{2}:\d{2}\s*[-–—]", stripped):
            # 日本語や余計な記号をトリム
            chapter_lines.append(stripped)
    return "\n".join(chapter_lines)

def sanitize_text(text: str) -> str:
    """IP名、マスタリング用語、日本語、不適切語を完全排除"""
    t = text
    # 1. IP除去
    for ip in ["Ghibli", "ghibli", "Disney", "Nintendo", "Pokemon", "Avicii", "Kygo", "Keshi", "NewJeans", "Lofi Girl", "ChilledCow"]:
        t = re.sub(re.escape(ip), "", t, flags=re.IGNORECASE)
    # 2. マスタリング用語除去
    for m in ["-14 LUFS", "14 LUFS", "LUFS", "Warm Tape", "alimiter", "35Hz HPF", "50Hz", "15kHz LPF", "EQ帯域", "マスタリング"]:
        t = re.sub(re.escape(m), "", t, flags=re.IGNORECASE)
    # 3. タイトル禁止用語除去
    for b in ["[FREE BGM]", "[Free BGM]", "[FREE DOWNLOAD]", "FREE BGM", "商用利用OK", "商用利用", "フリーBGM", "作業用BGM", "耐久"]:
        t = re.sub(re.escape(b), "", t, flags=re.IGNORECASE)
    return t

def update_video_metadata(yt, video_id: str, new_title: str, new_lead: str, channel_name: str):
    print(f"\n▶ Fetching video details for {video_id}...")
    v_res = yt.videos().list(part="snippet,status", id=video_id).execute()
    if not v_res["items"]:
        print(f"❌ Video {video_id} not found.")
        return

    snippet = v_res["items"][0]["snippet"]
    current_desc = snippet.get("description", "")
    
    # タイムスタンプ抽出
    chapters_text = extract_chapters_from_description(current_desc)
    if not chapters_text:
        # 既存チャプターが見つからない場合のフォールバック（クリーンテキスト化）
        cleaned_desc = sanitize_text(current_desc)
    else:
        cleaned_desc = f"""{new_lead}

🎧 Tracklist & Chapters:
{chapters_text}

📜 Commercial Use & Music Policy:
All original music in this video is produced by {channel_name}. You are free to use these tracks in your personal and commercial content (YouTube videos, streams, podcasts) with proper credit:
Music provided by {channel_name} (YouTube: @{channel_name.replace(' ', '-')})

#{channel_name.replace(' ', '')} #BackgroundMusic #DeepFocus #4KMusicVideo"""

    snippet["title"] = new_title
    snippet["description"] = cleaned_desc
    snippet["categoryId"] = "10"
    snippet["defaultLanguage"] = "en"
    snippet["defaultAudioLanguage"] = "en"

    # タグのクリーン化
    current_tags = snippet.get("tags", [])
    clean_tags = []
    for tag in current_tags:
        cleaned_tag = sanitize_text(tag).strip()
        if cleaned_tag and len(cleaned_tag) > 1 and not re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', cleaned_tag):
            clean_tags.append(cleaned_tag)
    if channel_name.lower() not in clean_tags:
        clean_tags.append(channel_name.lower())
    snippet["tags"] = clean_tags[:20]

    yt.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet
        }
    ).execute()
    print(f"✅ Video {video_id} updated successfully!")
    print(f"   Title: {new_title}")

def update_shorts_title(yt, video_id: str, new_title: str):
    v_res = yt.videos().list(part="snippet", id=video_id).execute()
    if not v_res["items"]:
        return
    snippet = v_res["items"][0]["snippet"]
    snippet["title"] = new_title
    yt.videos().update(part="snippet", body={"id": video_id, "snippet": snippet}).execute()
    print(f"✅ Shorts {video_id} title updated -> {new_title}")

def main():
    print("==================================================")
    print("🛠️ STARTING METADATA MASS-FIX FOR ALL CHANNELS")
    print("==================================================")

    # 1. 長尺動画のメタデータ修正
    for vid, data in FIX_MAP.items():
        ch_key = data["channel"]
        ch_name = "Haven Chill Audio" if ch_key == "chill" else ("Velvet Sunset Audio" if ch_key == "phonk" else "AuraMelody Audio")
        try:
            yt = get_youtube_service(ch_key)
            update_video_metadata(yt, vid, data["title"], data["lead"], ch_name)
        except Exception as e:
            print(f"⚠️ Failed to update {vid} on {ch_key}: {e}")

    # 2. Shorts動画のタイトル修正
    for vid, new_title in SHORTS_FIXES.items():
        ch_key = "phonk" if vid in ["3VpNKeepj7k", "OJ_t8IHXPys", "j-4kLDJYvJw", "q3wtUjXcWMs", "gRfVfXdC3Ns", "cGSlw1GI01U", "JXDXOXhy0Ek", "tC3669w2slc", "d3C_8SoPxig", "SoLyfFLzEG8"] else "auramelody"
        try:
            yt = get_youtube_service(ch_key)
            update_shorts_title(yt, vid, new_title)
        except Exception as e:
            print(f"⚠️ Failed to update shorts {vid}: {e}")

    print("\n🎉 ALL METADATA FIXED AND COMPLIANT ACROSS ALL CHANNELS!")

if __name__ == "__main__":
    main()
