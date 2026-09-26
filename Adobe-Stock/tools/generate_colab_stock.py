#!/usr/bin/env python3
"""
Google Colab CLI を経由して SDXL-Lightning で Adobe Stock 用画像を生成・4K拡大し、
ローカルの outputs / outputs_upscaled / CSV に自動同期するランナースクリプト
"""

import os
import sys
import subprocess
import csv
import shutil
import zipfile

COLAB_BIN = os.path.expanduser("~/.local/bin/colab")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER_SCRIPT = os.path.join(BASE_DIR, "tools", "remote_sdxl_worker.py")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")
SESSION_NAME = "adobe-gpu"

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

def run_cmd(cmd, check=True):
    print(f"▶ {cmd}")
    res = subprocess.run(cmd, shell=True, check=check, text=True)
    return res

def main():
    print("==================================================")
    print("🚀 SDXL-Lightning × Colab CLI 制作パイプライン開始")
    print("==================================================")

    # 1. セッション確認
    print("\n🔍 Colab セッションを確認中...")
    status = subprocess.getoutput(f"{COLAB_BIN} sessions")
    if SESSION_NAME not in status:
        print(f"⚡ セッション '{SESSION_NAME}' (T4 GPU) を新規起動します...")
        run_cmd(f"{COLAB_BIN} new -s {SESSION_NAME} --gpu T4")
    else:
        print(f"✅ セッション '{SESSION_NAME}' (T4 GPU) を再利用します。")

    # 2. クラウド側で SDXL ワーカーを実行
    print("\n⏳ クラウドGPU上で SDXL-Lightning 生成 ＆ 4Kアップスケールを実行中...")
    run_cmd(f"{COLAB_BIN} exec -s {SESSION_NAME} -f '{WORKER_SCRIPT}' --timeout 600.0")

    # 3. 成果物のダウンロード
    print("\n📥 クラウドから成果物（sdxl_result.zip）をダウンロード中...")
    local_zip = os.path.join(BASE_DIR, "sdxl_result.zip")
    if os.path.exists(local_zip):
        os.remove(local_zip)

    run_cmd(f"{COLAB_BIN} download -s {SESSION_NAME} /content/sdxl_result.zip '{local_zip}'")

    # 4. ZIPを展開してローカルフォルダに同期
    print("\n📂 ローカルフォルダへ成果物を配置中...")
    extract_dir = os.path.join(BASE_DIR, "_sdxl_temp")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    with zipfile.ZipFile(local_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # outputs (raw) のコピー
    src_outputs = os.path.join(extract_dir, "outputs")
    if os.path.exists(src_outputs):
        for f in os.listdir(src_outputs):
            shutil.copy2(os.path.join(src_outputs, f), os.path.join(OUTPUTS_DIR, f))
            print(f"   [Raw] -> outputs/{f}")

    # outputs_upscaled (4K) のコピー
    src_upscaled = os.path.join(extract_dir, "outputs_upscaled")
    if os.path.exists(src_upscaled):
        for f in os.listdir(src_upscaled):
            shutil.copy2(os.path.join(src_upscaled, f), os.path.join(UPSCALED_DIR, f))
            print(f"   [4K]  -> outputs_upscaled/{f}")

    # CSV のマージ（既存の adobe_stock_submission.csv に追記）
    new_csv = os.path.join(extract_dir, "submission_sdxl.csv")
    if os.path.exists(new_csv):
        new_rows = []
        with open(new_csv, mode="r", encoding="utf-8-sig") as nf:
            reader = csv.DictReader(nf)
            fieldnames = reader.fieldnames
            for row in reader:
                new_rows.append(row)

        existing_filenames = set()
        existing_rows = []
        if os.path.exists(MAIN_CSV):
            with open(MAIN_CSV, mode="r", encoding="utf-8-sig") as mf:
                reader = csv.DictReader(mf)
                for row in reader:
                    existing_filenames.add(row.get("Filename"))
                    existing_rows.append(row)
        
        added_count = 0
        for r in new_rows:
            if r.get("Filename") not in existing_filenames:
                existing_rows.append(r)
                added_count += 1
        
        with open(MAIN_CSV, mode="w", encoding="utf-8-sig", newline="") as mf:
            writer = csv.DictWriter(mf, fieldnames=fieldnames or ["Filename", "Title", "Keywords", "Category"])
            writer.writeheader()
            writer.writerows(existing_rows)
        print(f"   [CSV] -> {MAIN_CSV} に {added_count} 件のメタデータを追記しました！")

    # 一時ファイルの削除
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    if os.path.exists(local_zip):
        os.remove(local_zip)

    print("\n==================================================")
    print("🎉 すべての処理が完了しました！")
    print(f"・元画像: {OUTPUTS_DIR}")
    print(f"・4K画像: {UPSCALED_DIR}")
    print(f"・出品CSV: {MAIN_CSV}")
    print("==================================================")

if __name__ == "__main__":
    main()
