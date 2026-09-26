import bpy
from pathlib import Path

blend_file = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/marble_run_race_flow.blend")
bpy.ops.wm.open_mainfile(filepath=str(blend_file))

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 270 # 9秒間 (ゴール判定＆余韻)
scene.eevee.taa_render_samples = 16

frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_flow_race")
frames_dir.mkdir(parents=True, exist_ok=True)
scene.render.filepath = str(frames_dir / "frame_")

print("Rendering 270 frames of high-speed marble race...")
bpy.ops.render.render(animation=True)
print("Render finished!")
