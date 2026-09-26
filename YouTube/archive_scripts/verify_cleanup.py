# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

checks = [
    ("auramelody", ["o8ygRO9KVuQ", "Tamf2pVElJU", "pW2Zw1TvNXA", "4sDPJh25GGw"]),
    ("chill", ["2L0ppHOvE20", "H9xAE2j0JZM", "4J2cTvohlMs"]),
    ("phonk", ["z1jIjyKqNLM", "4aJlGEfEI84", "KfDXrQ2gmkM"])
]

for token, vids in checks:
    yt = get_youtube_service(token)
    print(f"\n=== Verification for [{token}] ===")
    for vid in vids:
        res = yt.videos().list(id=vid, part="snippet").execute()
        item = res["items"][0]["snippet"]
        title = item["title"]
        desc = item["description"]
        has_ts = ("00:00" in desc or "0:00" in desc)
        has_summer = ("summer" in title.lower() or "summer" in desc.lower() or any("summer" in t.lower() for t in item.get("tags", [])))
        print(f"ID: {vid}")
        print(f"  Title: {title}")
        print(f"  Timestamps: {has_ts} | SummerWord: {has_summer}")
