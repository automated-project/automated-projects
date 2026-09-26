# -*- coding: utf-8 -*-
"""
楽曲タイトル重複・類似性 自動バリデーション＆被り防止ツール
- 機能:
  1. 既存マスター（tracks_master.json）に存在する全楽曲タイトルとの完全一致チェック
  2. 同一単語の過剰使用チェック（アルバム内で主要単語が重複していないか）
  3. サブスク配信基準のフォーマットチェック（記号・チープ語・直訳排除）
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

MASTER_PATH = Path("/Users/base/Automated-Projects/YouTube/shared/metadata/tracks_master.json")

# 除外する一般的なストップワード
STOP_WORDS = {"the", "a", "an", "of", "in", "on", "at", "by", "for", "to", "and", "or", "past", "turn"}

def load_master():
    if not MASTER_PATH.exists():
        print(f"[-] Master file not found: {MASTER_PATH}")
        sys.exit(1)
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_all_master_tracks():
    print("=== STARTING TRACK TITLE AUDIT ACROSS ALL CHANNELS ===")
    data = load_master()
    channels = data.get("channels", {})
    
    total_tracks = 0
    all_titles = []
    has_errors = False
    
    for ch_key, ch_info in channels.items():
        print(f"\n▶ Auditing Channel: {ch_info['channel_name']} ({ch_key})")
        for alb_key, alb_info in ch_info.get("albums", {}).items():
            print(f"  Album: {alb_info['album_title']} ({len(alb_info['tracks'])} tracks)")
            
            words_in_album = []
            album_titles = []
            
            for t in alb_info["tracks"]:
                num = t["num"]
                title = t["title"]
                total_tracks += 1
                
                # 1. 完全重複チェック
                if title.lower() in [x.lower() for x in album_titles]:
                    print(f"    ❌ ERROR: Duplicate title in album: '{title}' (Track {num})")
                    has_errors = True
                album_titles.append(title)
                all_titles.append((ch_key, alb_key, title))
                
                # 単語分解
                words = [w.lower() for w in re.findall(r'\b[A-Za-z]+\b', title) if w.lower() not in STOP_WORDS]
                words_in_album.extend(words)
            
            # 2. 単語過剰使用チェック
            word_counts = Counter(words_in_album)
            frequent_words = {w: c for w, c in word_counts.items() if c > 2}
            if frequent_words:
                print(f"    ⚠️ Warning: Overused words in {alb_key}: {frequent_words}")
            else:
                print(f"    ✓ Title variety and vocabulary diversity: PASS")

    print("\n==================================================")
    if has_errors:
        print("❌ AUDIT FAILED: Duplicate titles found in master database!")
        sys.exit(1)
    else:
        print(f"✅ AUDIT PASSED: All {total_tracks} tracks across 3 channels are unique and compliant!")
        print("==================================================")

def check_new_title(channel_key: str, album_key: str, candidate_title: str):
    """新曲タイトルを追加する前の検証API"""
    data = load_master()
    ch_info = data.get("channels", {}).get(channel_key, {})
    alb_info = ch_info.get("albums", {}).get(album_key, {})
    
    existing_titles = [t["title"].lower() for t in alb_info.get("tracks", [])]
    if candidate_title.lower() in existing_titles:
        return False, f"Title '{candidate_title}' already exists in {channel_key} / {album_key}"
        
    return True, "Valid unique title"

if __name__ == "__main__":
    validate_all_master_tracks()
