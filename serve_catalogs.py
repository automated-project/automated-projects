#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini Production Suite: 総合受信 & プロンプト管理サーバー (Port 8765)
- プロンプトカタログ (Adobe Stock / Game Music) のリアルタイムAPI配信
- Web版Geminiからの画像・動画・音楽の直接受信 & 専用フォルダ書き込み (CORS/DL制限完全ゼロ)
- 4K Lanczos拡大 & 動画透かし自動除去 & 音楽抽出パイプラインの自動起動
"""

import http.server
import socketserver
import json
import os
import sys
import shutil
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

PORT = 8765
ROOT_DIR = Path("/Users/base/Automated-Projects").resolve()
STOCK_CATALOG_PATH = ROOT_DIR / "Adobe-Stock" / "stock_catalog.json"
MUSIC_CATALOG_PATH = ROOT_DIR / "Game-Music" / "music_catalog.json"

STOCK_OUTPUTS_DIR = ROOT_DIR / "Adobe-Stock" / "outputs"
MUSIC_OUTPUTS_DIR = ROOT_DIR / "新曲-web"

class ProductionHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. ヘルスチェック & 概要
        if path in ("/api/status", "/status"):
            stock_exists = STOCK_CATALOG_PATH.exists()
            music_exists = MUSIC_CATALOG_PATH.exists()
            stock_count = len(json.loads(STOCK_CATALOG_PATH.read_text(encoding="utf-8"))) if stock_exists else 0
            music_count = len(json.loads(MUSIC_CATALOG_PATH.read_text(encoding="utf-8"))) if music_exists else 0

            self.send_json({
                "status": "ready",
                "server": "Gemini Production Suite Receiver v5.2 (Music, Image & Video)",
                "stock_catalog": {"status": "ok" if stock_exists else "missing", "days": stock_count},
                "music_catalog": {"status": "ok" if music_exists else "missing", "tracks": music_count}
            })
            return

        # 2. カタログ配信 (JSON)
        if path in ("/stock_catalog.json", "/api/prompts/stock"):
            if STOCK_CATALOG_PATH.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(STOCK_CATALOG_PATH.read_bytes())
            else:
                self.send_json({"error": "stock_catalog.json not found"}, 404)
            return

        if path in ("/music_catalog.json", "/api/prompts/music"):
            if MUSIC_CATALOG_PATH.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(MUSIC_CATALOG_PATH.read_bytes())
            else:
                self.send_json({"error": "music_catalog.json not found"}, 404)
            return

        # 3. Web管理ダッシュボード
        if path in ("/", "/index.html"):
            self.render_dashboard()
            return

        self.send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)

        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {e}"}, 400)
            return

        if path == "/api/upload":
            self.handle_upload(payload)
            return

        if path == "/api/save_csv":
            self.handle_save_csv(payload)
            return

        if path == "/api/process":
            self.handle_process(payload)
            return

        self.send_json({"error": "Endpoint Not Found"}, 404)

    def handle_upload(self, payload):
        """画像・動画・音楽の受信 & 専用フォルダ書き込み"""
        workflow = payload.get("workflow", "adobe_stock")
        filename = payload.get("filename", "")
        media_type = payload.get("type", "image")
        url = payload.get("url", "")
        base64_data = payload.get("base64_data", "")
        subfolder_name = payload.get("subfolder", "")

        today_str = datetime.now().strftime("%Y%m%d")

        if workflow == "adobe_stock":
            if not subfolder_name:
                subfolder_name = f"AdobeStock_Batch_{today_str}"
            target_dir = STOCK_OUTPUTS_DIR / subfolder_name
        else: # game_music
            target_dir = MUSIC_OUTPUTS_DIR
            if subfolder_name:
                target_dir = target_dir / subfolder_name

        target_dir.mkdir(parents=True, exist_ok=True)
        out_file = target_dir / filename

        print(f"\n📥 [受信開始] {workflow} ({media_type}) ➔ {target_dir.name}/{filename}")

        saved = False
        if base64_data:
            import base64
            try:
                if "," in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                file_bytes = base64.b64decode(base64_data)
                out_file.write_bytes(file_bytes)
                saved = True
                print(f"✅ [Base64保存成功]: {out_file.name} ({len(file_bytes)} bytes)")
            except Exception as e:
                print(f"⚠️ Base64デコードエラー: {e}")

        if not saved and url:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
                )
                with urllib.request.urlopen(req, timeout=90) as resp:
                    file_bytes = resp.read()
                    if file_bytes.startswith(b"<!doctype html") or file_bytes.startswith(b"<html"):
                        print(f"❌ [拒絶]: Google認証セッションが必要なURLです (HTMLログイン画面が返されました: {filename})")
                    else:
                        out_file.write_bytes(file_bytes)
                        saved = True
                        print(f"✅ [URLダウンロード保存成功]: {out_file.name} ({len(file_bytes)} bytes)")
            except Exception as e:
                print(f"❌ URLダウンロード失敗: {e}")

        if saved:
            self.send_json({
                "status": "success",
                "filename": filename,
                "saved_path": str(out_file),
                "folder": str(target_dir)
            })
        else:
            self.send_json({"error": "Failed to save file"}, 500)

    def handle_save_csv(self, payload):
        """CSV保存"""
        workflow = payload.get("workflow", "adobe_stock")
        csv_text = payload.get("csv_text", "")
        subfolder_name = payload.get("subfolder", "")
        filename = payload.get("filename", "adobe_stock_submission.csv")

        today_str = datetime.now().strftime("%Y%m%d")
        if workflow == "adobe_stock":
            if not subfolder_name:
                subfolder_name = f"AdobeStock_Batch_{today_str}"
            target_dir = STOCK_OUTPUTS_DIR / subfolder_name
        else:
            target_dir = MUSIC_OUTPUTS_DIR

        target_dir.mkdir(parents=True, exist_ok=True)
        csv_path = target_dir / filename
        csv_path.write_text(csv_text, encoding="utf-8")
        print(f"📄 [CSV保存完了]: {csv_path.relative_to(ROOT_DIR)}")

        self.send_json({"status": "success", "path": str(csv_path)})

    def handle_process(self, payload):
        """パイプライン実行キック (4K化など)"""
        workflow = payload.get("workflow", "adobe_stock")
        subfolder = payload.get("subfolder", "")

        today_str = datetime.now().strftime("%Y%m%d")
        if workflow == "adobe_stock":
            if not subfolder:
                subfolder = f"AdobeStock_Batch_{today_str}"
            target_dir = STOCK_OUTPUTS_DIR / subfolder
            script = ROOT_DIR / "Adobe-Stock" / "tools" / "upscale_adobe_stock_4k.py"
            py_bin = str(ROOT_DIR / "YouTube" / "venv" / "bin" / "python")
            if not Path(py_bin).exists():
                py_bin = sys.executable

            print(f"\n🚀 [パイプライン起動] Adobe Stock 4K拡大 & 透かし除去: {target_dir.name}")
            try:
                subprocess.Popen([py_bin, str(script), str(target_dir)])
                self.send_json({"status": "started", "target": str(target_dir)})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
        else:
            self.send_json({"status": "ignored", "message": f"No pipeline for {workflow}"})

    def render_dashboard(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Gemini Production Suite v5.2 Dashboard</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 32px; }}
.container {{ max-width: 900px; margin: 0 auto; }}
h1 {{ color: #60a5fa; border-bottom: 2px solid #1e293b; padding-bottom: 12px; }}
.card {{ background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 16px rgba(0,0,0,0.4); }}
.badge {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 12px; }}
.badge-ok {{ background: #065f46; color: #34d399; }}
code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #f43f5e; }}
</style>
</head>
<body>
<div class="container">
<h1>⚡ Gemini Production Suite v5.2</h1>
<p style="color:#94a3b8;">音楽・画像・動画 完全自律生成サーバー (Port {PORT})</p>
<div class="card">
<h3>📸 Adobe Stock (画像＆動画)</h3>
<p>保存先: <code>Adobe-Stock/outputs/</code></p>
<p>ステータス: <span class="badge badge-ok">稼働中 (4K拡大 & 透かし除去連動)</span></p>
</div>
<div class="card">
<h3>🎵 Game Music (音楽＆カバー)</h3>
<p>保存先: <code>新曲-web/</code></p>
<p>ステータス: <span class="badge badge-ok">稼働中 (WAV/MP3抽出パイプライン連動)</span></p>
</div>
</div>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ProductionHandler) as httpd:
        print("=" * 60)
        print(f"🚀 [Gemini Production Suite v5.2] サーバー起動完了！")
        print(f"📡 受信ポート: http://127.0.0.1:{PORT}")
        print("  - 📸 Adobe Stock: 画像＆4K動画自動受信")
        print("  - 🎵 Game Music: 音楽動画直接受信 ➔ 新曲-web")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 サーバー停止")

if __name__ == "__main__":
    run_server()
