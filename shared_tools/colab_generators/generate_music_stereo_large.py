#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する 世界最高峰ステレオ音楽生成スクリプト
モデル: Meta MusicGen Stereo-Large (3.3B パラメータ / 32kHz Stereo)
"""
import os
import time
import subprocess
import sys

def setup_environment():
    print("📦 [1/4] 必要なライブラリのインストール...", flush=True)
    pkgs = [
        "torch",
        "transformers",
        "accelerate",
        "scipy",
        "soundfile",
        "sentencepiece"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_music_generation():
    import torch
    import scipy.io.wavfile
    from transformers import AutoProcessor, MusicgenForConditionalGeneration

    print("🚀 [2/4] 世界最高峰モデル Meta MusicGen Stereo-Large (3.3B) のロード (A100 GPU / fp16)...", flush=True)
    t0 = time.time()
    
    processor = AutoProcessor.from_pretrained("facebook/musicgen-stereo-large")
    model = MusicgenForConditionalGeneration.from_pretrained(
        "facebook/musicgen-stereo-large",
        torch_dtype=torch.float16
    ).to("cuda")
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    print(f"✅ MusicGen Stereo-Large ロード完了 ({time.time() - t0:.2f}秒 / Sampling Rate: {sampling_rate}Hz)", flush=True)

    # 出力ディレクトリ
    output_dir = "/content/music_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # YouTube 3大チャンネル確定コンセプト プロンプト (30秒ステレオ楽曲)
    test_prompts = [
        {
            "id": "ch1_haven_chill_music",
            "title": "Ch1: Haven Chill (Midnight Rainy Felt Piano & Cozy Lo-Fi Beat)",
            "prompt": "Warm vintage felt piano chords, cozy midnight lofi hip hop beat, gentle raindrops on window, vinyl crackle, soothing atmospheric Rhodes, deep mellow bassline, peaceful night study ambience, 70 BPM, stereo width, high quality production."
        },
        {
            "id": "ch2_velvet_sunset_music",
            "title": "Ch2: Velvet Sunset (Sunset Pop & Smooth R&B Groove)",
            "prompt": "Smooth modern R&B pop groove, lush 80s synth chords, groovy bassline, crisp snappy drums, romantic sunset mood, soulful melodic hooks, city night cruising vibe, 102 BPM, polished studio mastering, rich stereo imaging."
        },
        {
            "id": "ch3_auramelody_music",
            "title": "Ch3: AuraMelody (Sunshine Tropical Feel-Good Pop)",
            "prompt": "Uplifting feel-good tropical pop, bright acoustic guitar strums, breezy marimba melody, energetic bouncy bass, crisp punchy drums, joyful summer sunshine anthem, refreshing festival vibes, 126 BPM, crystal clear high end, wide stereo."
        }
    ]

    print("\n🎵 [3/4] ステレオ音楽生成の開始 (各30秒ステレオ音源)...", flush=True)
    generated_files = []

    for idx, item in enumerate(test_prompts, 1):
        print(f"\n--- [{idx}/{len(test_prompts)}] 生成中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        inputs = processor(
            text=[item["prompt"]],
            padding=True,
            return_tensors="pt"
        ).to("cuda")
        
        # 1500 tokens ≈ 30秒のステレオ音源
        audio_values = model.generate(
            **inputs,
            do_sample=True,
            guidance_scale=3.0,
            max_new_tokens=1500
        )
        
        # [batch, channels, time] -> numpy [time, channels]
        audio_data = audio_values[0].cpu().float().numpy()
        if audio_data.ndim == 2:
            audio_data = audio_data.T  # (channels, time) -> (time, channels)
            
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.wav")
        scipy.io.wavfile.write(out_path, rate=sampling_rate, data=audio_data)
        generated_files.append(out_path)
        print(f"✨ 音楽生成完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] 全ステレオ楽曲の生成が正常に完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_files}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_music_generation()
