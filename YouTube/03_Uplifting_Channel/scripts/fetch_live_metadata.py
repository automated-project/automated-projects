# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio) ライブ配信メタデータ取得・一覧スクリプト
"""
import sys
import json
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("auramelody")

print("🔍 Fetching live broadcasts for AuraMelody Audio...")
try:
    # 1. アクティブなライブ配信を取得
    res = yt.liveBroadcasts().list(
        part="id,snippet,status,contentDetails",
        broadcastStatus="active"
    ).execute()
    
    items = res.get("items", [])
    if not items:
        # active がなければ upcoming や all も取得
        print("  No 'active' broadcast found. Checking 'all'...")
        res = yt.liveBroadcasts().list(
            part="id,snippet,status,contentDetails",
            mine=True,
            maxResults=10
        ).execute()
        items = res.get("items", [])
        
    print(f"Found {len(items)} broadcasts:")
    for b in items:
        b_id = b["id"]
        snippet = b.get("snippet", {})
        status = b.get("status", {})
        print(f"\n==================================================")
        print(f"📺 Broadcast ID: {b_id}")
        print(f"📌 LifeCycle Status: {status.get('lifeCycleStatus')}")
        print(f"🔒 Privacy: {status.get('privacyStatus')}")
        print(f"🏷️ Title: {snippet.get('title')}")
        print(f"📝 Description (Preview): {snippet.get('description', '')[:200]}...")
        print(f"🔗 Video URL: https://youtu.be/{b_id}")
        print(f"==================================================")
        
except Exception as e:
    print(f"❌ Error: {e}")
