#!/bin/zsh
# Adobe Stock用 動画一括アップスケールスクリプト（重複スキップ対応版）
# 使い方: ./tools/upscale_video.sh <入力動画ファイルまたはフォルダ> <出力先フォルダ>

INPUT=$1
OUTPUT_DIR=$2

if [ -z "$INPUT" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <input_video_or_dir> <output_dir>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR=$(cd "$OUTPUT_DIR"; pwd)

TOOL_DIR="$(cd "$(dirname "$0")/realesrgan" && pwd)"
MODEL_DIR="$TOOL_DIR/models"
FFMPEG_BIN="/opt/homebrew/bin/ffmpeg"
FFPROBE_BIN="/opt/homebrew/bin/ffprobe"

if [ ! -x "$FFMPEG_BIN" ]; then
    FFMPEG_BIN="ffmpeg"
    FFPROBE_BIN="ffprobe"
fi

upscale_single_video() {
    local video_file="$1"
    local base_name=$(basename -- "$video_file")
    local name="${base_name%.*}"
    local ext="${base_name##*.}"
    local output_file="$OUTPUT_DIR/${name}_4k_upscaled.mp4"

    # すでにアップスケール済みの場合はスキップ
    if [ -f "$output_file" ]; then
        echo "Skipping video: $base_name (already upscaled: $output_file)"
        return 0
    fi

    echo "=========================================="
    echo "Processing video: $video_file"
    echo "Output target: $output_file"
    echo "=========================================="

    local tmp_dir="/tmp/esrgan_video_${name}_$$"
    local frames_in="$tmp_dir/in"
    local frames_out="$tmp_dir/out"
    mkdir -p "$frames_in" "$frames_out"

    # FPSを取得
    local fps=$($FFPROBE_BIN -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "$video_file")
    if [ -z "$fps" ]; then
        fps="30"
    fi
    echo "Detected FPS: $fps"

    # フレーム分割（連番PNG）
    echo "Step 1/3: Extracting frames..."
    $FFMPEG_BIN -y -i "$video_file" -qscale:v 1 "$frames_in/frame_%06d.png" > /dev/null 2>&1

    # Real-ESRGANによる全フレーム超解像処理
    echo "Step 2/3: Upscaling frames with GPU (Real-ESRGAN x4plus)..."
    cd "$TOOL_DIR" || exit 1
    ./realesrgan-ncnn-vulkan -i "$frames_in" -o "$frames_out" -s 4 -m "$MODEL_DIR" -n realesrgan-x4plus

    # ffmpegで再結合（高画質H.264, yuv420p）
    echo "Step 3/3: Re-assembling video into 4K MP4..."
    $FFMPEG_BIN -y -r "$fps" -i "$frames_out/frame_%06d.png" -c:v libx264 -crf 17 -pix_fmt yuv420p "$output_file" > /dev/null 2>&1

    # 一時ファイル削除
    rm -rf "$tmp_dir"
    echo "Completed: $output_file"
}

if [ -f "$INPUT" ]; then
    upscale_single_video "$INPUT"
elif [ -d "$INPUT" ]; then
    for v in "$INPUT"/*.{mp4,mov,m4v}(N); do
        if [ -f "$v" ]; then
            upscale_single_video "$v"
        fi
    done
else
    echo "Error: Input not found: $INPUT"
    exit 1
fi

echo "All video upscaling jobs completed!"
