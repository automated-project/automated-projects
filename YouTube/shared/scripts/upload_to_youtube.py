#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube Data API v3 自動アップロードスクリプト
(YouTube Video Auto-Uploader)

- OAuth 2.0 認証 (client_secrets.json → token.json による自動再利用)
- メタデータJSON (タイトル・概要欄・タグ等) の自動読み込み対応
- 分割レジュームアップロード (Resumable Upload) 対応
"""

import os
import sys
import json
import argparse
import http.client
import httplib2
import random
import time
from pathlib import Path
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 環境変数の読み込み
load_dotenv()

# 必要なOAuthスコープ
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"

# アップロードのリトライ設定
httplib2.RETRIES = 3
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, http.client.NotConnected,
    http.client.IncompleteRead, http.client.ImproperConnectionState,
    http.client.CannotSendRequest, http.client.CannotSendHeader,
    http.client.ResponseNotReady, http.client.BadStatusLine
)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

def get_authenticated_service(account_num: int = None):
    """OAuth 2.0 認証を行い、YouTube サービスオブジェクトを返します (アカウント1/2両対応)。"""
    try:
        from account_manager import get_account_config
        cfg = get_account_config(account_num)
        client_id = cfg["youtube_client_id"]
        client_secret = cfg["youtube_client_secret"]
        refresh_token = cfg["youtube_refresh_token"]
        acct = cfg["account_num"]
    except ImportError:
        client_id = os.getenv("YOUTUBE_CLIENT_ID")
        client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        acct = 1

    if client_id and client_secret and refresh_token:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=None
        )
        return build("youtube", "v3", credentials=creds)

    # 2. 既存の token.json から読み込み
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print("==================================================================", file=sys.stderr)
                print(f"エラー: OAuth認証情報が見つかりません。", file=sys.stderr)
                print(".env に YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN を設定するか、", file=sys.stderr)
                print(f"'{CLIENT_SECRETS_FILE}' を配置してください。", file=sys.stderr)
                print("==================================================================", file=sys.stderr)
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

    return build("youtube", "v3", credentials=creds)

def resumable_upload(request):
    """分割レジュームアップロードを実行します。"""
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"アップロード中... {int(status.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"再試行可能なエラーが発生しました: {e}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"接続エラーが発生しました: {e}"

        if error is not None:
            print(error, file=sys.stderr)
            retry += 1
            if retry > MAX_RETRIES:
                print("最大再試行回数を超えました。", file=sys.stderr)
                sys.exit(1)
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"{sleep_seconds:.1f} 秒待機して再試行します...", file=sys.stderr)
            time.sleep(sleep_seconds)

    print("==================================================")
    print(f" アップロード成功！")
    video_id = response.get('id')
    print(f" 動画ID: {video_id}")
    print(f" URL: https://youtu.be/{video_id}")
    print(f" Shorts URL: https://www.youtube.com/shorts/{video_id}")
    print("==================================================")
    return response

def upload_video(video_path: Path, title: str, description: str, tags: list, privacy_status: str = "private", thumbnail_path: Path = None, account_num: int = None, publish_at: str = None, category_id: str = None):
    """動画をYouTubeにアップロードします。デフォルトは安全確認用の非公開(private)です。"""
    if not video_path.exists():
        print(f"エラー: 動画ファイルが見つかりません: {video_path}", file=sys.stderr)
        sys.exit(1)

    youtube = get_authenticated_service(account_num=account_num)

    status_dict = {
        "selfDeclaredMadeForKids": False
    }
    if publish_at:
        status_dict["privacyStatus"] = "private"
        status_dict["publishAt"] = publish_at
    else:
        status_dict["privacyStatus"] = privacy_status

    # カテゴリの決定: 指定があれば優先、アカウント2はEducation(27)、その他はMusic(10)
    cat_id = category_id or ("27" if account_num == 2 else "10")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": cat_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": status_dict
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"YouTube へのアップロードを開始します...")
    print(f" タイトル: {title}")
    print(f" 公開設定: {privacy_status}")
    response = resumable_upload(request)

    # サムネイルの設定（指定されている場合）
    if thumbnail_path and thumbnail_path.exists():
        video_id = response.get("id")
        print(f"サムネイルを設定中: {thumbnail_path}")
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
            ).execute()
            print("サムネイルの設定が完了しました！")
        except Exception as e:
            print(f"注: サムネイルAPI設定はスキップされました（動画冒頭のフレームがカバー画像として適用されます）。理由: {e}")

    return response

def main():
    parser = argparse.ArgumentParser(description="YouTube Data API v3 動画自動アップローダー")
    parser.add_argument("--meta", help="メタデータJSONファイルのパス (指定するとtitle/desc/tags/videoを自動取得)")
    parser.add_argument("--video", help="アップロードする動画ファイルパス")
    parser.add_argument("--thumbnail", help="サムネイル画像ファイルパス")
    parser.add_argument("--title", help="動画タイトル")
    parser.add_argument("--description", help="概要欄テキスト")
    parser.add_argument("--tags", nargs="*", help="タグ一覧")
    parser.add_argument("--account", type=int, help="アップロード先アカウント番号 (1 または 2)")
    parser.add_argument(
        "--privacy",
        choices=["public", "private", "unlisted"],
        default="public",
        help="公開ステータス (デフォルト: public)"
    )
    args = parser.parse_args()

    video_file = None
    thumbnail_file = None
    title = None
    description = ""
    tags = []

    # メタデータJSONがある場合は読み込み
    if args.meta:
        meta_path = Path(args.meta)
        if not meta_path.exists():
            print(f"エラー: メタデータファイルが見つかりません: {meta_path}", file=sys.stderr)
            sys.exit(1)
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            video_file = Path(meta.get("video_file", ""))
            if meta.get("thumbnail_file"):
                thumbnail_file = Path(meta.get("thumbnail_file"))
            title = meta.get("title")
            description = meta.get("description", "")
            tags = meta.get("tags", [])

    if args.video:
        video_file = Path(args.video)
    if args.thumbnail:
        thumbnail_file = Path(args.thumbnail)
    if args.title:
        title = args.title
    if args.description:
        description = args.description
    if args.tags:
        tags = args.tags

    if not video_file or not title:
        print("エラー: 動画ファイルとタイトルは必須です。(--meta または --video, --title を指定してください)", file=sys.stderr)
        sys.exit(1)

    upload_video(
        video_path=video_file,
        title=title,
        description=description,
        tags=tags,
        privacy_status=args.privacy,
        thumbnail_path=thumbnail_file,
        account_num=args.account
    )

if __name__ == "__main__":
    main()
