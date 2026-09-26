import subprocess
from pathlib import Path

raw_file = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel/raw_audio/Hands_Turn_Slowly.mp4")
out_dir = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel/mastered_audio_test")
out_dir.mkdir(parents=True, exist_ok=True)

# 1. 現行（自然系クリア）
eq_current = (
    "equalizer=f=55:t=q:w=1.2:g=7.0,"
    "equalizer=f=110:t=q:w=1.2:g=4.5,"
    "equalizer=f=280:t=q:w=1.0:g=-2.5,"
    "equalizer=f=4500:t=q:w=1.0:g=3.5,"
    "equalizer=f=10000:t=q:w=1.0:g=8.0,"
    "equalizer=f=15000:t=q:w=1.0:g=8.5,"
    "alimiter=limit=0.96"
)

# 2. Super Crisp Festival V-Shape（PhonkForge並みのキック重低音＋シンセ煌めき）
eq_super_crisp = (
    "equalizer=f=50:t=q:w=1.4:g=9.5,"
    "equalizer=f=100:t=q:w=1.2:g=6.0,"
    "equalizer=f=250:t=q:w=1.0:g=-3.0,"
    "equalizer=f=3500:t=q:w=1.0:g=4.0,"
    "equalizer=f=8000:t=q:w=1.0:g=7.5,"
    "equalizer=f=12000:t=q:w=1.0:g=9.0,"
    "equalizer=f=16000:t=q:w=1.0:g=9.5,"
    "alimiter=limit=0.95"
)

subprocess.run(["ffmpeg", "-y", "-i", str(raw_file), "-af", eq_current, "-b:a", "320k", str(out_dir / "Hands_Turn_Slowly_Current.mp3")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["ffmpeg", "-y", "-i", str(raw_file), "-af", eq_super_crisp, "-b:a", "320k", str(out_dir / "Hands_Turn_Slowly_SuperCrispVocalMaster.mp3")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Generated comparison audio files!")
