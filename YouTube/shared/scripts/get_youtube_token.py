#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
get_youtube_token.py
-------------------------------------------------------------------------------
新チャンネル（Gym Phonk特化チャンネル等）のYouTube Data API OAuth認証トークン取得スクリプト

【使用手順】
1. Google Cloud Console で作成した OAuth クライアントID の JSON ファイルを本ディレクトリに配置
   （例: YouTube/shared/credentials/client_secrets.json）
2. 本スクリプトを実行:
   python3 get_youtube_token.py --client-secrets /path/to/client_secrets.json --output-token YouTube/02_Gym_Phonk_Channel/token.json
3. ブラウザが自動で開くので、新チャンネルを管理しているGoogleアカウント / ブランドアカウントを選択して許可。
4. トークンが保存され、次回から自動でAPIアクセス・動画投稿が可能になります。
-------------------------------------------------------------------------------
"""

import os
import sys
import argparse
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube"
]

def main():
    parser = argparse.ArgumentParser(description="Acquire YouTube OAuth Token for a Channel")
    parser.add_argument("--client-secrets", default="/Users/base/Automated-Projects/YouTube/shared/credentials/client_secrets.json", help="Path to client_secrets.json")
    parser.add_argument("--output-token", default="/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/token.json", help="Path to output token.json")
    args = parser.parse_args()

    client_secrets_path = Path(args.client_secrets)
    output_token_path = Path(args.output_token)

    if not client_secrets_path.exists():
        print(f"[-] Error: client_secrets file not found at: {client_secrets_path}")
        print(f"[*] Please place your Google Cloud OAuth client_secrets.json at this path and rerun.")
        sys.exit(1)

    output_token_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[+] Starting OAuth 2.0 Flow for YouTube API...")
    print(f"[*] Client Secrets: {client_secrets_path}")
    print(f"[*] Target Token: {output_token_path}")
    print(f"[*] Opening browser for authentication...")

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), SCOPES)
    creds = flow.run_local_server(port=0)

    with open(output_token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print(f"[✓] Authentication Successful!")
    print(f"[✓] Token saved to: {output_token_path}")
    print(f"[*] You can now automate uploads to this channel!")

if __name__ == "__main__":
    main()
