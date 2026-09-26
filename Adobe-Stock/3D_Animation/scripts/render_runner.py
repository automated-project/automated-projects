import bpy
import os
import glob
from pathlib import Path

frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_race_v1")
existing = glob.glob(str(frames_dir / "frame_*.png"))
rendered_count = len(existing)
print(f"Current rendered frames: {rendered_count}")

# 最後にレンダリングされたフレーム番号を特定
max_frame = 0
for f in existing:
    try:
        num = int(Path(f).stem.split('_')[1])
        if num > max_frame:
            max_frame = num
    except:
        pass

start_f = max_frame + 1 if max_frame < 540 else 1
end_f = 540

if start_f <= end_f:
    print(f"Rendering from frame {start_f} to {end_f}...")
    scene = bpy.context.scene
    scene.frame_start = start_f
    scene.frame_end = end_f
    scene.eevee.taa_render_samples = 16
    bpy.ops.render.render(animation=True)
    print("All frames rendered successfully!")
else:
    print("All 540 frames are already rendered.")
