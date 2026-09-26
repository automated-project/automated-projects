# -*- coding: utf-8 -*-
"""
全チャンネル統合トークンマネージャー (3大音楽チャンネル + 社会科学アカウント完全対応)
チャンネルIDまたは識別名に応じた専用トークンを安全にロード・管理する
"""
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CREDENTIALS_DIR = Path(__file__).resolve().parent.parent / "credentials"

CHANNELS = {
    "phonkforge": {
        "channel_id": "UCsyFo4FtRSWLxX_53j77AFg",
        "name": "PhonkForge Audio",
        "token_file": CREDENTIALS_DIR / "token_phonkforge.json"
    },
    "phonk": {
        "channel_id": "UCsyFo4FtRSWLxX_53j77AFg",
        "name": "PhonkForge Audio",
        "token_file": CREDENTIALS_DIR / "token_phonkforge.json"
    },
    "gameverse": {
        "channel_id": "UC4Cjd2YmARE7rr59u1UqUbw",
        "name": "Haven Chill Audio",
        "token_file": CREDENTIALS_DIR / "token_gameverse.json"
    },
    "komorebi": {
        "channel_id": "UC4Cjd2YmARE7rr59u1UqUbw",
        "name": "Haven Chill Audio",
        "token_file": CREDENTIALS_DIR / "token_gameverse.json"
    },
    "chill": {
        "channel_id": "UC4Cjd2YmARE7rr59u1UqUbw",
        "name": "Haven Chill Audio",
        "token_file": CREDENTIALS_DIR / "token_gameverse.json"
    },
    "auramelody": {
        "channel_id": "UCldq7fhclKDAXUA1gLI0FRw",
        "name": "AuraMelody Audio",
        "token_file": CREDENTIALS_DIR / "token_auramelody.json"
    },
    "uplifting": {
        "channel_id": "UCldq7fhclKDAXUA1gLI0FRw",
        "name": "AuraMelody Audio",
        "token_file": CREDENTIALS_DIR / "token_auramelody.json"
    }
}

def get_youtube_service(account_key: str):
    account_key = account_key.lower()
    if account_key not in CHANNELS:
        raise ValueError(f"Unknown account key: {account_key}. Choose from {list(CHANNELS.keys())}")
    
    token_path = CHANNELS[account_key]["token_file"]
    if not token_path.exists():
        raise FileNotFoundError(f"Token file not found at {token_path}. Run OAuth authentication first.")
    
    with open(token_path, "r", encoding="utf-8") as f:
        token_data = json.load(f)
    
    creds = Credentials.from_authorized_user_info(token_data)
    return build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    print("=== Verifying All Connected Channels ===")
    for key, info in CHANNELS.items():
        try:
            yt = get_youtube_service(key)
            res = yt.channels().list(part="snippet", mine=True).execute()
            for item in res.get("items", []):
                print(f"  ✅ [{key}] Verified: {item['snippet']['title']} (ID: {item['id']})")
        except Exception as e:
            print(f"  ❌ [{key}] Error: {e}")
