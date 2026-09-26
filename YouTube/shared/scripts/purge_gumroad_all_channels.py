# -*- coding: utf-8 -*-
"""
全チャンネル・全動画からGumroad関連リンク・不要記述を一括完全削除するスクリプト
"""
import os
import sys
import re
from pathlib import Path

# YouTubeディレクトリをパスに追加
sys.path.insert(0, "/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service, CHANNELS

def clean_description(desc: str) -> tuple[str, bool]:
    lines = desc.split("\n")
    new_lines = []
    modified = False
    
    for line in lines:
        lower = line.lower()
        if (
            "gumroad.com" in lower
            or "gumroad" in lower
            or "official store" in lower
            or "💎 need 24-bit" in lower
            or "get full audio / wav pack" in lower
            or "commercial license" in lower and "gumroad" in lower
        ):
            modified = True
            continue
        new_lines.append(line)
        
    cleaned = "\n".join(new_lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    
    return cleaned, modified

def main():
    target_keys = ["komorebi", "phonkforge", "auramelody"]
    total_updated = 0
    total_checked = 0
    
    for key in target_keys:
        channel_name = CHANNELS[key]["name"]
        print(f"\n==========================================")
        print(f"Scanning Channel: {key} ({channel_name})")
        print(f"==========================================")
        try:
            yt = get_youtube_service(key)
            
            # チャンネルのアップロードプレイリストIDを取得
            ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
            if not ch_res.get("items"):
                print("  No channel items found.")
                continue
                
            uploads_playlist_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # プレイリストから全動画を取得
            videos = []
            next_page_token = None
            while True:
                pl_res = yt.playlistItems().list(
                    part="snippet",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                for item in pl_res.get("items", []):
                    vid = item["snippet"]["resourceId"]["videoId"]
                    title = item["snippet"]["title"]
                    videos.append((vid, title))
                    
                next_page_token = pl_res.get("nextPageToken")
                if not next_page_token:
                    break
                    
            print(f"  Found {len(videos)} videos on this channel.")
            
            for vid, title in videos:
                total_checked += 1
                v_res = yt.videos().list(part="snippet", id=vid).execute()
                if not v_res.get("items"):
                    continue
                    
                snippet = v_res["items"][0]["snippet"]
                old_desc = snippet.get("description", "")
                
                cleaned_desc, modified = clean_description(old_desc)
                
                if modified or (cleaned_desc != old_desc.strip() and "gumroad" in old_desc.lower()):
                    print(f"  [UPDATING] Video ID: {vid} | Title: {title[:40]}...")
                    snippet["description"] = cleaned_desc
                    yt.videos().update(
                        part="snippet",
                        body={"id": vid, "snippet": snippet}
                    ).execute()
                    total_updated += 1
                    print(f"    -> Gumroad links removed successfully.")
                else:
                    print(f"  [OK - Clean] Video ID: {vid} | Title: {title[:40]}...")
                    
        except Exception as e:
            print(f"  ❌ Error processing channel {key}: {e}")

    print(f"\n==========================================")
    print(f"COMPLETED: Checked {total_checked} videos across all channels. Updated {total_updated} videos.")
    print(f"==========================================")

if __name__ == "__main__":
    main()
