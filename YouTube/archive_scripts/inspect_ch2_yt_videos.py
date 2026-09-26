# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) の公開中全動画のメタデータとチャプターを確認するスクリプト
"""
import sys
import json
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("phonkforge")
res = yt.channels().list(mine=True, part="contentDetails").execute()
uploads_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

pl_items = []
next_token = None
while True:
    r = yt.playlistItems().list(playlistId=uploads_id, part="snippet,contentDetails", maxResults=50, pageToken=next_token).execute()
    pl_items.extend(r.get("items", []))
    next_token = r.get("nextPageToken")
    if not next_token:
        break

for item in pl_items:
    vid = item["contentDetails"]["videoId"]
    v_res = yt.videos().list(id=vid, part="snippet,contentDetails").execute()
    if v_res.get("items"):
        s = v_res["items"][0]["snippet"]
        dur = v_res["items"][0]["contentDetails"]["duration"]
        print(f"\n==========================================")
        print(f"ID: {vid} | Duration: {dur}")
        print(f"Title: {s['title']}")
        lines = s["description"].split("\n")
        ts_lines = [l for l in lines if ("00:00" in l or "0:00" in l or "02:" in l or "03:" in l)]
        if ts_lines:
            print("Timestamps:")
            for tl in ts_lines[:5]:
                print(f"  {tl}")
            if len(ts_lines) > 5:
                print(f"  ... (+ {len(ts_lines)-5} more)")
