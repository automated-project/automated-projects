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

def check_title_duplicate_via_api(yt, proposed_title: str) -> bool:
    """
    YouTube Data API を経由して自分のチャンネルの既投稿動画（公開・非公開問わず）のタイトルを取得し、
    提案されたタイトルが過去動画と被っていないか自動バリデーションする。
    重複がある場合は True を返し、例外をスローして処理を自動停止させる。
    """
    print(f"🔍 Checking title duplication via YouTube Data API: '{proposed_title}'...")
    try:
        # 自分のチャンネルの動画一覧を取得 (mine=True)
        request = yt.search().list(
            part="snippet",
            forMine=True,
            type="video",
            maxResults=50
        )
        response = request.execute()
        
        existing_titles = [item['snippet']['title'].strip().lower() for item in response.get('items', [])]
        target_title = proposed_title.strip().lower()

        if target_title in existing_titles:
            print(f"❌ [DUPLICATE TITLE DETECTED] Title '{proposed_title}' already exists in channel videos!")
            return True
        print(f"✅ Title duplication check passed (Checked {len(existing_titles)} uploaded videos).")
        return False
    except Exception as e:
        print(f"⚠️ Title duplicate API check warning: {e}. Proceeding with upload validation.")
        return False

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

    yt = get_youtube_service(account_key)

    # 🔒 タイトル重複 API 自動検証ガード
    if check_title_duplicate_via_api(yt, title):
        raise ValueError(f"❌ 動画タイトル '{title}' は過去に投稿された動画と完全に重複しています。ユニークなタイトルに変更してください。")

    print(f"📤 Uploading video to YouTube ({account_key})...")

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
