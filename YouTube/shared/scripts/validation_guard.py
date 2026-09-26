#!/usr/bin/env python3
"""
YouTube & Media Pipeline Validation Guard Module
すべてのパイプライン・スクリプトで共通利用される事前・事後バリデーションガード
ユーザー指定の引数・変数・サムネイル画像・音声ファイル・動画時間等の整合性を自動検証する。
"""

import os
import sys
import subprocess
import json

class ValidationGuardError(Exception):
    """バリデーションガード専用例外。捏造・ごまかしを防止し即時停止させる。"""
    pass

def validate_input_params(params: dict, required_keys: list):
    """
    ユーザー指示・設定値パラメータの存在および非空チェック
    """
    for key in required_keys:
        if key not in params or params[key] is None or params[key] == "":
            raise ValidationGuardError(f"[事前検証エラー] 必須パラメータ '{key}' が指定されていないか空です。")
    print("✅ [Pre-Validation] 入力パラメータ検証合格")

def validate_file_exists(file_path: str, label: str = "ファイル"):
    """
    物理ファイルの存在確認
    """
    if not file_path or not isinstance(file_path, str):
        raise ValidationGuardError(f"[事前検証エラー] Invalid file path passed for {label}: {file_path}")
    if not os.path.exists(file_path):
        raise ValidationGuardError(f"[事前検証エラー] 指定された{label}が存在しません: {file_path}")
    if os.path.getsize(file_path) == 0:
        raise ValidationGuardError(f"[事前検証エラー] 指定された{label}のファイルサイズが0バイトです: {file_path}")
    print(f"✅ [Pre-Validation] {label} 存在確認OK: {file_path}")

def validate_audio_files(audio_files: list):
    """
    音声ファイル群の存在およびサイズチェック
    """
    if not audio_files or len(audio_files) == 0:
        raise ValidationGuardError("[事前検証エラー] 音声ファイルリストが空です。")
    for af in audio_files:
        validate_file_exists(af, label="音声ファイル")
    print(f"✅ [Pre-Validation] 音声ファイル群 ({len(audio_files)}件) 検証合格")

def get_media_duration(file_path: str) -> float:
    """
    ffprobeを使用して動画/音声の実際の再生時間(秒)を取得
    """
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        print(f"⚠️ Warning: ffprobe duration check failed for {file_path}: {e}")
        return 0.0

def validate_video_output(video_path: str, target_min_duration_sec: float = 0, expected_aspect_ratio: str = None):
    """
    事後検証ガード: 生成された動画ファイルが指示通りのスペック（存在、サイズ、動画時間）を満たしているか確認
    """
    validate_file_exists(video_path, label="出力動画")
    
    actual_duration = get_media_duration(video_path)
    print(f"🔍 [Post-Validation] 出力動画の計測尺: {actual_duration:.2f}秒 (目標最小: {target_min_duration_sec:.2f}秒)")
    
    if target_min_duration_sec > 0 and actual_duration < target_min_duration_sec:
        raise ValidationGuardError(
            f"[事後検証エラー] 動画尺がユーザー指示要件を満たしていません！ "
            f"計測値: {actual_duration:.2f}秒 < 要求値: {target_min_duration_sec:.2f}秒"
        )
    print("✅ [Post-Validation] 出力動画成果物検証合格")

def print_user_instruction_checklist(checklist_items: list):
    """
    完了報告用のユーザー指示履行確認チェックリストを表示・記録する
    checklist_items = [
        {"item": "サムネイルパス", "req": "path/to/thumb.jpg", "actual": "OK", "status": True},
        ...
    ]
    """
    print("\n========================================================")
    print("📋 ユーザー指示履行確認チェックリスト (User Directives Checklist)")
    print("========================================================")
    print(f"| {'指示項目':<20} | {'要求要件':<25} | {'実際の検証値':<25} | {'判定':<6} |")
    print("|" + "-"*22 + "|" + "-"*27 + "|" + "-"*27 + "|" + "-"*8 + "|")
    
    all_passed = True
    for entry in checklist_items:
        item = entry.get("item", "")
        req = str(entry.get("req", ""))
        actual = str(entry.get("actual", ""))
        status = "✅ PASS" if entry.get("status", False) else "❌ FAIL"
        if not entry.get("status", False):
            all_passed = False
        print(f"| {item:<20} | {req:<25} | {actual:<25} | {status:<6} |")
    print("========================================================\n")
    
    if not all_passed:
        raise ValidationGuardError("[チェックリスト判定エラー] 指示項目に不適合が含まれています。内容をごまかさず修正してください。")

if __name__ == "__main__":
    print("ValidationGuard Module Ready.")
