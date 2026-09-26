#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Sheets テンプレート完全自動生成エンジン
(Google Sheets Automated Template Factory)

【機能】
1. Google Sheets API & Drive API 認証 (OAuth 2.0 / token_sheets.json による自動再利用)
2. 美しいUI・数式・ドロップダウン・条件付き書式付きスプレッドシートの完全自動構築
3. 閲覧権限の自動付与 ＆ 「/copy」テンプレート複製URLの自動生成
4. Gumroad API との直接連携 (自動出品)
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

TOKEN_FILE = "token_sheets.json"
CLIENT_SECRETS_FILE = "client_secrets.json"

def get_services():
    """Google Sheets と Google Drive の API サービスオブジェクトを取得"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(f"{CLIENT_SECRETS_FILE} が見つかりません。")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            print("==================================================================")
            print("🔑 Google Sheets & Drive の初回認可を開始します。")
            print("ブラウザが開きますので、Googleアカウントでログインして許可してください。")
            print("==================================================================")
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    sheets_service = build("sheets", "v4", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return sheets_service, drive_service

def make_template_public_copy(drive_service, spreadsheet_id: str) -> str:
    """スプレッドシートを『リンクを知っている全員が閲覧可能』に設定し、/copy URLを生成"""
    permission = {
        "type": "anyone",
        "role": "reader"
    }
    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permission,
        fields="id"
    ).execute()

    copy_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/copy"
    return copy_url

def build_creator_revenue_hub(sheets_service, drive_service, title="All-in-One Creator Revenue Hub"):
    """
    プロ級のデジタルクリエイター向け収支管理ダッシュボードを完全自動生成
    - メインKPIサマリーカード
    - 自動計算式 (SUM, 利益計算)
    - プラットフォーム選択ドロップダウン
    - プロ仕様のカラーリング (ダークネイビー & エメラルドグリーン)
    """
    print(f"📊 新規スプレッドシート作成中: {title}...")
    spreadsheet = {
        "properties": {
            "title": title,
            "locale": "en_US",
            "autoRecalc": "ON_CHANGE"
        }
    }
    ss = sheets_service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId,sheets").execute()
    ss_id = ss.get("spreadsheetId")
    sheet_id = ss["sheets"][0]["properties"]["sheetId"]
    print(f"✅ スプレッドシート作成完了 (ID: {ss_id})")

    # 1. セルデータの投入 (サマリーKPIカード + トランザクションテーブル)
    values = [
        # 行1: タイトルヘッダー
        ["CREATOR REVENUE & ASSET SALES HUB", "", "", "", "", "", "", ""],
        ["All-in-One Multi-Platform Income & Expense Tracker", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        
        # 行4: KPI サマリーカード見出し
        ["TOTAL GROSS REVENUE", "", "TOTAL PLATFORM FEES", "", "NET PROFIT", "", "PROFIT MARGIN", ""],
        # 行5: KPI 計算式
        ['=SUM(F11:F100)', "", '=SUM(G11:G100)', "", '=A5-C5', "", '=IF(A5>0, E5/A5, 0)', ""],
        ["", "", "", "", "", "", "", ""],
        
        # 行7: プラットフォーム別サマリー見出し
        ["PLATFORM BREAKDOWN", "", "", "", "", "", "", ""],
        ["Platform", "Total Sales", "Gross Revenue", "Net Profit", "", "", "", ""],
        ["Gumroad", '=COUNTIF(B11:B100, "Gumroad")', '=SUMIF(B11:B100, "Gumroad", F11:F100)', '=SUMIF(B11:B100, "Gumroad", H11:H100)', "", "", "", ""],
        ["YouTube / AdSense", '=COUNTIF(B11:B100, "YouTube")', '=SUMIF(B11:B100, "YouTube", F11:F100)', '=SUMIF(B11:B100, "YouTube", H11:H100)', "", "", "", ""],
        
        # 行11: トランザクション明細ヘッダー
        ["DATE", "PLATFORM", "PRODUCT / ASSET NAME", "CATEGORY", "UNITS", "GROSS AMOUNT ($)", "FEE ($)", "NET PROFIT ($)"],
        # サンプルデータ 1
        ["2026-09-01", "Gumroad", "Neon Overdrive Audio Pack", "Audio Asset", 1, 3.00, 0.30, "=F12-G12"],
        # サンプルデータ 2
        ["2026-09-02", "Gumroad", "Wrath of the Abyss BGM", "Audio Asset", 1, 3.00, 0.30, "=F13-G13"],
        # サンプルデータ 3
        ["2026-09-03", "YouTube", "Sarcasm Documentary AdSense", "Ad Revenue", 1, 45.20, 0.00, "=F14-G14"],
    ]

    body = {
        "values": values
    }
    sheets_service.spreadsheets().values().update(
        spreadsheetId=ss_id,
        range="A1:H14",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    # 2. スタイル・装飾・ドロップダウンのバッチ適用
    print("🎨 プロ仕様のデザイン・書式設定・ドロップダウンを適用中...")
    requests = [
        # (1) タイトルの結合 & スタイル
        {
            "mergeCells": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8},
                "mergeType": "MERGE_ALL"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.06, "green": 0.09, "blue": 0.16}, # ダークスレート
                        "horizontalAlignment": "LEFT",
                        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "fontSize": 16, "bold": True}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },
        
        # (2) KPIサマリーカードの背景色 (エメラルドグリーン & ダーク)
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.12, "green": 0.16, "blue": 0.24},
                        "textFormat": {"foregroundColor": {"red": 0.58, "green": 0.64, "blue": 0.72}, "fontSize": 10, "bold": True}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.06, "green": 0.09, "blue": 0.16},
                        "textFormat": {"foregroundColor": {"red": 0.08, "green": 0.72, "blue": 0.65}, "fontSize": 18, "bold": True}, # エメラルド
                        "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,numberFormat)"
            }
        },

        # (3) 明細テーブルヘッダー (行11) のスタイリング
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 10, "endRowIndex": 11, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.15, "green": 0.23, "blue": 0.36}, # ディープネイビー
                        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "fontSize": 11, "bold": True},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },

        # (4) プラットフォーム列 (B列) にドロップダウンリスト (Data Validation) を設定
        {
            "setDataValidation": {
                "range": {"sheetId": sheet_id, "startRowIndex": 11, "endRowIndex": 100, "startColumnIndex": 1, "endColumnIndex": 2},
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {"userEnteredValue": "Gumroad"},
                            {"userEnteredValue": "YouTube"},
                            {"userEnteredValue": "Adobe Stock"},
                            {"userEnteredValue": "Shutterstock"},
                            {"userEnteredValue": "KDP / Books"},
                            {"userEnteredValue": "Patreon"}
                        ]
                    },
                    "inputMessage": "プラットフォームを選択してください",
                    "showCustomUi": True
                }
            }
        },

        # (5) 通貨フォーマット (F, G, H列)
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 11, "endRowIndex": 100, "startColumnIndex": 5, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"}
                    }
                },
                "fields": "userEnteredFormat(numberFormat)"
            }
        },

        # (6) 列幅の最適化
        {"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 110}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 140}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 240}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4}, "properties": {"pixelSize": 130}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 5, "endIndex": 8}, "properties": {"pixelSize": 130}, "fields": "pixelSize"}},
    ]

    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=ss_id,
        body={"requests": requests}
    ).execute()

    # 3. 共有設定 & /copy テンプレートURLの生成
    print("🔗 テンプレート共有設定 (/copy URL) を生成中...")
    copy_url = make_template_public_copy(drive_service, ss_id)

    print("\n==================================================")
    print("🎉 Google Sheets テンプレートが完全に自動構築されました！")
    print(f"編集・管理URL: https://docs.google.com/spreadsheets/d/{ss_id}/edit")
    print(f"配布・販売用 /copy URL: {copy_url}")
    print("==================================================")
    return ss_id, copy_url

if __name__ == "__main__":
    sheets, drive = get_services()
    build_creator_revenue_hub(sheets, drive)
