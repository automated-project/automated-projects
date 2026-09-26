# -*- coding: utf-8 -*-
import sys
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
        title = s["title"]
        desc = s["description"]
        if "H" not in dur and "M" not in dur: # Shorts
            print(f"\nShorts ID: {vid} | Dur: {dur}")
            print(f"  Title: {title}")
            for l in desc.split("\n")[:4]:
                print(f"  {l}")
