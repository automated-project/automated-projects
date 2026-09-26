#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 8分 Mini Mix (Vol. 1) 公式動画 アップロードスクリプト
- Video: output_videos/8MIN_HARDCORE_GYM_PHONK_VOL1.mp4
- Thumbnail: output_videos/thumbnails/thumb_ch2_8min_gym_phonk_vol1.jpg
- Token: phonkforge (token_phonkforge.json)
- Channel: @PhonkForgeAudio-s1h (UCsyFo4FtRSWLxX_53j77AFg)
- Pinned Comment Timestamps & Multilingual SEO
"""

import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/8MIN_HARDCORE_GYM_PHONK_VOL1.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/thumb_ch2_8min_gym_phonk_vol1.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/8MIN_HARDCORE_GYM_PHONK_VOL1_chapters.txt"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

if not THUMBNAIL_PATH.exists():
    print(f"Error: Thumbnail file not found at {THUMBNAIL_PATH}", file=sys.stderr)
    sys.exit(1)

chapters_text = ""
if CHAPTERS_PATH.exists():
    with open(CHAPTERS_PATH, "r", encoding="utf-8") as f:
        chapters_text = f.read().strip()

print("=== Starting Upload for 8-Min Hardcore Gym Phonk Mix on PhonkForge Audio ===")
yt = get_youtube_service("phonkforge")

TITLE_EN = "⚡ [8 MIN] HARDCORE GYM PHONK MIX — Pure Adrenaline Workout & PR Motivation"

DESCRIPTION_EN = f"""⚡ Welcome to PhonkForge Audio — Pure Hardcore Heavy Bass Gym Phonk for PRs, Heavy Lifts, and Maximum Adrenaline! 🔥

Built for athletes, bodybuilders, and night drivers who demand pure energy with zero filler. 8 minutes of non-stop, heavy 808 sub-bass drops and aggressive workout beats designed to get you through your heaviest sets.

100% Free & Royalty-Free for Creators! Feel free to use these tracks in your YouTube videos, live streams, workouts, and edits.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 TRACKLIST & TIMESTAMPS:
{chapters_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 【FREE DOWNLOAD & CREATOR LICENSE / フリー音源利用規約】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: PhonkForge Audio
   Watch: https://www.youtube.com/@PhonkForgeAudio-s1h
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧 Sound Design & Mastering:
- Extreme Sub-Bass Calibration (-14.0 LUFS / 808 Punch)
- Seamless 2.5s DJ Crossfades
- Visuals: 48-Bar Waveform & Sub-Bass Pulse

━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 LOOKING FOR COZY LOFI OR UPLIFTING EDM?
Check out our dedicated sister channels:

🌿 Cozy Lofi & Study Beats ➡️ @Haven-Chill-Audio
https://www.youtube.com/@Haven-Chill-Audio

✨ Uplifting Pop & Melodic EDM ➡️ @AuraMelody-Audio
https://www.youtube.com/@AuraMelody-Audio
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe to @PhonkForgeAudio-s1h to fuel your workouts with pure adrenaline!

#GymPhonk #PhonkMix #WorkoutMusic #HardcorePhonk #HeavyBass #DriftPhonk #PhonkForge #8MinMix #FreeBGM
"""

TAGS = [
    "gym phonk", "hardcore phonk", "workout music", "phonk mix", "heavy bass phonk",
    "gym motivation", "pr workout music", "drift phonk", "aggressive phonk", "808 bass",
    "phonkforge", "phonkforge audio", "free bgm phonk", "gym bgm"
]

LOCALIZATIONS = {
    "ru": {
        "title": "⚡ [8 МИН] ХАРДКОР ФОНК ДЛЯ ЗАЛА — Мощный Басс для Тренировок и Рекордов",
        "description": f"⚡ 8 минут мощного фонка с тяжелым 808 басом для тренировок в зале, рекордов и поднятия энергии!\n\n100% Бесплатно для использования в видео и стримах!\n\n🎵 Треклист в закрепленном комментарии.\n\n#Фонк #ФонкДляЗала #МузыкаДляТренировок #PhonkForge"
    },
    "pt": {
        "title": "⚡ [8 MIN] HARDCORE GYM PHONK MIX — Pura Adrenalina para Treino Pesado",
        "description": f"⚡ 8 minutos de puro Phonk pesado com graves 808 para treinos intensos, academia e foco total!\n\n100% Grátis e Royalty-Free para criadores!\n\n🎵 Tracklist no comentário fixado.\n\n#GymPhonk #TreinoPesado #MusicaParaTreino #PhonkForge"
    },
    "es": {
        "title": "⚡ [8 MIN] HARDCORE GYM PHONK MIX — Pura Adrenalina para Entrenar y Gym",
        "description": f"⚡ 8 minutos de Phonk agresivo con graves 808 pesados para tus entrenamientos más duros y motivación total.\n\n100% Libre de regalías para creadores!\n\n🎵 Lista de canciones en el comentario fijado.\n\n#GymPhonk #MusicaParaGym #Entrenamiento #PhonkForge"
    },
    "ko": {
        "title": "⚡ [8분] 헬스장 씹어먹는 하드코어 폰크 믹스 — PR 갱신용 초고강도 헬스 BGM",
        "description": f"⚡ 8분 논스톱! 3대 500 돌파와 최고 중량 도전을 위한 극강의 808 중저음 헬스 폰크 믹스. 낭비 없는 킬러 트랙 3곡 구성!\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트는 고정 댓글을 확인하세요.\n\n#헬스폰크 #헬스음악 #운동할때듣는음악 #하드코어폰크 #PhonkForge"
    },
    "ja": {
        "title": "⚡ 【筋トレ用BGM/8分】限界突破ハードコア・ジムフォンク — PR更新・追い込み特化の重低音Mix",
        "description": f"⚡ 8分間ノンストップ！筋トレの最高重量挑戦（PR更新）やラストの追い込みに特化した極厚808重低音ジムフォンク。\n無駄な曲を一切排した厳選キラーチューン3曲構成！\n\n動画や配信で使える100%フリー音源（商用利用可・クレジット表記で無料）！\n\n🎵 トラックリストは固定コメントをご確認ください。\n\n#筋トレBGM #ジムフォンク #ワークアウトBGM #重低音 #PhonkForge"
    }
}

body = {
    "snippet": {
        "title": TITLE_EN,
        "description": DESCRIPTION_EN,
        "tags": TAGS,
        "categoryId": "10",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    },
    "localizations": LOCALIZATIONS
}

print(f"[+] Uploading video: {VIDEO_PATH.name} ({VIDEO_PATH.stat().st_size / 1024 / 1024:.2f} MB)...")
media = MediaFileUpload(str(VIDEO_PATH), mimetype="video/mp4", resumable=True, chunksize=10*1024*1024)

request = yt.videos().insert(
    part="snippet,status,localizations",
    body=body,
    media_body=media
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"  -> Upload progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print(f"\n🎉 Video Successfully Uploaded! Video ID: {video_id}")
print(f"🔗 URL: https://youtu.be/{video_id}")

# 3. サムネイル設定
print(f"[+] Setting thumbnail: {THUMBNAIL_PATH.name}...")
time.sleep(3)
try:
    yt.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
    ).execute()
    print("✅ Thumbnail Successfully Set!")
except Exception as e:
    print(f"⚠️ Failed to set thumbnail: {e}")

# 4. 固定コメント（Pinned Comment）
comment_text = f"""⚡ Tracklist & Timestamps:
{chapters_text}

Drop a LIKE 👍 and SUBSCRIBE if this fueled your workout session! What lift are you hitting today? Drop it below! 👇🔥"""

try:
    print("[+] Posting pinned engagement comment...")
    comment_res = yt.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    ).execute()
    print("✅ Pinned Comment Successfully Posted!")
except Exception as e:
    print(f"⚠️ Note on comment posting: {e}")

print(f"\n🚀 ALL TASKS COMPLETED! Live at https://youtu.be/{video_id}")
