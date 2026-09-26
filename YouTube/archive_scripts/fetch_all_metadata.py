# -*- coding: utf-8 -*-
"""
全チャンネル（Ch1: chill, Ch2: phonk, Ch3: uplifting）の公開動画一覧と現在のメタデータを取得するスクリプト
"""
import sys
import json
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

channels = {
    "Ch1 (Haven Chill)": "chill",
    "Ch2 (PhonkForge)": "phonk",
    "Ch3 (AuraMelody)": "uplifting"
}

results = {}

for ch_name, token_key in channels.items():
    print(f"=== Fetching videos for {ch_name} ({token_key}) ===")
    yt = get_youtube_service(token_key)
    # Get uploads playlist ID
    channels_res = yt.channels().list(mine=True, part="contentDetails").execute()
    uploads_playlist_id = channels_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    # Get all videos in uploads playlist
    playlist_items = []
    next_page_token = None
    while True:
        pl_res = yt.playlistItems().list(
            playlistId=uploads_playlist_id,
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        playlist_items.extend(pl_res.get("items", []))
        next_page_token = pl_res.get("nextPageToken")
        if not next_page_token:
            break
            
    video_ids = [item["contentDetails"]["videoId"] for item in playlist_items]
    print(f"Found {len(video_ids)} videos for {ch_name}")
    
    video_details = []
    # Fetch snippet and localizations for each video
    for vid in video_ids:
        v_res = yt.videos().list(
            id=vid,
            part="snippet,status,localizations,contentDetails"
        ).execute()
        if v_res.get("items"):
            item = v_res["items"][0]
            video_details.append({
                "id": vid,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "tags": item["snippet"].get("tags", []),
                "duration": item["contentDetails"]["duration"],
                "publishedAt": item["snippet"]["publishedAt"],
                "localizations": item.get("localizations", {})
            })
            
    results[ch_name] = video_details

output_path = Path("/Users/base/Automated-Projects/YouTube/all_channels_current_metadata.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nMetadata inspection saved to {output_path}")
