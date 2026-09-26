#!/usr/bin/env python3
"""
Colab A100 GPU上で仮想ディスプレイ(Xvfb)を用いて Blender Eevee/Cycles レンダリングを完全成功させるスクリプト
"""
import os
import sys
import time
import subprocess

def setup_environment():
    print("📦 [1/4] Xvfb (仮想ディスプレイ) & Blender 4.2 LTS のセットアップ...", flush=True)
    # 1. 仮想ディスプレイ(Xvfb)とOpenGLライブラリのインストール
    subprocess.check_call(["apt-get", "update", "-qq"])
    subprocess.check_call(["apt-get", "install", "-y", "-qq", "xvfb", "libgl1-mesa-dri", "libglib2.0-0", "freeglut3-dev"])
    
    # 2. Blender 4.2 LTS ダウンロード
    if not os.path.exists("/content/blender-4.2.0-linux-x64/blender"):
        url = "https://download.blender.org/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz"
        subprocess.check_call(["wget", "-q", "-c", url, "-O", "/content/blender.tar.xz"])
        subprocess.check_call(["tar", "-xf", "/content/blender.tar.xz", "-C", "/content"])
    print("✅ Xvfb & Blenderセットアップ完了！", flush=True)

def create_blender_scene():
    script_content = '''
import bpy
import math
import os

def build_scene():
    print("🚀 Building High-Level Satisfying Marble Scene for Colab...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 60
    scene.render.fps = 30
    
    # 剛体シミュレーション
    bpy.ops.rigidbody.world_add()
    rb = scene.rigidbody_world
    rb.substeps_per_frame = 20
    
    # マテリアル
    mat_gold = bpy.data.materials.new(name="Mat_Gold")
    mat_gold.use_nodes = True
    bsdf = mat_gold.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.75, 0.1, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.95
        bsdf.inputs['Roughness'].default_value = 0.1

    mat_ball = bpy.data.materials.new(name="Mat_Ball")
    mat_ball.use_nodes = True
    bsdf_b = mat_ball.node_tree.nodes.get("Principled BSDF")
    if bsdf_b:
        bsdf_b.inputs['Base Color'].default_value = (0.1, 0.5, 1.0, 1.0)
        bsdf_b.inputs['Roughness'].default_value = 0.05
        bsdf_b.inputs['Metallic'].default_value = 0.9

    # レール（パッシブ）
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    ramp = bpy.context.active_object
    ramp.scale = (2.0, 10.0, 0.1)
    ramp.rotation_euler = (math.radians(20), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    bpy.ops.rigidbody.object_add()
    ramp.rigid_body.type = 'PASSIVE'
    ramp.data.materials.append(mat_gold)

    # ボール（アクティブ）
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 3.5, 3.0))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.type = 'ACTIVE'
    ball.data.materials.append(mat_ball)

    # ライティング & カメラ
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 4.0

    bpy.ops.object.camera_add(location=(0, -8, 5), rotation=(math.radians(65), 0, 0))
    scene.camera = bpy.context.active_object

    # レンダリング設定 (Eevee)
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderSettings') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.resolution_x = 720
    scene.render.resolution_y = 1280
    
    os.makedirs("/content/blender_renders", exist_ok=True)
    scene.render.filepath = "/content/blender_renders/frame_"
    scene.render.image_settings.file_format = 'PNG'

    # ベイク
    bpy.ops.ptcache.bake_all(bake=True)

build_scene()
'''
    with open("/content/make_scene.py", "w") as f:
        f.write(script_content)

def run_colab_render():
    print("🚀 [2/4] Colab上でシーン構築...", flush=True)
    blender_bin = "/content/blender-4.2.0-linux-x64/blender"
    create_blender_scene()
    
    # Xvfb(仮想ディスプレイ)経由でBlenderを実行してOpenGLエラーを完全回避
    cmd_build = ["xvfb-run", "-a", blender_bin, "-b", "-P", "/content/make_scene.py", "--python-expr", "import bpy; bpy.ops.wm.save_as_mainfile(filepath='/content/scene.blend')"]
    subprocess.check_call(cmd_build)

    print("🎬 [3/4] Xvfb + Colab GPU で Eevee 60フレーム レンダリング中...", flush=True)
    cmd_render = ["xvfb-run", "-a", blender_bin, "-b", "/content/scene.blend", "-s", "1", "-e", "60", "-a"]
    proc = subprocess.Popen(cmd_render, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        if "Saved:" in line:
            print(line.strip(), flush=True)
    proc.wait()

    print("🎞️ [4/4] FFmpeg で Colab上 MP4 動画変換中...", flush=True)
    os.makedirs("/content/blender_outputs", exist_ok=True)
    out_mp4 = "/content/blender_outputs/colab_satisfying_render.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-framerate", "30",
        "-i", "/content/blender_renders/frame_%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        out_mp4
    ]
    subprocess.check_call(cmd_ffmpeg)
    print(f"🎉 Colabレンダリング成功！ 出力: {out_mp4}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_colab_render()
