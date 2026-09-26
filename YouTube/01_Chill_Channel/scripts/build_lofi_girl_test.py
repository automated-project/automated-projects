import subprocess
import os

def render_lofi_test():
    video_input = "/Users/base/Automated-Projects/YouTube/01_Chill_Channel/cover_art/Girl_studying_at_desk_20260922021250.mp4"
    audio1 = "/Users/base/Automated-Projects/YouTube/01_Chill_Channel/Lofi-Mix/Coffee_by_the_Window.mp4"
    audio2 = "/Users/base/Automated-Projects/YouTube/01_Chill_Channel/Lofi-Mix/Sunday_Morning_Stream.mp4"
    output_dir = "/Users/base/Automated-Projects/YouTube/01_Chill_Channel/output_videos"
    os.makedirs(output_dir, exist_ok=True)
    output_video = os.path.join(output_dir, "lofi_ghibli_girl_loop_test.mp4")

    print(f"🎬 Starting render with video: {video_input}")
    print(f"🎵 Audio 1: {audio1}")
    print(f"🎵 Audio 2: {audio2}")

    # ffmpeg command:
    # 1. Loop input video infinitely (-stream_loop -1)
    # 2. Input audio1 and audio2
    # 3. Apply 2.5s acrossfade between audio1 and audio2
    # 4. Scale video to 1920x1080 Full HD
    # 5. Output with -shortest to match audio length
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", video_input,
        "-i", audio1,
        "-i", audio2,
        "-filter_complex",
        "[1:a][2:a]acrossfade=d=2.5:c1=esin:c2=esin[aout];[0:v]scale=1920:1080:flags=lanczos[vout]",
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        output_video
    ]

    print("Running ffmpeg...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error during ffmpeg:")
        print(res.stderr)
        return False

    print(f"✅ Successfully created: {output_video}")

    # Extract preview frame
    preview_img = "/Users/base/.gemini/antigravity/brain/155a7193-a8f4-44d7-80ea-176734dc875d/preview_ghibli_girl_loop.jpg"
    thumb_cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:05",
        "-i", output_video,
        "-vframes", "1",
        "-q:v", "2",
        preview_img
    ]
    subprocess.run(thumb_cmd, capture_output=True)
    print(f"📸 Preview frame saved to {preview_img}")
    return True

if __name__ == "__main__":
    render_lofi_test()
