import os
import subprocess
import time

print("=== Colab GPU (NVENC) FFmpeg 検証スクリプト ===")

# Step 1: NVIDIA GPU 認識確認
print("\n[Step 1] GPU (nvidia-smi) 確認中...")
try:
    gpu_info = subprocess.check_output(["nvidia-smi"]).decode("utf-8")
    print(gpu_info.split("\n")[0])
    print(gpu_info.split("\n")[3])
    print("✅ GPUが正常に認識されています。")
except Exception as e:
    print(f"❌ GPU認識エラー: {e}")
    print("⚠️ Colabのランタイムタイプを 'T4 GPU' または 'GPU' に変更してください。")

# Step 2: NVENC対応 FFmpeg バイナリのセットアップ
print("\n[Step 2] NVENC対応 FFmpeg バイナリのセットアップ中...")
FFMPEG_BIN = "/content/colab-ffmpeg-cuda/ffmpeg"

if not os.path.exists(FFMPEG_BIN):
    print("NVENC対応FFmpegをダウンロード・配置しています...")
    cmd = """
    git clone https://github.com/Glyx/colab-ffmpeg-cuda.git /content/colab-ffmpeg-cuda
    chmod +x /content/colab-ffmpeg-cuda/ffmpeg
    chmod +x /content/colab-ffmpeg-cuda/ffprobe
    """
    subprocess.run(cmd, shell=True, check=True)

# Step 3: NVENC エンコーダー一覧チェック
print("\n[Step 3] h264_nvenc エンコーダー検証中...")
res = subprocess.check_output([FFMPEG_BIN, "-encoders"]).decode("utf-8")
if "h264_nvenc" in res:
    print("🎉 SUCCESS: h264_nvenc (NVIDIA GPU エンコーダー) が正常に利用可能です！")
else:
    print("❌ ERROR: h264_nvenc が見つかりませんでした。")

# Step 4: 4K 60fps 波形合成 ＆ GPUエンコード ベンチマークテスト (30秒間)
print("\n[Step 4] 4K (3840x2160) 60fps GPUエンコード ベンチマーク実行中...")
test_output = "/content/nvenc_test_4k.mp4"

# 4K背景(黒) + サンプル波形アニメーション(showwaves) + GPUエンコード(h264_nvenc)
ffmpeg_benchmark_cmd = [
    FFMPEG_BIN, "-y",
    "-f", "lavfi", "-i", "sine=frequency=440:duration=30",  # 30秒のテスト音声
    "-f", "lavfi", "-i", "color=c=black:s=3840x2160:r=60:d=30", # 4K 60fps 30秒背景
    "-filter_complex",
    "[0:a]showwaves=s=3840x300:mode=line:colors=0xffaa00[wave];[1:v][wave]overlay=0:H-h[v]",
    "-map", "[v]",
    "-map", "0:a",
    "-c:v", "h264_nvenc",      # ⭐ GPU ハードウェアエンコーダー使用
    "-preset", "p4",           # 高速・高品質バランスプリセット
    "-b:v", "12M",             # ビットレート 12Mbps
    "-c:a", "aac",
    "-b:a", "320k",
    test_output
]

start_time = time.time()
subprocess.run(ffmpeg_benchmark_cmd, check=True)
elapsed = time.time() - start_time

file_size_mb = os.path.getsize(test_output) / (1024 * 1024)
print(f"\n✨ ベンチマーク結果 ✨")
print(f"・生成ファイル: {test_output}")
print(f"・動画仕様: 4K (3840x2160) / 60fps / 30秒")
print(f"・ファイルサイズ: {file_size_mb:.2f} MB")
print(f"・GPUエンコード所要時間: {elapsed:.2f} 秒")
print(f"・処理スピード倍率: {30.0 / elapsed:.2f} x リアルタイム速度")
