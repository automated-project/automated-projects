# -*- coding: utf-8 -*-
import json

with open("/Users/base/Automated-Projects/YouTube/all_channels_current_metadata.json") as f:
    data = json.load(f)

for ch_name, vlist in data.items():
    print(f"\n==================== {ch_name} ====================")
    for i, v in enumerate(vlist):
        vid = v["id"]
        title = v["title"]
        dur = v["duration"]
        desc = v["description"]
        tags = v.get("tags", [])
        has_ts = ("00:00" in desc or "0:00" in desc)
        
        # Check summer or other seasonal words
        has_summer = ("summer" in title.lower() or "summer" in desc.lower() or any("summer" in t.lower() for t in tags))
        
        if ch_name == "Ch1 (Haven Chill)" and i >= 15:
            continue
        print(f"[{i+1}] ID: {vid} | Dur: {dur} | TS: {has_ts} | Summer: {has_summer}")
        print(f"    Title: {title}")
