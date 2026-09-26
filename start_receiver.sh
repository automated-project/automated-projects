#!/bin/bash
# Gemini Production Suite ローカル統合サーバー起動ランチャー

cd "/Users/base/Automated-Projects" || exit 1
echo "🚀 Gemini Production Suite サーバーを起動します..."
if [ -f "./YouTube/venv/bin/python" ]; then
    ./YouTube/venv/bin/python serve_catalogs.py
else
    python3 serve_catalogs.py
fi
