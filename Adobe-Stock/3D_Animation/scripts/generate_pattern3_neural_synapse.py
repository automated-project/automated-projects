#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock ハイエンド商用3D素材 (Pattern 3)
テーマ：Neon Neural Synapse Network (神経回路網のようにパルスが走るネットワークコア)
仕様：4K UHD 3840x2160, 30fps, 3秒(90f) シームレスループ, コピースペース確保, 完全無音
"""

import os
import sys
import math
import shutil
import subprocess
import csv
from pathlib import Path
import bpy

OUTPUT_DIR = Path("/Users/base/Automated-Projects/Adobe-Stock/3D_Animation/renders")
FRAMES_DIR = OUTPUT_DIR / "pattern3_neural_synapse_frames"
FINAL_4K_VIDEO = OUTPUT_DIR / "neon_neural_synapse_4k_loop.mp4"
PREVIEW_PNG = OUTPUT_DIR / "preview_neon_neural_synapse.png"
CSV_FILE = OUTPUT_DIR / "adobe_stock_neural_synapse_submission.csv"
BLENDER_PROJECTS_DIR = Path("/Users/base/Automated-Projects/Adobe-Stock/3D_Animation/blender_projects")

def build_and_render(total_frames=90, fps=30):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BLENDER_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "NeuralSynapseScene"

    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps

    # 2. EEVEE ハイエンド設定
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene, 'eevee'):
        scene.eevee.taa_render_samples = 12
        if hasattr(scene.eevee, 'use_raytracing'):
            scene.eevee.use_raytracing = True

    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Punchy'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.quality = 96
    scene.render.filepath = str(FRAMES_DIR / "frame_")

    # 3. 背景・ワールド環境
    world = bpy.data.worlds.new("SynapseWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.006, 0.008, 0.018, 1.0)
    bg.inputs['Strength'].default_value = 0.5

    # 4. スタジオ照明
    bpy.ops.object.light_add(type='AREA', location=(4.0, -8.0, 7.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 1400.0
    key_light.data.size = 12.0
    key_light.data.color = (0.2, 0.7, 1.0)
    key_light.rotation_euler = (math.radians(50), math.radians(-10), 0)

    bpy.ops.object.light_add(type='AREA', location=(-2.0, 10.0, 5.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1600.0
    rim_light.data.size = 14.0
    rim_light.data.color = (0.8, 0.15, 1.0)
    rim_light.rotation_euler = (math.radians(-50), 0, 0)

    # 5. マテリアル
    # A. ノード球（発光ネオンマゼンタ＆シアン）
    mat_node_magenta = bpy.data.materials.new(name="MatNodeMagenta")
    mat_node_magenta.use_nodes = True
    bsdf_nm = mat_node_magenta.node_tree.nodes.get("Principled BSDF")
    bsdf_nm.inputs['Base Color'].default_value = (0.9, 0.1, 0.7, 1.0)
    if 'Emission Color' in bsdf_nm.inputs:
        bsdf_nm.inputs['Emission Color'].default_value = (1.0, 0.15, 0.8, 1.0)
        bsdf_nm.inputs['Emission Strength'].default_value = 4.0

    mat_node_cyan = bpy.data.materials.new(name="MatNodeCyan")
    mat_node_cyan.use_nodes = True
    bsdf_nc = mat_node_cyan.node_tree.nodes.get("Principled BSDF")
    bsdf_nc.inputs['Base Color'].default_value = (0.1, 0.85, 1.0, 1.0)
    if 'Emission Color' in bsdf_nc.inputs:
        bsdf_nc.inputs['Emission Color'].default_value = (0.15, 0.9, 1.0, 1.0)
        bsdf_nc.inputs['Emission Strength'].default_value = 4.5

    # B. シナプス接続ワイヤー（半透明ダーククローム）
    mat_synapse_wire = bpy.data.materials.new(name="MatSynapseWire")
    mat_synapse_wire.use_nodes = True
    bsdf_sw = mat_synapse_wire.node_tree.nodes.get("Principled BSDF")
    bsdf_sw.inputs['Base Color'].default_value = (0.2, 0.35, 0.6, 1.0)
    bsdf_sw.inputs['Metallic'].default_value = 0.95
    bsdf_sw.inputs['Roughness'].default_value = 0.1
    if 'Emission Color' in bsdf_sw.inputs:
        bsdf_sw.inputs['Emission Color'].default_value = (0.1, 0.4, 0.8, 1.0)
        bsdf_sw.inputs['Emission Strength'].default_value = 0.8

    # C. シナプスパルス粒子（高輝度発光）
    mat_pulse = bpy.data.materials.new(name="MatPulse")
    mat_pulse.use_nodes = True
    bsdf_p = mat_pulse.node_tree.nodes.get("Principled BSDF")
    bsdf_p.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    if 'Emission Color' in bsdf_p.inputs:
        bsdf_p.inputs['Emission Color'].default_value = (0.5, 0.95, 1.0, 1.0)
        bsdf_p.inputs['Emission Strength'].default_value = 10.0

    # 6. オブジェクト配置（右側配置、左側7割コピースペース）
    center_x = 2.5
    center_y = 0.0
    center_z = 0.0
    frames = range(1, total_frames + 1, 2)

    # 6.1 ニューラルネットワークノード（3D空間に配置）
    node_coords = [
        (0.0, 0.0, 0.0),
        (0.9, 0.8, 0.7),
        (-0.8, 0.7, -0.6),
        (0.7, -0.9, -0.5),
        (-0.9, -0.8, 0.8),
        (1.5, -0.2, 0.9),
        (-1.4, 0.3, 0.8),
        (0.2, 1.4, -0.9),
        (-0.3, -1.3, -0.8),
        (1.2, 1.1, -0.7),
        (-1.1, -1.0, -0.7),
        (0.0, 0.0, 1.6),
        (0.0, 0.0, -1.6),
    ]

    synapse_parent = bpy.data.objects.new("SynapseNetworkGroup", None)
    scene.collection.objects.link(synapse_parent)
    synapse_parent.location = (center_x, center_y, center_z)

    # ノード球の生成
    node_objs = []
    for idx, (nx, ny, nz) in enumerate(node_coords):
        is_central = (idx == 0)
        rad = 0.28 if is_central else 0.12
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=rad, location=(nx, ny, nz))
        node_obj = bpy.context.active_object
        node_obj.name = f"NeuralNode_{idx}"
        node_obj.parent = synapse_parent
        mat_use = mat_node_cyan if idx % 2 == 0 else mat_node_magenta
        node_obj.data.materials.append(mat_use)
        node_objs.append(node_obj)

    # 6.2 ノード間を結ぶシナプスライン（ベジェ曲線）
    connections = [
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 11), (0, 12),
        (1, 5), (1, 9), (2, 6), (2, 7), (3, 5), (3, 8),
        (4, 6), (4, 10), (5, 9), (6, 10), (7, 9), (8, 10),
        (11, 1), (11, 2), (12, 3), (12, 4)
    ]

    for c_idx, (start_idx, end_idx) in enumerate(connections):
        p_start = node_coords[start_idx]
        p_end = node_coords[end_idx]

        curve_data = bpy.data.curves.new(name=f"SynapseWire_{c_idx}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.016
        curve_data.bevel_resolution = 3

        spline = curve_data.splines.new(type='POLY')
        spline.points.add(1)
        spline.points[0].co = (p_start[0], p_start[1], p_start[2], 1.0)
        spline.points[1].co = (p_end[0], p_end[1], p_end[2], 1.0)

        curve_obj = bpy.data.objects.new(f"SynapseWireObj_{c_idx}", curve_data)
        scene.collection.objects.link(curve_obj)
        curve_obj.parent = synapse_parent
        curve_obj.data.materials.append(mat_synapse_wire)

        # 6.3 ワイヤー上を走るパルス光 (Synapse Pulse)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.040, location=(0, 0, 0))
        pulse_dot = bpy.context.active_object
        pulse_dot.name = f"PulseDot_{c_idx}"
        pulse_dot.data.materials.append(mat_pulse)
        pulse_dot.parent = synapse_parent

        pulse_offset = (c_idx / len(connections))

        for f in frames:
            t = (f - 1) / total_frames
            # シームレスにノード間を行き来または一方向に流れる
            u = (t * 2.0 + pulse_offset) % 1.0
            px = p_start[0] + (p_end[0] - p_start[0]) * u
            py = p_start[1] + (p_end[1] - p_start[1]) * u
            pz = p_start[2] + (p_end[2] - p_start[2]) * u

            pulse_dot.location = (px, py, pz)
            pulse_dot.keyframe_insert(data_path="location", frame=f)

    # グループ全体の滑らかな360度シームレス自転
    for f in frames:
        t = (f - 1) / total_frames
        rot_z = t * 2.0 * math.pi
        synapse_parent.rotation_euler = (math.radians(20) * math.sin(rot_z), math.radians(15) * math.cos(rot_z), rot_z)
        synapse_parent.keyframe_insert(data_path="rotation_euler", frame=f)

    # 7. カメラ設計（三脚完全固定・シネマティック中望遠）
    bpy.ops.object.camera_add(location=(-3.2, -10.0, 4.2))
    cam = bpy.context.active_object
    cam.name = "Stationary_Neural_Camera"
    cam.rotation_euler = (math.radians(68), 0, math.radians(-18))
    cam.data.lens = 42.0

    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 11.0
    cam.data.dof.aperture_fstop = 2.4

    scene.camera = cam

    # Blend保存
    blend_file = BLENDER_PROJECTS_DIR / "neon_neural_synapse.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend File Saved: {blend_file}")

    # レンダリング実行
    print("🎬 Rendering 1080p High-End Animation Frames...")
    bpy.ops.render.render(animation=True)
    print("✅ 1080p Frames Render Complete!")

    # プレビューPNGの抽出 (frame_0045)
    frame_45 = FRAMES_DIR / "frame_0045.jpg"
    if frame_45.exists():
        shutil.copy(frame_45, PREVIEW_PNG)
        print(f"📸 Preview Image Created: {PREVIEW_PNG}")

    # 4Kアップスケール動画生成
    print("🚀 Encoding to 4K UHD via Lanczos Fast Upscale...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(FRAMES_DIR / "frame_%04d.jpg"),
        "-vf", "scale=3840:2160:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(FINAL_4K_VIDEO)
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"🎉 4K Loop Video Exported: {FINAL_4K_VIDEO}")

    # CSVメタデータ生成
    print("📄 Generating Adobe Stock Submission CSV...")
    headers = ["Filename", "Title", "Keywords", "Category"]
    row = [
        FINAL_4K_VIDEO.name,
        "Abstract Neon Neural Synapse Network Loop Animation with Copy Space 4K",
        "neural network, artificial intelligence, deep learning, synapse, data connection, ai brain, glowing node, digital network, cyber technology, future computing, copy space, negative space, motion background, 4k seamless loop",
        3
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ Metadata CSV Created: {CSV_FILE}")

if __name__ == "__main__":
    build_and_render(total_frames=90, fps=30)
