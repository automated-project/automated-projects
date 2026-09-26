# -*- coding: utf-8 -*-
"""
新チャンネル（第3チャンネル: Melodic EDM）専用OAuth認証スクリプト
- 認証完了後、shared/credentials/token_auramelody.json に独立・永続保存
- 他のアカウント（phonkforge, gameverse）のトークンは一切上書き・干渉しない
"""
import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

CREDENTIALS_DIR = Path("/Users/base/Automated-Projects/YouTube/shared/credentials")
CLIENT_SECRETS = CREDENTIALS_DIR / "client_secrets.json"
TARGET_TOKEN = CREDENTIALS_DIR / "token_auramelody.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload"
]

print(f"=== Starting OAuth for 3rd Channel (AuraMelody Audio) ===")
print(f"Client Secrets: {CLIENT_SECRETS}")
print(f"Target Token Save Path: {TARGET_TOKEN}")

flow = InstalledAppFlow.from_client_secrets_file(
    str(CLIENT_SECRETS),
    SCOPES
)

# 8080ポートで認証サーバー起動 & ブラウザ自動オープン
creds = flow.run_local_server(port=8080, open_browser=True)

with open(TARGET_TOKEN, "w", encoding="utf-8") as f:
    f.write(creds.to_json())

print("✅ SUCCESS_AURAMELODY_AUTHENTICATED")
print(f"✅ Token permanently saved to: {TARGET_TOKEN}")
