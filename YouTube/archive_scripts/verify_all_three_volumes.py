# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("auramelody")
for vid, name in [("o8ygRO9KVuQ", "Vol. 1"), ("Tamf2pVElJU", "Vol. 2"), ("EWtj0yBMsrs", "Vol. 3")]:
    res = yt.videos().list(id=vid, part="snippet").execute()
    item = res["items"][0]["snippet"]
    lines = item["description"].split("\n")
    ts_sample = [l for l in lines if ("00:00" in l or "02:" in l or "03:" in l or "05:" in l)][:4]
    title = item["title"]
    print(f"\n=== {name} ({vid}) ===")
    print(f"Title: {title}")
    print("Top Timestamps:")
    for ts in ts_sample:
        print(f"  {ts}")
