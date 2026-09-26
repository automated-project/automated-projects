import cv2
import numpy as np
import os
import random
from PIL import Image

def generate_rain_window_video():
    img_path = "/Users/base/Downloads/Gemini_Generated_Image_cdtzficdtzficdtz.jpeg"
    output_dir = "/Users/base/Automated-Projects/YouTube/01_Dark_Fantasy_Channel/output_videos/test_rain"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_rainy_window_10s.mp4")

    # 画像読み込み (1920x1080にリサイズ)
    base_img = cv2.imread(img_path)
    base_img = cv2.resize(base_img, (1920, 1080))
    h, w, _ = base_img.shape

    # 窓のマスク作成 (左側エリア: 窓の部分にのみ雨を適用)
    # 窓領域: 左端〜中央付近 (x: 0 ~ 970, y: 0 ~ 760)
    window_mask = np.zeros((h, w), dtype=np.float32)
    
    # 窓ガラスのポリゴン領域
    pts_left_window = np.array([[120, 0], [590, 0], [580, 720], [120, 720]], np.int32)
    pts_right_window = np.array([[640, 20], [950, 40], [940, 650], [640, 680]], np.int32)
    
    cv2.fillPoly(window_mask, [pts_left_window, pts_right_window], 1.0)
    # 窓枠の外側にも少し柔らかくブレンド (全体的に窓の外をカバー)
    window_mask = cv2.GaussianBlur(window_mask, (21, 21), 0)

    fps = 30
    duration_sec = 10
    total_frames = fps * duration_sec

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    # 水滴オブジェクトの定義 (静止水滴 + スライド水滴)
    num_static_drops = 250
    static_drops = []
    for _ in range(num_static_drops):
        x = random.randint(100, 960)
        y = random.randint(10, 720)
        r = random.uniform(1.2, 3.5)
        static_drops.append((x, y, r))

    num_sliding_drops = 25
    sliding_drops = []
    for _ in range(num_sliding_drops):
        x = random.randint(130, 930)
        y = random.randint(-200, 600)
        speed = random.uniform(2.5, 6.0)
        r = random.uniform(2.0, 4.5)
        sliding_drops.append({'x': x, 'y': y, 'speed': speed, 'r': r, 'trail': []})

    # 雨筋 (Falling streaks)
    num_streaks = 70
    streaks = []
    for _ in range(num_streaks):
        x = random.randint(100, 980)
        y = random.randint(-500, 750)
        speed = random.uniform(22, 38)
        length = random.randint(15, 35)
        streaks.append({'x': x, 'y': y, 'speed': speed, 'length': length})

    print("Rendering rain animation...")
    for frame_idx in range(total_frames):
        frame = base_img.copy().astype(np.float32)
        rain_layer = np.zeros((h, w, 3), dtype=np.float32)

        # 1. 落下する雨筋 (Streaks)
        for s in streaks:
            s['y'] += s['speed']
            if s['y'] > 750:
                s['y'] = random.randint(-50, 0)
                s['x'] = random.randint(100, 980)
            
            pt1 = (int(s['x']), int(s['y']))
            pt2 = (int(s['x'] + 2), int(s['y'] + s['length']))
            cv2.line(rain_layer, pt1, pt2, (180, 200, 220), 1)

        # 2. 静止水滴の描画 (光の屈折感)
        for x, y, r in static_drops:
            # 水滴のハイライトと影
            cv2.circle(rain_layer, (int(x), int(y)), int(r), (140, 160, 180), -1)
            cv2.circle(rain_layer, (int(x - 0.5), int(y - 0.5)), int(max(1, r * 0.5)), (230, 240, 255), -1)

        # 3. 窓を伝い落ちる水滴 (Sliding Drops with Trails)
        for d in sliding_drops:
            d['y'] += d['speed']
            # 水滴が時折加速したり止まったりするリアルな動き
            if random.random() < 0.15:
                d['speed'] = random.uniform(1.0, 7.0)
            
            d['trail'].append((int(d['x']), int(d['y'])))
            if len(d['trail']) > 15:
                d['trail'].pop(0)

            if d['y'] > 740:
                d['y'] = random.randint(-100, 0)
                d['x'] = random.randint(130, 930)
                d['trail'] = []
                d['speed'] = random.uniform(2.5, 6.0)

            # 軌跡の描画
            for idx, (tx, ty) in enumerate(d['trail']):
                trail_r = max(1, int(d['r'] * (idx / len(d['trail'])) * 0.6))
                cv2.circle(rain_layer, (tx, ty), trail_r, (160, 180, 200), -1)

            # 水滴本体
            cv2.circle(rain_layer, (int(d['x']), int(d['y'])), int(d['r']), (180, 200, 220), -1)
            cv2.circle(rain_layer, (int(d['x'] - 1), int(d['y'] - 1)), int(max(1, d['r'] * 0.5)), (255, 255, 255), -1)

        # ガウスぼかしを微かにかけて柔らかく
        rain_layer = cv2.GaussianBlur(rain_layer, (3, 3), 0)

        # 窓マスクの適用
        for c in range(3):
            rain_applied = cv2.addWeighted(frame[:, :, c], 1.0, rain_layer[:, :, c], 0.45, 0)
            frame[:, :, c] = frame[:, :, c] * (1.0 - window_mask) + rain_applied * window_mask

        # 微小な呼吸のような光の揺らぎ (Ambient Pulse)
        ambient_factor = 1.0 + 0.015 * np.sin(2 * np.pi * frame_idx / (fps * 4))
        frame[:, 960:, :] = np.clip(frame[:, 960:, :] * ambient_factor, 0, 255)

        out.write(np.clip(frame, 0, 255).astype(np.uint8))

    out.release()
    print(f"Done! Saved to {output_path}")

    # H.264に変換してMac QuickTime等で再生可能にする
    h264_path = output_path.replace(".mp4", "_h264.mp4")
    cmd = f"ffmpeg -y -i {output_path} -c:v libx264 -pix_fmt yuv420p {h264_path}"
    os.system(cmd)
    print(f"H.264 version: {h264_path}")

if __name__ == "__main__":
    generate_rain_window_video()
