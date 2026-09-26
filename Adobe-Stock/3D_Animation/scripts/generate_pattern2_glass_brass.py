#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock ハイエンド商用3D素材 (Pattern 2)
テーマ：Minimalist Frosted Glass & Polished Brass Mechanism (幾何学パーツの精密連動からくり)
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
FRAMES_DIR = OUTPUT_DIR / "pattern2_glass_brass_frames"
FINAL_4K_VIDEO = OUTPUT_DIR / "glass_brass_mechanism_4k_loop.mp4"
PREVIEW_PNG = OUTPUT_DIR / "preview_glass_brass_mechanism.png"
CSV_FILE = OUTPUT_DIR / "adobe_stock_glass_brass_submission.csv"
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
    scene.name = "GlassBrassScene"

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

    # 3. 背景・ワールド環境（ミニマルなスタジオスレートグレー）
    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.015, 0.018, 0.022, 1.0)
    bg.inputs['Strength'].default_value = 0.6

    # バックドロップ
    mat_backdrop = bpy.data.materials.new(name="MatBackdrop")
    mat_backdrop.use_nodes = True
    bsdf_bd = mat_backdrop.node_tree.nodes.get("Principled BSDF")
    bsdf_bd.inputs['Base Color'].default_value = (0.02, 0.025, 0.03, 1.0)
    bsdf_bd.inputs['Roughness'].default_value = 0.8

    bpy.ops.mesh.primitive_plane_add(size=80.0, location=(0, 15.0, 0))
    backdrop = bpy.context.active_object
    backdrop.rotation_euler = (math.radians(90), 0, 0)
    backdrop.data.materials.append(mat_backdrop)

    # 4. スタジオ照明（高級プロダクト撮影ライティング）
    # ウォームキーライト（真鍮の輝きを引き立てる）
    bpy.ops.object.light_add(type='AREA', location=(-5.0, -8.0, 7.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 1600.0
    key_light.data.size = 8.0
    key_light.data.color = (1.0, 0.92, 0.82)
    key_light.rotation_euler = (math.radians(50), math.radians(-15), math.radians(-25))

    # クールフィルライト（ガラスのエッジを際立たせる）
    bpy.ops.object.light_add(type='AREA', location=(6.0, -6.0, 4.0))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 900.0
    fill_light.data.size = 10.0
    fill_light.data.color = (0.75, 0.85, 1.0)
    fill_light.rotation_euler = (math.radians(40), math.radians(20), math.radians(15))

    # リムバックライト
    bpy.ops.object.light_add(type='AREA', location=(0.0, 10.0, 5.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1400.0
    rim_light.data.size = 12.0
    rim_light.data.color = (1.0, 0.95, 0.9)
    rim_light.rotation_euler = (math.radians(-50), 0, 0)

    # 5. マテリアル
    # A. 磨き出し真鍮（Polished Brass / Gold）
    mat_brass = bpy.data.materials.new(name="MatBrass")
    mat_brass.use_nodes = True
    bsdf_br = mat_brass.node_tree.nodes.get("Principled BSDF")
    bsdf_br.inputs['Base Color'].default_value = (0.92, 0.72, 0.28, 1.0)
    bsdf_br.inputs['Metallic'].default_value = 0.95
    bsdf_br.inputs['Roughness'].default_value = 0.12

    # B. 高級フロストガラス（Frosted Glass）
    mat_glass = bpy.data.materials.new(name="MatFrostedGlass")
    mat_glass.use_nodes = True
    bsdf_gl = mat_glass.node_tree.nodes.get("Principled BSDF")
    bsdf_gl.inputs['Base Color'].default_value = (0.95, 0.98, 1.0, 1.0)
    bsdf_gl.inputs['Roughness'].default_value = 0.08
    bsdf_gl.inputs['IOR'].default_value = 1.48
    if 'Transmission Weight' in bsdf_gl.inputs:
        bsdf_gl.inputs['Transmission Weight'].default_value = 0.92
    elif 'Transmission' in bsdf_gl.inputs:
        bsdf_gl.inputs['Transmission'].default_value = 0.92

    # C. マットダークスレート（台座・コントラスト用）
    mat_slate = bpy.data.materials.new(name="MatSlate")
    mat_slate.use_nodes = True
    bsdf_sl = mat_slate.node_tree.nodes.get("Principled BSDF")
    bsdf_sl.inputs['Base Color'].default_value = (0.08, 0.10, 0.13, 1.0)
    bsdf_sl.inputs['Metallic'].default_value = 0.4
    bsdf_sl.inputs['Roughness'].default_value = 0.35

    # 6. オブジェクト配置（画面右側に配置、左側7割コピースペース）
    center_x = 2.4
    center_y = 0.0
    center_z = 0.0
    frames = range(1, total_frames + 1, 2)

    # 6.1 中央の多面体ガラスコア（角丸キューブ / ダイアモンド様構造）
    bpy.ops.mesh.primitive_cube_add(size=1.4, location=(center_x, center_y, center_z))
    glass_cube = bpy.context.active_object
    glass_cube.name = "Mechanism_GlassCube"
    glass_cube.data.materials.append(mat_glass)

    # ベベルモディファイアで高級感のあるエッジハイライト
    sub_mod = glass_cube.modifiers.new(name="Bevel", type='BEVEL')
    sub_mod.width = 0.06
    sub_mod.segments = 4

    for f in frames:
        t = (f - 1) / total_frames
        rot = t * 2.0 * math.pi
        glass_cube.rotation_euler = (rot * 1.0, rot * 1.0, rot * 0.5)
        glass_cube.keyframe_insert(data_path="rotation_euler", frame=f)

    # 6.2 3軸の真鍮インターロッキングジンバルリング
    radii = [1.8, 2.3, 2.8]
    speeds = [1.0, -1.0, 1.0]
    axes = [
        (math.radians(30), 0, 0),
        (0, math.radians(45), 0),
        (math.radians(-30), math.radians(30), 0)
    ]

    for idx, (r, spd, axis) in enumerate(zip(radii, speeds, axes)):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=r,
            minor_radius=0.032,
            major_segments=64,
            minor_segments=16,
            location=(center_x, center_y, center_z)
        )
        ring = bpy.context.active_object
        ring.name = f"BrassRing_{idx}"
        ring.data.materials.append(mat_brass)

        for f in frames:
            t = (f - 1) / total_frames
            spin = t * 2.0 * math.pi * spd
            if idx == 0:
                ring.rotation_euler = (axis[0] + spin, axis[1], axis[2])
            elif idx == 1:
                ring.rotation_euler = (axis[0], axis[1] + spin, axis[2])
            else:
                ring.rotation_euler = (axis[0], axis[1], axis[2] + spin)
            ring.keyframe_insert(data_path="rotation_euler", frame=f)

    # 6.3 周囲を浮遊・連動する幾何学真鍮カプセル
    num_satellites = 6
    for s_idx in range(num_satellites):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.08,
            depth=0.35,
            location=(0, 0, 0)
        )
        sat = bpy.context.active_object
        sat.name = f"BrassSatellite_{s_idx}"
        sat.data.materials.append(mat_brass)

        phase = (s_idx / num_satellites) * 2.0 * math.pi
        sat_r = 2.1

        for f in frames:
            t = (f - 1) / total_frames
            angle = phase + t * 2.0 * math.pi
            sx = center_x + math.cos(angle) * sat_r
            sy = center_y + math.sin(angle) * sat_r
            sz = center_z + math.sin(angle * 2.0) * 0.4

            sat.location = (sx, sy, sz)
            sat.rotation_euler = (t * 4.0 * math.pi, angle, math.radians(45))
            sat.keyframe_insert(data_path="location", frame=f)
            sat.keyframe_insert(data_path="rotation_euler", frame=f)

    # 7. カメラ設計（三脚完全固定・シネマティック中望遠）
    bpy.ops.object.camera_add(location=(-3.0, -10.5, 4.0))
    cam = bpy.context.active_object
    cam.name = "Stationary_GlassBrass_Camera"
    cam.rotation_euler = (math.radians(69), 0, math.radians(-16))
    cam.data.lens = 45.0

    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 11.2
    cam.data.dof.aperture_fstop = 2.4

    scene.camera = cam

    # Blend保存
    blend_file = BLENDER_PROJECTS_DIR / "glass_brass_mechanism.blend"
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
        "Minimalist Frosted Glass and Polished Brass Mechanism Loop Animation with Copy Space 4K",
        "frosted glass, polished brass, luxury mechanical, kinetic sculpture, geometric animation, modern abstract 3d, luxury corporate background, innovation concept, copy space, negative space, premium motion design, 4k seamless loop",
        3
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ Metadata CSV Created: {CSV_FILE}")

if __name__ == "__main__":
    build_and_render(total_frames=90, fps=30)
