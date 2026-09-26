#!/bin/zsh
# Adobe Stock用一括アップスケールスクリプト（重複スキップ対応版）
# 使い方: ./upscale_all.sh <入力フォルダ> <出力フォルダ>

INPUT_DIR=$1
OUTPUT_DIR=$2

if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <input_dir> <output_dir>"
    exit 1
fi

# 絶対パスに変換
INPUT_DIR=$(cd "$INPUT_DIR"; pwd)
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR=$(cd "$OUTPUT_DIR"; pwd)

TOOL_DIR="$(cd "$(dirname "$0")/realesrgan" && pwd)"
MODEL_DIR="$TOOL_DIR/models"

cd "$TOOL_DIR" || exit 1

echo "Starting upscaling process..."
echo "Input: $INPUT_DIR"
echo "Output: $OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{jpg,jpeg,png}(N); do
    if [ -f "$img" ]; then
        filename=$(basename -- "$img")
        name="${filename%.*}"
        ext="${filename##*.}"
        target_file="$OUTPUT_DIR/${name}_upscaled.${ext}"
        
        # すでにアップスケール済みの場合は重複実行をスキップ
        if [ -f "$target_file" ]; then
            echo "Skipping: $filename (already upscaled)"
            continue
        fi
        
        echo "Upscaling: $filename..."
        # モデルの絶対パスを指定し、高画質向けモデル(realesrgan-x4plus)を使用
        ./realesrgan-ncnn-vulkan -i "$img" -o "$target_file" -s 4 -m "$MODEL_DIR" -n realesrgan-x4plus
    fi
done

echo "All upscaling complete!"
