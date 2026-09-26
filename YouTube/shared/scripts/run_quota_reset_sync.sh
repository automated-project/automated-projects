#!/bin/bash
# ==============================================================================
# YouTube Quota Reset Auto-Sync Runner (毎日 16:05 JST 自動実行)
# 全チャンネルの最新多言語メタデータ ＆ 固定コメント（英語＋ロシア語）を一括反映
# ==============================================================================

PROJECT_DIR="/Users/base/Automated-Projects/YouTube"
PYTHON_BIN="$PROJECT_DIR/venv/bin/python3"
LOG_FILE="$PROJECT_DIR/shared/quota_sync.log"

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Starting Daily Post-Quota Reset Sync ===" >> "$LOG_FILE"

# 1. メタデータ＆多言語ローカライズ同期
echo "[+] Running sync_all_channels_metadata.py..." >> "$LOG_FILE"
"$PYTHON_BIN" "$PROJECT_DIR/shared/scripts/sync_all_channels_metadata.py" >> "$LOG_FILE" 2>&1

# 2. 固定コメント（英語＋ロシア語）同期
echo "[+] Running update_all_pinned_comments.py..." >> "$LOG_FILE"
"$PYTHON_BIN" "$PROJECT_DIR/shared/scripts/update_all_pinned_comments.py" >> "$LOG_FILE" 2>&1

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Finished Daily Sync ===" >> "$LOG_FILE"
