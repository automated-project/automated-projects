# -*- coding: utf-8 -*-
import json

with open("/Users/base/Automated-Projects/YouTube/all_channels_current_metadata.json") as f:
    data = json.load(f)

for ch_name, videos in data.items():
    print(f"\n==========================================")
    print(f"=== {ch_name} (Total: {len(videos)} videos) ===")
    print(f"==========================================")
    for i, v in enumerate(videos):
        desc = v.get("description", "")
        title = v.get("title", "")
        tags = v.get("tags", [])
        has_timestamps = ("00:00" in desc or "0:00" in desc)
        
        season_words = ["summer", "spring", "autumn", "fall", "winter", "夏", "春", "秋", "冬"]
        found_seasons = []
        for w in season_words:
            if w in title.lower() or w in desc.lower() or any(w in t.lower() for t in tags):
                found_seasons.append(w)
        
        # Check title uniqueness / duplicate
        vid_id = v.get("id")
        dur = v.get("duration")
        pub = v.get("publishedAt")
        print(f"[{i+1}] ID: {vid_id} | Dur: {dur} | Published: {pub[:10]}")
        print(f"    Title: {title}")
        print(f"    Timestamps: {'YES' if has_timestamps else 'NO'} | Seasons: {found_seasons if found_seasons else 'None'}")
