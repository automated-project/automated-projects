#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【共通モジュール④】YouTube Data API v3 非公開自動投稿 ＆ 多言語メタデータ・固定コメント自動投稿モジュール
- トークンファイルの外部参照、動画アップロード、サムネイル追加、非公開（private）設定を安全に実行
- 多言語タイトル・概要欄（localizations: ja, ko, es, pt, id）の自動登録
- 動画投稿完了後の【固定コメント (Pinned Comment)】自動投稿（英語タイムスタンプ ＋ 日英チャンネル登録・コメント促進メッセージ）
"""

import os
import sys
import json
import random
from pathlib import Path

YOUTUBE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(YOUTUBE_ROOT))

from shared.scripts.account_token_manager import get_youtube_service
from googleapiclient.http import MediaFileUpload

# コメント促進メッセージのローテーションリスト (英語 ＋ 日本語一言)
CALL_TO_ACTION_MESSAGES = [
    "✨ What is your favorite track in this mix? Let us know in the comments below! Don't forget to subscribe for more smooth music 🎵\nお気に入りの曲があればぜひコメントで教えてください！チャンネル登録もお待ちしています✨",
    "🎧 Thank you for listening! Leave a comment with your current mood, and subscribe to support the channel 💛\nご視聴ありがとうございます！感想や今の気分のコメント、チャンネル登録もお待ちしております！",
    "☕ Hope this music brings warmth to your day! Which track relaxed you the most? Subscribe for daily beats 🌙\nリラックスできましたか？ぜひお気に入りの曲をコメントしてくださいね！チャンネル登録もよろしくお願いします🎵"
]

def add_pinned_comment(yt, video_id: str, chapters_text: str):
    """
    動画に固定コメント（タイムスタンプ ＋ 日英エンゲージメント促進文）を投稿し、ピン留めする
    """
    cta_msg = random.choice(CALL_TO_ACTION_MESSAGES)
    
    comment_body = f"{cta_msg}\n\n⏱️ TIMESTAMPS:\n{chapters_text}"
    
    print(f"💬 Posting top-level comment to video {video_id}...")
    request_body = {
        'snippet': {
            'videoId': video_id,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': comment_body
                }
            }
        }
    }
    
    try:
        response = yt.commentThreads().insert(
            part='snippet',
            body=request_body
        ).execute()
        comment_id = response['id']
        print(f"✅ Top-level comment posted! ID: {comment_id}")
    except Exception as e:
        print(f"⚠️ Warning: Failed to post top-level comment: {e}")

def upload_video_to_youtube(
    account_key: str,
    video_path: Path,
    thumbnail_path: Path,
    title: str,
    description: str,
    tags: list,
    localizations: dict = None,
    chapters_text: str = "",
    privacy_status: str = "private"
) -> str:
    """
    指定されたアカウントキーのトークンを使って YouTube へ動画・サムネイルをアップロードし、
    多言語メタデータ登録および固定コメントの挿入を行う。
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not thumbnail_path.exists():
        raise FileNotFoundError(f"Thumbnail file not found: {thumbnail_path}")

    print(f"📤 Uploading video to YouTube ({account_key})...")
    yt = get_youtube_service(account_key)

    snippet_data = {
        'title': title,
        'description': description,
        'tags': tags,
        'categoryId': '10',  # Music
        'defaultLanguage': 'en',
        'defaultAudioLanguage': 'en'
    }

    body = {
        'snippet': snippet_data,
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }

    if localizations:
        body['localizations'] = localizations

    parts_to_insert = ['snippet', 'status']
    if localizations:
        parts_to_insert.append('localizations')

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype='video/mp4')
    request = yt.videos().insert(part=','.join(parts_to_insert), body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Uploading progress: {int(status.progress() * 100)}%", flush=True)

    video_id = response['id']
    print(f"🎉 Upload successful! Video ID: {video_id} (https://youtu.be/{video_id})")

    print("🖼️ Uploading thumbnail...")
    yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumbnail_path))).execute()
    print("✅ Thumbnail uploaded successfully!")

    if chapters_text:
        add_pinned_comment(yt, video_id, chapters_text)

    return video_id

if __name__ == "__main__":
    print("Standalone test mode for 04_youtube_upload.py")
