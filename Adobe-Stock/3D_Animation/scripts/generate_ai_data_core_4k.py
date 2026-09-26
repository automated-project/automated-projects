#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock 特化型 3Dモーショングラフィックス 完全自動化マスター (一気通貫実行)
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
FRAMES_DIR = OUTPUT_DIR / "tech_core_frames"
FINAL_4K_VIDEO = OUTPUT_DIR / "tech_ai_data_core_orbit_4k_loop.mp4"
CSV_FILE = OUTPUT_DIR / "adobe_stock_3d_tech_submission.csv"

def build_scene(total_frames=90, fps=30):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "TechDataCoreScene"

    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps

    # 2. 超低負荷 EEVEE 5.2 設定 (1080p / サンプル数8)
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene, 'eevee'):
        scene.eevee.taa_render_samples = 8
        if hasattr(scene.eevee, 'use_raytracing'):
            scene.eevee.use_raytracing = True

    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Punchy'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.quality = 95
    scene.render.filepath = str(FRAMES_DIR / "frame_")

    # 3. ワールド環境（深いプレミアム・サイバーダーク）
    world = bpy.data.worlds.new("TechWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.005, 0.008, 0.018, 1.0)
    bg.inputs['Strength'].default_value = 0.5

    # 4. ライティング
    bpy.ops.object.light_add(type='AREA', location=(-6.0, -8.0, 8.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 800.0
    key_light.data.size = 8.0
    key_light.data.color = (0.3, 0.8, 1.0)
    key_light.rotation_euler = (math.radians(50), math.radians(-15), math.radians(-25))

    bpy.ops.object.light_add(type='AREA', location=(8.0, -4.0, 6.0))
    side_light = bpy.context.active_object
    side_light.data.energy = 600.0
    side_light.data.size = 10.0
    side_light.data.color = (0.4, 0.15, 1.0)
    side_light.rotation_euler = (math.radians(45), math.radians(20), math.radians(10))

    bpy.ops.object.light_add(type='AREA', location=(2.0, 10.0, 6.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1000.0
    rim_light.data.size = 10.0
    rim_light.data.color = (0.1, 0.95, 1.0)
    rim_light.rotation_euler = (math.radians(-55), 0, 0)

    # 5. マテリアルパレット
    mat_chrome = bpy.data.materials.new(name="MatChrome")
    mat_chrome.use_nodes = True
    bsdf_ch = mat_chrome.node_tree.nodes.get("Principled BSDF")
    bsdf_ch.inputs['Base Color'].default_value = (0.85, 0.88, 0.95, 1.0)
    bsdf_ch.inputs['Metallic'].default_value = 0.98
    bsdf_ch.inputs['Roughness'].default_value = 0.12

    mat_glass = bpy.data.materials.new(name="MatFrostedGlass")
    mat_glass.use_nodes = True
    bsdf_gl = mat_glass.node_tree.nodes.get("Principled BSDF")
    bsdf_gl.inputs['Base Color'].default_value = (0.9, 0.95, 1.0, 1.0)
    bsdf_gl.inputs['Roughness'].default_value = 0.08
    bsdf_gl.inputs['IOR'].default_value = 1.45
    if 'Transmission Weight' in bsdf_gl.inputs:
        bsdf_gl.inputs['Transmission Weight'].default_value = 0.92
    elif 'Transmission' in bsdf_gl.inputs:
        bsdf_gl.inputs['Transmission'].default_value = 0.92

    mat_neon_cyan = bpy.data.materials.new(name="MatNeonCyan")
    mat_neon_cyan.use_nodes = True
    bsdf_nc = mat_neon_cyan.node_tree.nodes.get("Principled BSDF")
    bsdf_nc.inputs['Base Color'].default_value = (0.0, 0.8, 1.0, 1.0)
    if 'Emission Color' in bsdf_nc.inputs:
        bsdf_nc.inputs['Emission Color'].default_value = (0.0, 0.9, 1.0, 1.0)
        bsdf_nc.inputs['Emission Strength'].default_value = 4.0

    mat_neon_violet = bpy.data.materials.new(name="MatNeonViolet")
    mat_neon_violet.use_nodes = True
    bsdf_nv = mat_neon_violet.node_tree.nodes.get("Principled BSDF")
    bsdf_nv.inputs['Base Color'].default_value = (0.5, 0.2, 1.0, 1.0)
    if 'Emission Color' in bsdf_nv.inputs:
        bsdf_nv.inputs['Emission Color'].default_value = (0.6, 0.25, 1.0, 1.0)
        bsdf_nv.inputs['Emission Strength'].default_value = 3.0

    # 6. オブジェクト生成
    center_x = 2.4
    center_y = 0.0
    center_z = 0.0

    frames = range(1, total_frames + 1, 2)

    # 6.1 中央コア
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=1.0, location=(center_x, center_y, center_z))
    core_sphere = bpy.context.active_object
    core_sphere.name = "DataCore_Outer"
    core_sphere.data.materials.append(mat_glass)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.65, location=(center_x, center_y, center_z))
    core_inner = bpy.context.active_object
    core_inner.name = "DataCore_Inner"
    core_inner.data.materials.append(mat_neon_cyan)

    for f in frames:
        t = (f - 1) / total_frames
        angle = t * 2.0 * math.pi
        core_inner.rotation_euler = (angle, angle * 1.5, angle * 0.5)
        core_inner.keyframe_insert(data_path="rotation_euler", frame=f)

    # 6.2 軌道幾何学リング群
    ring_configs = [
        {"radius": 1.7, "tube": 0.025, "tilt_x": 30, "tilt_y": 20, "speed": 1.0, "mat": mat_chrome},
        {"radius": 2.2, "tube": 0.020, "tilt_x": -45, "tilt_y": 35, "speed": -1.0, "mat": mat_neon_cyan},
        {"radius": 2.8, "tube": 0.030, "tilt_x": 60, "tilt_y": -40, "speed": 1.5, "mat": mat_chrome},
        {"radius": 3.4, "tube": 0.018, "tilt_x": -20, "tilt_y": 70, "speed": -0.8, "mat": mat_neon_violet},
    ]

    for idx, cfg in enumerate(ring_configs):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=cfg["radius"],
            minor_radius=cfg["tube"],
            major_segments=48,
            minor_segments=16,
            location=(center_x, center_y, center_z)
        )
        ring = bpy.context.active_object
        ring.name = f"OrbitRing_{idx}"
        ring.data.materials.append(cfg["mat"])

        base_rx = math.radians(cfg["tilt_x"])
        base_ry = math.radians(cfg["tilt_y"])

        for f in frames:
            t = (f - 1) / total_frames
            spin = t * 2.0 * math.pi * cfg["speed"]
            ring.rotation_euler = (base_rx, base_ry, spin)
            ring.keyframe_insert(data_path="rotation_euler", frame=f)

    # 6.3 浮遊ノード
    num_particles = 24
    for i in range(num_particles):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.045, location=(0, 0, 0))
        node = bpy.context.active_object
        node.name = f"TechNode_{i}"
        node.data.materials.append(mat_neon_cyan if i % 2 == 0 else mat_chrome)

        orbit_r = 1.8 + (i % 5) * 0.4
        inclination = (i / num_particles) * math.pi
        speed = 1.0 if (i % 2 == 0) else -1.0
        phase = (i / num_particles) * 2.0 * math.pi

        for f in frames:
            t = (f - 1) / total_frames
            angle = phase + t * 2.0 * math.pi * speed
            nx = center_x + math.cos(angle) * orbit_r * math.sin(inclination)
            ny = center_y + math.sin(angle) * orbit_r
            nz = center_z + math.cos(inclination) * orbit_r * 0.6 + math.sin(t * 4.0 * math.pi + i) * 0.15

            node.location = (nx, ny, nz)
            node.keyframe_insert(data_path="location", frame=f)

    # 7. カメラ設定（完全三脚固定）
    bpy.ops.object.camera_add(location=(-3.0, -10.5, 4.2))
    cam = bpy.context.active_object
    cam.name = "Stationary_Tech_Camera"
    cam.rotation_euler = (math.radians(68), 0, math.radians(-16))
    cam.data.lens = 42.0

    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 11.5
    cam.data.dof.aperture_fstop = 2.4

    scene.camera = cam

    blend_file = OUTPUT_DIR.parent / "blender_projects" / "tech_ai_data_core_orbit.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print("🎬 Rendering 1080p Animation Frames...")
    bpy.ops.render.render(animation=True)
    print("✅ All Frames Rendered Successfully!")

if __name__ == "__main__":
    build_scene(total_frames=90, fps=30)
