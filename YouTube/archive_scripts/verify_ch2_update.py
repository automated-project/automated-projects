# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("phonkforge")
for vid, name in [("z1jIjyKqNLM", "30M Gym Phonk"), ("4aJlGEfEI84", "1H Gym Phonk"), ("KfDXrQ2gmkM", "1H Car Phonk")]:
    res = yt.videos().list(id=vid, part="snippet,localizations").execute()
    item = res["items"][0]["snippet"]
    locs = res["items"][0].get("localizations", {})
    lines = item["description"].split("\n")
    ts_sample = [l for l in lines if ("00:00" in l or "02:" in l or "05:" in l)][:3]
    print(f"\n=== {name} ({vid}) ===")
    print(f"EN Title: {item['title']}")
    print(f"JA Title: {locs.get('ja', {}).get('title', 'N/A')}")
    print(f"KO Title: {locs.get('ko', {}).get('title', 'N/A')}")
    print("Sample Timestamps:")
    for ts in ts_sample:
        print(f"  {ts}")
