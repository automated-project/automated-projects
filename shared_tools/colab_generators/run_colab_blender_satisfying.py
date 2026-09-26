#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する Blender 3D Eevee-Next 爆速 Satisfying 動画生成スクリプト
"""
import os
import sys
import time
import subprocess

def setup_blender():
    print("📦 [1/4] Blender 4.2 LTS のセットアップ...", flush=True)
    if not os.path.exists("/content/blender-4.2.0-linux-x64/blender"):
        url = "https://download.blender.org/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz"
        subprocess.check_call(["wget", "-q", "-c", url, "-O", "/content/blender.tar.xz"])
        subprocess.check_call(["tar", "-xf", "/content/blender.tar.xz", "-C", "/content"])
    print("✅ Blenderセットアップ完了！", flush=True)

def create_blender_scene_script():
    script_content = '''
import bpy
import math
import os

def create_eevee_satisfying_scene():
    print("🚀 Building Eevee-Next Fast Satisfying Scene...")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    fps = 30
    duration_sec = 3 # 3秒 (90フレーム)
    total_frames = fps * duration_sec
    
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps
    
    # 剛体ワールド設定
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.substeps_per_frame = 20
    rb_world.solver_iterations = 40
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames

    # マテリアル
    mat_track = bpy.data.materials.new(name="Mat_Track")
    mat_track.use_nodes = True
    bsdf = mat_track.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.06, 0.08, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.15
        bsdf.inputs['Metallic'].default_value = 0.8

    mat_gold = bpy.data.materials.new(name="Mat_Gold")
    mat_gold.use_nodes = True
    bsdf = mat_gold.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.78, 0.15, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.1
        bsdf.inputs['Metallic'].default_value = 0.95

    ball_colors = {
        "Red": (0.95, 0.05, 0.1, 1.0),
        "Blue": (0.05, 0.4, 1.0, 1.0),
        "Green": (0.05, 0.9, 0.15, 1.0),
        "Yellow": (1.0, 0.85, 0.0, 1.0),
    }
    ball_materials = {}
    for name, col in ball_colors.items():
        mat = bpy.data.materials.new(name=f"Mat_{name}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = col
            bsdf.inputs['Roughness'].default_value = 0.05
            bsdf.inputs['Metallic'].default_value = 0.95
        ball_materials[name] = mat

    def add_ramp(name, loc, size, rot_deg):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        ramp = bpy.context.active_object
        ramp.name = name
        ramp.scale = size
        ramp.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.rigidbody.object_add()
        ramp.rigid_body.type = 'PASSIVE'
        ramp.rigid_body.collision_shape = 'CONVEX_HULL'
        ramp.rigid_body.friction = 0.01
        ramp.rigid_body.restitution = 0.2
        ramp.data.materials.append(mat_track)
        return ramp

    def add_wall(name, loc, size, rot_deg):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        wall = bpy.context.active_object
        wall.name = name
        wall.scale = size
        wall.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.rigidbody.object_add()
        wall.rigid_body.type = 'PASSIVE'
        wall.rigid_body.collision_shape = 'CONVEX_HULL'
        wall.rigid_body.friction = 0.01
        wall.data.materials.append(mat_gold)
        return wall

    # コース構築
    add_ramp("Ramp_1", (0, 4.0, 18.5), (2.4, 12.0, 0.1), (24, 0, 0))
    add_wall("Ramp_1_Wall_L", (-1.2, 4.0, 19.3), (0.1, 12.2, 1.6), (24, 0, 0))
    add_wall("Ramp_1_Wall_R", (1.2, 4.0, 19.3), (0.1, 12.2, 1.6), (24, 0, 0))
    add_wall("Ramp_1_Wall_Back", (0, -1.8, 22.0), (2.5, 0.1, 2.0), (0, 0, 0))

    # ボール配置
    positions = [(-0.6, -1.0, 21.0), (-0.2, -1.0, 21.0), (0.2, -1.0, 21.0), (0.6, -1.0, 21.0)]
    for i, (name, pos) in enumerate(zip(["Red", "Blue", "Green", "Yellow"], positions)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=pos)
        ball = bpy.context.active_object
        ball.name = f"Ball_{name}"
        bpy.ops.object.shade_smooth()
        bpy.ops.rigidbody.object_add()
        ball.rigid_body.type = 'ACTIVE'
        ball.rigid_body.collision_shape = 'SPHERE'
        ball.rigid_body.mass = 1.0
        ball.rigid_body.friction = 0.005
        ball.rigid_body.restitution = 0.3
        ball.data.materials.append(ball_materials[name])

    # ライティング
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 30))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 25))
    area = bpy.context.active_object
    area.data.energy = 300.0
    area.data.size = 10.0

    # カメラ
    bpy.ops.object.camera_add(location=(0, -6.0, 24.0))
    camera = bpy.context.active_object
    camera.name = "Follow_Camera"
    camera.rotation_euler = (math.radians(52), 0, 0)
    scene.camera = camera

    # 【重要】Eevee (BLENDER_EEVEE_NEXT) エンジン設定
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderSettings') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920 # Shorts 9:16
    scene.render.resolution_percentage = 100
    
    out_frames = "/content/blender_renders/frame_"
    os.makedirs("/content/blender_renders", exist_ok=True)
    scene.render.filepath = out_frames
    scene.render.image_settings.file_format = 'PNG'

    # 物理ベイク
    print("⏳ Baking Physics...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics Baked Successfully!")

create_eevee_satisfying_scene()
'''
    with open("/content/make_scene.py", "w") as f:
        f.write(script_content)

def run_render():
    print("🚀 [3/4] Blender 3D シーン生成 & Eevee-Next 爆速レンダリング開始...", flush=True)
    t0 = time.time()
    
    blender_bin = "/content/blender-4.2.0-linux-x64/blender"
    create_blender_scene_script()
    
    # 1. シーン構築 & 物理ベイク
    cmd_build = [blender_bin, "-b", "-P", "/content/make_scene.py", "--python-expr", "import bpy; bpy.ops.wm.save_as_mainfile(filepath='/content/scene.blend')"]
    subprocess.check_call(cmd_build)
    
    # 2. 90フレーム (3秒) 爆速レンダリング
    print("🎬 Eevee-Next レンダリング実行中 (Frames 1 to 90)...", flush=True)
    cmd_render = [blender_bin, "-b", "/content/scene.blend", "-s", "1", "-e", "90", "-a"]
    proc = subprocess.Popen(cmd_render, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        if "Saved:" in line or "Render" in line or "Frame" in line:
            print(line.strip(), flush=True)
    proc.wait()
    
    # 3. FFmpegでMP4にエンコード
    print("🎞️ FFmpeg で 30fps MP4 にエンコード中...", flush=True)
    os.makedirs("/content/blender_outputs", exist_ok=True)
    out_mp4 = "/content/blender_outputs/eevee_satisfying_marble_3s.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-framerate", "30",
        "-i", "/content/blender_renders/frame_%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        out_mp4
    ]
    subprocess.check_call(cmd_ffmpeg)
    
    elapsed = time.time() - t0
    print(f"🎉 [4/4] 爆速レンダリング完了！ 出力: {out_mp4} (総所要時間: {elapsed:.2f}秒)", flush=True)

if __name__ == "__main__":
    setup_blender()
    run_render()
