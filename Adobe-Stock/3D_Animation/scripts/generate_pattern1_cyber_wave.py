#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock ハイエンド商用3D素材 (Pattern 1)
テーマ：Cyber Data Wave & Flow (有機的にうねる光のグリッド波とデータフロー)
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
FRAMES_DIR = OUTPUT_DIR / "pattern1_cyber_wave_frames"
FINAL_4K_VIDEO = OUTPUT_DIR / "cyber_data_wave_flow_4k_loop.mp4"
PREVIEW_PNG = OUTPUT_DIR / "preview_cyber_data_wave.png"
CSV_FILE = OUTPUT_DIR / "adobe_stock_cyber_data_wave_submission.csv"
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
    scene.name = "CyberWaveScene"

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
    world = bpy.data.worlds.new("CyberWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.005, 0.008, 0.016, 1.0) # 深いサイバーネイビー
    bg.inputs['Strength'].default_value = 0.5

    # 4. スタジオ照明
    # トップキーライト（シアンブルー）
    bpy.ops.object.light_add(type='AREA', location=(0.0, -2.0, 10.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 1500.0
    key_light.data.size = 14.0
    key_light.data.color = (0.1, 0.8, 1.0)
    key_light.rotation_euler = (math.radians(15), 0, 0)

    # バックリムライト（バイオレット）
    bpy.ops.object.light_add(type='AREA', location=(0.0, 12.0, 4.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1200.0
    rim_light.data.size = 16.0
    rim_light.data.color = (0.5, 0.1, 1.0)
    rim_light.rotation_euler = (math.radians(-45), 0, 0)

    # 5. マテリアル
    # A. 波動グリッド用ネオンマテリアル（シアン〜ディープブルー）
    mat_wave_grid = bpy.data.materials.new(name="MatWaveGrid")
    mat_wave_grid.use_nodes = True
    bsdf_wg = mat_wave_grid.node_tree.nodes.get("Principled BSDF")
    bsdf_wg.inputs['Base Color'].default_value = (0.05, 0.6, 0.95, 1.0)
    bsdf_wg.inputs['Metallic'].default_value = 0.9
    bsdf_wg.inputs['Roughness'].default_value = 0.15
    if 'Emission Color' in bsdf_wg.inputs:
        bsdf_wg.inputs['Emission Color'].default_value = (0.0, 0.8, 1.0, 1.0)
        bsdf_wg.inputs['Emission Strength'].default_value = 3.2

    # B. データパルス球マテリアル（高輝度エレクトリックホワイト・ブルー）
    mat_pulse_dot = bpy.data.materials.new(name="MatPulseDot")
    mat_pulse_dot.use_nodes = True
    bsdf_pd = mat_pulse_dot.node_tree.nodes.get("Principled BSDF")
    bsdf_pd.inputs['Base Color'].default_value = (0.8, 0.95, 1.0, 1.0)
    if 'Emission Color' in bsdf_pd.inputs:
        bsdf_pd.inputs['Emission Color'].default_value = (0.4, 0.9, 1.0, 1.0)
        bsdf_pd.inputs['Emission Strength'].default_value = 8.0

    # C. 背景コピースペース用のディープグラデーションリボン
    mat_sub_stream = bpy.data.materials.new(name="MatSubStream")
    mat_sub_stream.use_nodes = True
    bsdf_ss = mat_sub_stream.node_tree.nodes.get("Principled BSDF")
    bsdf_ss.inputs['Base Color'].default_value = (0.3, 0.05, 0.8, 1.0)
    bsdf_ss.inputs['Metallic'].default_value = 0.8
    bsdf_ss.inputs['Roughness'].default_value = 0.2
    if 'Emission Color' in bsdf_ss.inputs:
        bsdf_ss.inputs['Emission Color'].default_value = (0.4, 0.1, 0.9, 1.0)
        bsdf_ss.inputs['Emission Strength'].default_value = 1.8

    # 6. サイバー波形グリッド（画面下部〜右側へダイナミックに広がるウェーブストリーム）
    # 複数の平行な波形リボン（スプライン）を生成
    frames = range(1, total_frames + 1, 2)
    num_lines = 16
    pts_per_line = 32
    length = 24.0

    wave_parent = bpy.data.objects.new("WaveGridGroup", None)
    scene.collection.objects.link(wave_parent)
    wave_parent.location = (2.0, 0.0, -1.2) # 右寄りに配置して左上〜中央に余白
    wave_parent.rotation_euler = (math.radians(-25), math.radians(15), math.radians(-30))

    for line_idx in range(num_lines):
        curve_data = bpy.data.curves.new(name=f"WaveLine_{line_idx}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.022
        curve_data.bevel_resolution = 3

        spline = curve_data.splines.new(type='NURBS')
        spline.points.add(pts_per_line - 1)

        curve_obj = bpy.data.objects.new(f"WaveLineObj_{line_idx}", curve_data)
        scene.collection.objects.link(curve_obj)
        curve_obj.parent = wave_parent

        mat_choice = mat_wave_grid if line_idx % 3 != 0 else mat_sub_stream
        curve_obj.data.materials.append(mat_choice)

        y_offset = (line_idx - num_lines / 2) * 0.7

        for f in frames:
            t = (f - 1) / total_frames
            phase = t * 2.0 * math.pi

            for p_idx in range(pts_per_line):
                x = (p_idx / (pts_per_line - 1) - 0.5) * length
                # 複合サイン波でシームレスなループ波形を作成
                # k * phase (kは整数) で完全ループ
                freq1 = 2.0 * math.pi / length * 2.0
                freq2 = 2.0 * math.pi / length * 3.0
                
                z = (
                    math.sin(x * freq1 - phase) * 0.8 * math.cos(y_offset * 0.3) +
                    math.sin(x * freq2 + phase * 2.0 + line_idx * 0.4) * 0.4 +
                    math.cos(y_offset * 0.5 - phase) * 0.3
                )
                
                # 端に向かってフェードアウト
                envelope = math.sin((p_idx / (pts_per_line - 1)) * math.pi)
                z = z * envelope

                pt = spline.points[p_idx]
                pt.co = (x, y_offset, z, 1.0)
                pt.keyframe_insert(data_path="co", frame=f)

    # 7. 流れる光のデータパルス粒子 (Data Packets)
    num_particles = 36
    for p in range(num_particles):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.045, location=(0, 0, 0))
        dot = bpy.context.active_object
        dot.name = f"DataPacket_{p}"
        dot.data.materials.append(mat_pulse_dot)
        dot.parent = wave_parent

        line_target = p % num_lines
        y_pos = (line_target - num_lines / 2) * 0.7
        speed_mult = 1.0 if (p % 2 == 0) else 2.0
        start_u = (p / num_particles)

        for f in frames:
            t = (f - 1) / total_frames
            u = (start_u + t * speed_mult) % 1.0
            x = (u - 0.5) * length
            phase = t * 2.0 * math.pi
            
            freq1 = 2.0 * math.pi / length * 2.0
            freq2 = 2.0 * math.pi / length * 3.0
            z = (
                math.sin(x * freq1 - phase) * 0.8 * math.cos(y_pos * 0.3) +
                math.sin(x * freq2 + phase * 2.0 + line_target * 0.4) * 0.4 +
                math.cos(y_pos * 0.5 - phase) * 0.3
            )
            envelope = math.sin(u * math.pi)
            z = (z * envelope) + 0.08 # 波の表面少し上に配置

            dot.location = (x, y_pos, z)
            dot.keyframe_insert(data_path="location", frame=f)

    # 8. カメラ設計（三脚完全固定・広角シネマティック）
    bpy.ops.object.camera_add(location=(-4.5, -12.0, 5.5))
    cam = bpy.context.active_object
    cam.name = "Stationary_CyberWave_Camera"
    cam.rotation_euler = (math.radians(68), 0, math.radians(-22))
    cam.data.lens = 35.0

    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 13.0
    cam.data.dof.aperture_fstop = 2.8

    scene.camera = cam

    # Blend保存
    blend_file = BLENDER_PROJECTS_DIR / "cyber_data_wave_flow.blend"
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
        "Abstract Cyber Data Wave and Digital Grid Flow Loop Background with Copy Space 4K",
        "cyber wave, big data stream, digital flow, network grid, futuristic technology, abstract 3d background, cloud computing, glowing particles, telecommunication, high tech motion graphics, corporate presentation b-roll, copy space, negative space, 4k seamless loop",
        3
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ Metadata CSV Created: {CSV_FILE}")

if __name__ == "__main__":
    build_and_render(total_frames=90, fps=30)
