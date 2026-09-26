#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
itch.io API & Butler CLI 連携クライアント
(GameVerse Audio用 itch.io デプロイモジュール)

【機能】
1. APIキー検証・認証情報取得
2. 登録済みゲーム一覧の取得・存在チェック
3. Butler CLI を使用したアセットパッケージ（ZIP）の高速自動プッシュ
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import urllib.request
import urllib.error
BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

ITCH_API_KEY = os.getenv("ITCH_API_KEY") or os.getenv("BUTLER_API_KEY")
ITCH_USERNAME = os.getenv("ITCH_USERNAME", "gameverse-audio")
BUTLER_PATH = BASE_DIR / "bin" / "butler"

def get_headers():
    if not ITCH_API_KEY:
        raise ValueError("ITCH_API_KEY または BUTLER_API_KEY が .env に設定されていません。")
    return {
        "Authorization": f"Bearer {ITCH_API_KEY}",
        "User-Agent": "GameVerse-Audio-Automation/1.0"
    }

def verify_credentials() -> dict:
    """itch.io APIキーを検証し、ユーザー情報を取得します。"""
    url = "https://itch.io/api/1/key/me"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data.get("user", {})
    except urllib.error.HTTPError as e:
        print(f"itch.io API 認証エラー: HTTP {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"itch.io 通信エラー: {e}", file=sys.stderr)
        return {}

def get_my_games() -> list:
    """登録済みのプロジェクト一覧を取得します。"""
    url = "https://itch.io/api/1/key/my-games"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            games = data.get("games", [])
            # 配列または辞書の可能性に対応
            if isinstance(games, dict):
                return list(games.values())
            return games
    except Exception as e:
        print(f"itch.io ゲーム一覧取得エラー: {e}", file=sys.stderr)
        return []

def game_exists(slug: str) -> bool:
    """指定したスラッグのプロジェクトが存在するか確認します。"""
    games = get_my_games()
    for g in games:
        # url や title, slug を照合
        url = g.get("url", "")
        if f"/{slug}" in url or g.get("title", "").lower() == slug.lower():
            return True
    return False

def push_build(zip_path: Path, channel: str, project_slug: str = "game-music-vault", user_version: str = "1.0.0") -> bool:
    """
    Butler CLI を使用してアセットZIPを itch.io の Vault プロジェクトの指定チャンネルにプッシュします。
    例: gameverse-audio/game-music-vault:god-of-ruin
    """
    if not zip_path.exists():
        print(f"エラー: アップロード対象ファイルが存在しません: {zip_path}", file=sys.stderr)
        return False

    butler_cmd = str(BUTLER_PATH) if BUTLER_PATH.exists() else "butler"
    target = f"{ITCH_USERNAME}/{project_slug}:{channel}"

    env = os.environ.copy()
    env["BUTLER_API_KEY"] = ITCH_API_KEY

    cmd = [
        butler_cmd,
        "push",
        str(zip_path),
        target,
        f"--userversion={user_version}"
    ]

    print(f"\n🎮 itch.io Butler アップロード開始...")
    print(f"ターゲット: {target}")
    print(f"パッケージ: {zip_path.name}")

    try:
        res = subprocess.run(cmd, env=env, check=True, text=True, capture_output=True)
        print("✅ itch.io へのプッシュが完了しました！")
        print(res.stdout)
        print(f"🔗 プロジェクトURL: https://{ITCH_USERNAME}.itch.io/{project_slug}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Butler プッシュに失敗しました: {e}", file=sys.stderr)
        if e.stderr:
            print(f"エラー出力: {e.stderr}", file=sys.stderr)
        if "invalid game" in (e.stderr or ""):
            print(f"\n💡 ヒント: itch.io の Web ダッシュボード (https://itch.io/game/new) で、")
            print(f"   先にスラッグ名「{project_slug}」で総合アセットプロジェクト（Game Assets）を作成してください。")
            print(f"   一度ページを作成すれば、以降は全楽曲が完全自動でこのストアに追加されます。")
        return False

if __name__ == "__main__":
    print("=== itch.io 接続テスト ===")
    user = verify_credentials()
    if user:
        print(f"✅ 認証成功: {user.get('username')} (ID: {user.get('id')})")
        print(f"URL: {user.get('url')}")
        games = get_my_games()
        print(f"登録済みプロジェクト数: {len(games)}")
    else:
        print("❌ 認証失敗")
