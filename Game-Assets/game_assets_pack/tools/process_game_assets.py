#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
process_game_assets.py: ゲームアセット自動背景透過 ＆ アイコン自動スライスツール
- 黒・ダーク背景の自動検出＆ルミナンスキーイング（発光・グローを美しく透過）
- ブラックフリンジ（黒いフチ）を自動除去するアンマルチプライ処理
- アイコンシートからの個別透過PNG自動スライス（512x512 等）
- 配布・販売用ZIPパッケージの自動生成
"""

import os
import sys
import glob
import zipfile
from pathlib import Path
from PIL import Image
import numpy as np

def make_transparent_luma(img_path, out_path, low_thresh=32, high_thresh=75):
    """
    黒・ダーク背景を高精度に透過（ルミナンス＋カラーキーイング）
    発光エフェクトや魔法の光を半透明で綺麗に残し、黒フチを除去する
    """
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"  ⚠️ [スキップ] 画像として開けません（SVGや破損ファイル等）: {Path(img_path).name} ({e})")
        return None

    data = np.array(img, dtype=np.float32)

    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # 各ピクセルの最大値と輝度
    max_val = np.maximum(np.maximum(r, g), b)
    luma = 0.299 * r + 0.587 * g + 0.114 * b

    # キーイング指標（輝度と最大チャンネルの複合）
    key_metric = 0.7 * max_val + 0.3 * luma

    # スムーズなアルファマスク生成 (Smoothstep)
    alpha = np.zeros_like(key_metric)
    mask_opaque = key_metric >= high_thresh
    mask_trans = key_metric <= low_thresh
    mask_inter = (~mask_opaque) & (~mask_trans)

    alpha[mask_opaque] = 255.0
    alpha[mask_trans] = 0.0

    # 遷移領域のスムーズ補間
    t = (key_metric[mask_inter] - low_thresh) / (high_thresh - low_thresh)
    alpha[mask_inter] = (3 * t**2 - 2 * t**3) * 255.0

    # ブラックフリンジ除去 (Unmultiply / カラーブースト)
    alpha_norm = np.clip(alpha / 255.0, 0.001, 1.0)
    for c in range(3):
        boosted = data[:, :, c] / alpha_norm
        data[:, :, c] = np.clip(boosted, 0, 255)

    data[:, :, 3] = np.clip(alpha, 0, 255)

    result = Image.fromarray(data.astype(np.uint8), "RGBA")
    result.save(out_path, "PNG")
    print(f"  ✨ [透過PNG生成]: {out_path.name}")
    return result

def auto_slice_icons(trans_img, base_name, out_dir, grid_cols=4, grid_rows=2):
    """
    透過PNGのマスターシートから個別の正方形アイコン（512x512等）を自動検出＆スライス
    - 投影プロファイル法により、1行5個・4x2・単体等、任意のレイアウトの境界（谷）を自動認識
    - 下部の不要な文字（ラベル）や上部のノイズ線を自動トリミング
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    w, h = trans_img.size
    alpha_data = np.array(trans_img)[:, :, 3]
    binary_mask = alpha_data > 40

    sliced_count = 0

    # 1. Y方向の投影プロファイル（行の検出）
    row_active = binary_mask.mean(axis=1)
    # アクティブな行の連続帯を取得
    row_segments = []
    in_seg = False
    start_y = 0
    for y, act in enumerate(row_active):
        if act > 0.05 and not in_seg:
            in_seg = True
            start_y = y
        elif act <= 0.05 and in_seg:
            in_seg = False
            if y - start_y > 50:  # 最低50pxの高さ
                row_segments.append((start_y, y))
    if in_seg and h - start_y > 50:
        row_segments.append((start_y, h))

    # 最も高さがある主要行（アイコン行）を選択（複数行あれば複数処理）
    if row_segments:
        # 小さな文字帯（下部の短い帯）を除外するため、高さが最大帯の35%以上ある帯のみ対象
        max_h = max(y1 - y0 for y0, y1 in row_segments)
        valid_row_segs = [(y0, y1) for y0, y1 in row_segments if (y1 - y0) >= max_h * 0.4]
    else:
        valid_row_segs = [(0, h)]

    for row_idx, (y0, y1) in enumerate(valid_row_segs):
        sub_mask = binary_mask[y0:y1, :]
        col_active = sub_mask.mean(axis=0)

        # X方向の谷（アイコン間の暗い隙間）を検出
        # 閾値よりアクティブな列をセグメント化
        col_segments = []
        in_col = False
        start_x = 0
        thresh_x = max(0.08, np.percentile(col_active, 30))
        for x, act in enumerate(col_active):
            if act > thresh_x and not in_col:
                in_col = True
                start_x = x
            elif act <= thresh_x and in_col:
                in_col = False
                if x - start_x > 40:  # 最低40pxの幅
                    col_segments.append((start_x, x))
        if in_col and w - start_x > 40:
            col_segments.append((start_x, w))

        # もし列検出が成功した場合（2個以上のアイコンが並んでいる場合）
        if len(col_segments) >= 2:
            for c_idx, (x0, x1) in enumerate(col_segments):
                crop_box = (x0, y0, x1, y1)
                cell = trans_img.crop(crop_box)
                bbox = cell.getbbox()
                if not bbox:
                    continue

                icon = cell.crop(bbox)
                iw, ih = icon.size
                if iw < 30 or ih < 30:
                    continue

                max_dim = max(iw, ih)
                canvas_size = 512
                square_canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
                scale = (canvas_size * 0.88) / max_dim
                new_w = max(1, int(iw * scale))
                new_h = max(1, int(ih * scale))
                icon_resized = icon.resize((new_w, new_h), Image.Resampling.LANCZOS)

                paste_x = (canvas_size - new_w) // 2
                paste_y = (canvas_size - new_h) // 2
                square_canvas.paste(icon_resized, (paste_x, paste_y), icon_resized)

                sliced_count += 1
                icon_filename = f"{base_name}_icon_{sliced_count:02d}_{canvas_size}px.png"
                square_canvas.save(out_dir / icon_filename, "PNG")
        else:
            # 列が明確に分かれなかった場合は従来の均等グリッドでフォールバック
            cell_w = w / grid_cols
            cell_h = h / grid_rows
            for r in range(grid_rows):
                for c in range(grid_cols):
                    x0 = int(c * cell_w)
                    cy0 = int(r * cell_h)
                    x1 = int((c + 1) * cell_w)
                    cy1 = int((r + 1) * cell_h)

                    cell = trans_img.crop((x0, cy0, x1, cy1))
                    bbox = cell.getbbox()
                    if not bbox:
                        continue

                    icon = cell.crop(bbox)
                    iw, ih = icon.size
                    if iw < 40 or ih < 40:
                        continue

                    max_dim = max(iw, ih)
                    canvas_size = 512
                    square_canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
                    scale = (canvas_size * 0.88) / max_dim
                    new_w = max(1, int(iw * scale))
                    new_h = max(1, int(ih * scale))
                    icon_resized = icon.resize((new_w, new_h), Image.Resampling.LANCZOS)

                    paste_x = (canvas_size - new_w) // 2
                    paste_y = (canvas_size - new_h) // 2
                    square_canvas.paste(icon_resized, (paste_x, paste_y), icon_resized)

                    sliced_count += 1
                    icon_filename = f"{base_name}_icon_{sliced_count:02d}_{canvas_size}px.png"
                    square_canvas.save(out_dir / icon_filename, "PNG")

    # もし1個もスライスできなかった場合の安全策（画像全体から有効領域を1枚の正方形として保存）
    if sliced_count == 0:
        overall_bbox = trans_img.getbbox()
        if overall_bbox:
            icon = trans_img.crop(overall_bbox)
            iw, ih = icon.size
            max_dim = max(iw, ih)
            canvas_size = 512
            square_canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
            scale = (canvas_size * 0.90) / max_dim
            new_w = max(1, int(iw * scale))
            new_h = max(1, int(ih * scale))
            icon_resized = icon.resize((new_w, new_h), Image.Resampling.LANCZOS)
            paste_x = (canvas_size - new_w) // 2
            paste_y = (canvas_size - new_h) // 2
            square_canvas.paste(icon_resized, (paste_x, paste_y), icon_resized)
            sliced_count = 1
            square_canvas.save(out_dir / f"{base_name}_icon_01_{canvas_size}px.png", "PNG")

    print(f"  🔪 [自動適応スライス完了]: {sliced_count}個の透過アイコン（{out_dir.name}/）")
    return sliced_count

def process_folder(target_folder):
    """フォルダ内の全アセット画像を一括処理"""
    folder = Path(target_folder).resolve()
    if not folder.exists():
        print(f"❌ フォルダが見つかりません: {folder}")
        return

    print(f"==================================================")
    print(f"🎮 [Game Assets] 透過＆スライス処理開始: {folder.name}")
    print(f"==================================================")

    img_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg')]
    # 既に生成した透過画像やスライスは除外
    targets = [f for f in img_files if not f.name.endswith('_transparent.png') and not f.name.startswith('icon_')]

    slices_dir = folder / "transparent_icons"
    slices_dir.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    for img_path in sorted(targets):
        print(f"\n📦 処理中: {img_path.name}")
        base_name = img_path.stem

        # 1. 透過PNGの生成
        trans_path = folder / f"{base_name}_transparent.png"
        trans_img = make_transparent_luma(img_path, trans_path)
        if trans_img is None:
            continue

        processed_count += 1

        # 2. アイコン・UIパックの場合は個別スライスも実行
        # ファイル名やカテゴリから判定（bg/background以外はスライス実行）
        if "bg_" not in base_name and "background" not in base_name:
            auto_slice_icons(trans_img, base_name, slices_dir, grid_cols=4, grid_rows=2)

    # 3. 配布用ZIPの自動パッケージング
    zip_name = f"{folder.name}_Complete_Pack.zip"
    zip_path = folder / zip_name
    print(f"\n📦 配布用ZIPを作成中: {zip_name} ...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 透過PNGマスターシート
        for f in folder.glob("*_transparent.png"):
            zf.write(f, arcname=f"Master_Sheets/{f.name}")
        # スライス済み透過アイコン
        for f in slices_dir.glob("*.png"):
            zf.write(f, arcname=f"Individual_Icons/{f.name}")
        # 元画像
        for f in targets:
            zf.write(f, arcname=f"Original_Art/{f.name}")

    print(f"🎉 【完了】すべての透過PNGとZIPパックが完成しました！")
    print(f"👉 保存場所: {folder}")
    print(f"🎁 配布用ZIP: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # デフォルトは最新のGame-Assets outputsフォルダ
        root_out = Path("/Users/base/Automated-Projects/Game-Assets/outputs")
        subdirs = [d for d in root_out.iterdir() if d.is_dir()] if root_out.exists() else []
        if subdirs:
            target = str(sorted(subdirs)[-1])
        else:
            target = str(root_out)
    process_folder(target)
