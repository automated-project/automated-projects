import cv2
import numpy as np
import os
import random

def generate_perfect_window_rain():
    img_path = "/Users/base/Downloads/Gemini_Generated_Image_cdtzficdtzficdtz.jpeg"
    output_dir = "/Users/base/Automated-Projects/YouTube/01_Dark_Fantasy_Channel/output_videos/test_rain"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_rain_perfect_mask.mp4")

    # 1920x1080で処理
    base_img = cv2.imread(img_path)
    base_img = cv2.resize(base_img, (1920, 1080))
    h, w, _ = base_img.shape

    # 【精密マスク作成】
    # 窓ガラスの内側だけに厳密に限定（窓枠サッシ・カーテン・壁・机には1pxもはみ出さない）
    # 元解像度(2752x1536) -> 1920x1080比率変換 (x*1920/2752, y*1080/1536)
    window_mask = np.zeros((h, w), dtype=np.float32)

    # 左ガラス板の内側 (四角形)
    pts_left = np.array([
        [150, 15],   # 左上
        [570, 15],   # 右上
        [570, 725],  # 右下
        [150, 725]   # 左下
    ], np.int32)

    # 右ガラス板の内側 (四角形)
    pts_right = np.array([
        [640, 30],   # 左上
        [935, 45],   # 右上
        [935, 665],  # 右下
        [640, 675]   # 左下
    ], np.int32)

    cv2.fillPoly(window_mask, [pts_left, pts_right], 1.0)
    
    # 窓枠との境界をわずか2pxだけ馴染ませる（はみ出さないソフトエッジ）
    window_mask = cv2.GaussianBlur(window_mask, (5, 5), 0)

    fps = 30
    duration_sec = 10
    total_frames = fps * duration_sec

    # 静止水滴（左窓・右窓の範囲内のみに生成）
    static_drops = []
    for _ in range(300):
        # 左または右の窓パネルを選択
        if random.random() < 0.6:
            x = random.randint(155, 565)
            y = random.randint(20, 720)
        else:
            x = random.randint(645, 930)
            y = random.randint(40, 660)
        r = random.uniform(1.2, 3.2)
        static_drops.append((x, y, r))

    # スライド水滴（垂れ落ちる水滴）
    sliding_drops = []
    for _ in range(20):
        if random.random() < 0.6:
            x = random.randint(160, 560)
            max_y = 720
        else:
            x = random.randint(650, 925)
            max_y = 660
        y = random.randint(-150, 500)
        speed = random.uniform(2.0, 5.0)
        r = random.uniform(2.0, 3.8)
        sliding_drops.append({'x': x, 'y': y, 'speed': speed, 'r': r, 'trail': [], 'max_y': max_y})

    # 雨脚（外を流れる雨）
    streaks = []
    for _ in range(80):
        if random.random() < 0.6:
            x = random.randint(150, 570)
            max_y = 725
        else:
            x = random.randint(640, 935)
            max_y = 670
        y = random.randint(-300, max_y)
        speed = random.uniform(25, 40)
        length = random.randint(12, 28)
        streaks.append({'x': x, 'y': y, 'speed': speed, 'length': length, 'max_y': max_y})

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    print("Rendering perfectly masked rain...")
    for frame_idx in range(total_frames):
        frame = base_img.copy().astype(np.float32)
        rain_layer = np.zeros((h, w, 3), dtype=np.float32)

        # 1. 落下する雨脚
        for s in streaks:
            s['y'] += s['speed']
            if s['y'] > s['max_y']:
                s['y'] = random.randint(-40, 0)
            
            pt1 = (int(s['x']), int(s['y']))
            pt2 = (int(s['x'] + 1), int(s['y'] + s['length']))
            cv2.line(rain_layer, pt1, pt2, (190, 210, 230), 1)

        # 2. 静止水滴
        for x, y, r in static_drops:
            cv2.circle(rain_layer, (int(x), int(y)), int(r), (140, 160, 180), -1)
            cv2.circle(rain_layer, (int(x - 0.5), int(y - 0.5)), int(max(1, r * 0.5)), (230, 240, 255), -1)

        # 3. 垂れ落ちる水滴 (Trails)
        for d in sliding_drops:
            d['y'] += d['speed']
            if random.random() < 0.12:
                d['speed'] = random.uniform(1.0, 6.0)
            
            d['trail'].append((int(d['x']), int(d['y'])))
            if len(d['trail']) > 12:
                d['trail'].pop(0)

            if d['y'] > d['max_y']:
                d['y'] = random.randint(-80, 0)
                d['trail'] = []
                d['speed'] = random.uniform(2.0, 5.0)

            for idx, (tx, ty) in enumerate(d['trail']):
                trail_r = max(1, int(d['r'] * (idx / len(d['trail'])) * 0.5))
                cv2.circle(rain_layer, (tx, ty), trail_r, (150, 170, 190), -1)

            cv2.circle(rain_layer, (int(d['x']), int(d['y'])), int(d['r']), (180, 200, 220), -1)
            cv2.circle(rain_layer, (int(d['x'] - 1), int(d['y'] - 1)), int(max(1, d['r'] * 0.5)), (255, 255, 255), -1)

        rain_layer = cv2.GaussianBlur(rain_layer, (3, 3), 0)

        # 厳密な窓マスクで合成（窓枠・カーテン・壁には一切描画されない）
        for c in range(3):
            rain_applied = cv2.addWeighted(frame[:, :, c], 1.0, rain_layer[:, :, c], 0.40, 0)
            frame[:, :, c] = frame[:, :, c] * (1.0 - window_mask) + rain_applied * window_mask

        # アンビエント微小光揺らぎ（右側のランプ周り）
        ambient_factor = 1.0 + 0.012 * np.sin(2 * np.pi * frame_idx / (fps * 4))
        frame[:, 1000:, :] = np.clip(frame[:, 1000:, :] * ambient_factor, 0, 255)

        out.write(np.clip(frame, 0, 255).astype(np.uint8))

    out.release()
    print(f"Done rendering! Output: {output_path}")

    # H.264エンコード
    h264_path = output_path.replace(".mp4", "_h264.mp4")
    os.system(f"ffmpeg -y -i {output_path} -c:v libx264 -pix_fmt yuv420p {h264_path}")
    print(f"H.264 version: {h264_path}")

if __name__ == "__main__":
    generate_perfect_window_rain()
