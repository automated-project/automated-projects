#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock ハイエンド商用3D素材 (v2 商業最高品質)
テーマ：Quantum AI Data Core & Flowing Aurora Ribbons (シームレスループ 4K)
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
FRAMES_DIR = OUTPUT_DIR / "quantum_core_frames"
FINAL_4K_VIDEO = OUTPUT_DIR / "quantum_ai_data_core_4k_loop.mp4"
PREVIEW_PNG = OUTPUT_DIR / "preview_quantum_ai_core.png"
CSV_FILE = OUTPUT_DIR / "adobe_stock_quantum_core_submission.csv"

def build_scene(total_frames=90, fps=30):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "QuantumCoreScene"

    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps

    # 2. EEVEE 5.2 ハイエンド設定
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

    # 3. 背景グラデーション（ディープサファイア〜ミッドナイトスレート）
    world = bpy.data.worlds.new("QuantumWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.008, 0.012, 0.024, 1.0)
    bg.inputs['Strength'].default_value = 0.8

    # 背景用大型グラデーションバックドロップ
    mat_backdrop = bpy.data.materials.new(name="MatBackdrop")
    mat_backdrop.use_nodes = True
    bsdf_bd = mat_backdrop.node_tree.nodes.get("Principled BSDF")
    bsdf_bd.inputs['Base Color'].default_value = (0.012, 0.018, 0.035, 1.0)
    bsdf_bd.inputs['Roughness'].default_value = 0.85

    bpy.ops.mesh.primitive_plane_add(size=80.0, location=(0, 15.0, 0))
    backdrop = bpy.context.active_object
    backdrop.rotation_euler = (math.radians(90), 0, 0)
    backdrop.data.materials.append(mat_backdrop)

    # 4. スタジオシネマティック照明
    # ソフトアンビエント（右奥を照らし、空間に奥行きを出す）
    bpy.ops.object.light_add(type='AREA', location=(6.0, 8.0, 4.0))
    bg_light = bpy.context.active_object
    bg_light.data.energy = 800.0
    bg_light.data.size = 14.0
    bg_light.data.color = (0.05, 0.35, 0.9)
    bg_light.rotation_euler = (math.radians(-40), math.radians(20), 0)

    # メインキーライト（シアンソフトボックス）
    bpy.ops.object.light_add(type='AREA', location=(-6.0, -10.0, 8.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 1200.0
    key_light.data.size = 10.0
    key_light.data.color = (0.15, 0.85, 1.0)
    key_light.rotation_euler = (math.radians(52), math.radians(-15), math.radians(-25))

    # バックリムライト（クリスプバイオレット）
    bpy.ops.object.light_add(type='AREA', location=(0.0, 10.0, 6.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1500.0
    rim_light.data.size = 12.0
    rim_light.data.color = (0.4, 0.15, 1.0)
    rim_light.rotation_euler = (math.radians(-55), 0, 0)

    # 5. マテリアル設計
    # A. クリスタルフロストガラス（コア）
    mat_outer_glass = bpy.data.materials.new(name="MatOuterGlass")
    mat_outer_glass.use_nodes = True
    bsdf_og = mat_outer_glass.node_tree.nodes.get("Principled BSDF")
    bsdf_og.inputs['Base Color'].default_value = (0.92, 0.96, 1.0, 1.0)
    bsdf_og.inputs['Roughness'].default_value = 0.06
    bsdf_og.inputs['IOR'].default_value = 1.45
    if 'Transmission Weight' in bsdf_og.inputs:
        bsdf_og.inputs['Transmission Weight'].default_value = 0.95
    elif 'Transmission' in bsdf_og.inputs:
        bsdf_og.inputs['Transmission'].default_value = 0.95

    # B. 発光量子パルス核
    mat_quantum_core = bpy.data.materials.new(name="MatQuantumCore")
    mat_quantum_core.use_nodes = True
    bsdf_qc = mat_quantum_core.node_tree.nodes.get("Principled BSDF")
    bsdf_qc.inputs['Base Color'].default_value = (0.1, 0.95, 1.0, 1.0)
    if 'Emission Color' in bsdf_qc.inputs:
        bsdf_qc.inputs['Emission Color'].default_value = (0.2, 0.95, 1.0, 1.0)
        bsdf_qc.inputs['Emission Strength'].default_value = 4.5

    # C. エレガントなオーロラ光リボン（シアン・エレクトリック）
    mat_ribbon_cyan = bpy.data.materials.new(name="MatRibbonCyan")
    mat_ribbon_cyan.use_nodes = True
    bsdf_rc = mat_ribbon_cyan.node_tree.nodes.get("Principled BSDF")
    bsdf_rc.inputs['Base Color'].default_value = (0.05, 0.85, 1.0, 1.0)
    bsdf_rc.inputs['Roughness'].default_value = 0.15
    bsdf_rc.inputs['Metallic'].default_value = 0.85
    if 'Emission Color' in bsdf_rc.inputs:
        bsdf_rc.inputs['Emission Color'].default_value = (0.0, 0.85, 1.0, 1.0)
        bsdf_rc.inputs['Emission Strength'].default_value = 2.5

    # D. オーロラ光リボン（バイオレット・マゼンタ）
    mat_ribbon_violet = bpy.data.materials.new(name="MatRibbonViolet")
    mat_ribbon_violet.use_nodes = True
    bsdf_rv = mat_ribbon_violet.node_tree.nodes.get("Principled BSDF")
    bsdf_rv.inputs['Base Color'].default_value = (0.6, 0.2, 1.0, 1.0)
    bsdf_rv.inputs['Roughness'].default_value = 0.15
    bsdf_rv.inputs['Metallic'].default_value = 0.85
    if 'Emission Color' in bsdf_rv.inputs:
        bsdf_rv.inputs['Emission Color'].default_value = (0.65, 0.25, 1.0, 1.0)
        bsdf_rv.inputs['Emission Strength'].default_value = 2.2

    # E. ダークチタンリング
    mat_titanium = bpy.data.materials.new(name="MatTitanium")
    mat_titanium.use_nodes = True
    bsdf_ti = mat_titanium.node_tree.nodes.get("Principled BSDF")
    bsdf_ti.inputs['Base Color'].default_value = (0.15, 0.18, 0.22, 1.0)
    bsdf_ti.inputs['Metallic'].default_value = 0.98
    bsdf_ti.inputs['Roughness'].default_value = 0.12

    # 6. 配置座標（右寄りに配置し、左側7割に大空間コピースペース）
    center_x = 2.5
    center_y = 0.0
    center_z = 0.1

    frames = range(1, total_frames + 1, 2)

    # 7. オブジェクト構築
    # 7.1 中央の量子AIコア
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=1.05, location=(center_x, center_y, center_z))
    outer_core = bpy.context.active_object
    outer_core.name = "Quantum_OuterSphere"
    outer_core.data.materials.append(mat_outer_glass)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.68, location=(center_x, center_y, center_z))
    inner_core = bpy.context.active_object
    inner_core.name = "Quantum_InnerPulse"
    inner_core.data.materials.append(mat_quantum_core)

    for f in frames:
        t = (f - 1) / total_frames
        rot_angle = t * 2.0 * math.pi
        inner_core.rotation_euler = (rot_angle * 1.0, rot_angle * 1.5, rot_angle * 0.5)
        inner_core.keyframe_insert(data_path="rotation_euler", frame=f)

    # 7.2 精密チタン軌道フレーム
    for r_idx, r_rad in enumerate([1.4, 2.0]):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=r_rad,
            minor_radius=0.015,
            major_segments=64,
            minor_segments=16,
            location=(center_x, center_y, center_z)
        )
        t_ring = bpy.context.active_object
        t_ring.name = f"TitaniumRing_{r_idx}"
        t_ring.data.materials.append(mat_titanium)

        rx = math.radians(35 if r_idx == 0 else -50)
        ry = math.radians(25 if r_idx == 0 else 40)
        speed = 1.0 if r_idx == 0 else -1.2

        for f in frames:
            t = (f - 1) / total_frames
            spin = t * 2.0 * math.pi * speed
            t_ring.rotation_euler = (rx, ry, spin)
            t_ring.keyframe_insert(data_path="rotation_euler", frame=f)

    # 7.3 洗練されたオーロラリボン（スリム＆エレガント）
    num_ribbons = 4
    for rib_idx in range(num_ribbons):
        curve_data = bpy.data.curves.new(name=f"RibbonCurve_{rib_idx}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = 0.020 # より細く繊細に
        curve_data.bevel_resolution = 4
        curve_data.extrude = 0.045

        spline = curve_data.splines.new(type='NURBS')
        spline.use_cyclic_u = True

        pts_count = 16
        spline.points.add(pts_count - 1)

        curve_obj = bpy.data.objects.new(f"RibbonObj_{rib_idx}", curve_data)
        scene.collection.objects.link(curve_obj)
        curve_obj.location = (center_x, center_y, center_z)

        mat_use = mat_ribbon_cyan if rib_idx % 2 == 0 else mat_ribbon_violet
        curve_obj.data.materials.append(mat_use)

        base_radius = 1.7 + rib_idx * 0.45
        rib_tilt = math.radians(25 + rib_idx * 40)
        rib_phase_offset = (rib_idx / num_ribbons) * 2.0 * math.pi

        for f in frames:
            t = (f - 1) / total_frames
            phase_t = t * 2.0 * math.pi + rib_phase_offset

            for p_idx in range(pts_count):
                u = (p_idx / pts_count) * 2.0 * math.pi
                r = base_radius + math.sin(u * 3.0 + phase_t) * 0.28
                px = math.cos(u) * r
                py = math.sin(u) * r * 0.8
                pz = math.sin(u * 2.0 - phase_t) * 0.6 + math.cos(u * 3.0) * 0.2

                pt = spline.points[p_idx]
                pt.co = (px, py, pz, 1.0)

            curve_obj.rotation_euler = (rib_tilt, 0, t * 2.0 * math.pi * (1.0 if rib_idx % 2 == 0 else -1.0))
            curve_obj.keyframe_insert(data_path="rotation_euler", frame=f)

    # 7.4 空間を漂う微細な光のダスト粒子（Neural Dust）
    mat_dust_cyan = bpy.data.materials.new(name="MatDustCyan")
    mat_dust_cyan.use_nodes = True
    nodes_dc = mat_dust_cyan.node_tree.nodes
    nodes_dc.clear()
    node_emit_dc = nodes_dc.new(type='ShaderNodeEmission')
    node_emit_dc.inputs['Color'].default_value = (0.4, 0.95, 1.0, 1.0)
    node_emit_dc.inputs['Strength'].default_value = 10.0
    node_out_dc = nodes_dc.new(type='ShaderNodeOutputMaterial')
    mat_dust_cyan.node_tree.links.new(node_emit_dc.outputs['Emission'], node_out_dc.inputs['Surface'])

    num_dust = 42
    for i in range(num_dust):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.030, location=(0, 0, 0))
        dust = bpy.context.active_object
        dust.name = f"QuantumDust_{i}"
        dust.data.materials.append(mat_dust_cyan)

        orbit_r = 1.3 + (i % 8) * 0.45
        inclination = (i / num_dust) * math.pi
        speed = 1.0 if (i % 2 == 0) else -1.0
        phase = (i / num_dust) * 2.0 * math.pi

        for f in frames:
            t = (f - 1) / total_frames
            angle = phase + t * 2.0 * math.pi * speed
            dx = center_x + math.cos(angle) * orbit_r * math.sin(inclination)
            dy = center_y + math.sin(angle) * orbit_r
            dz = center_z + math.cos(inclination) * orbit_r * 0.7 + math.sin(t * 4.0 * math.pi + i) * 0.2

            dust.location = (dx, dy, dz)
            dust.keyframe_insert(data_path="location", frame=f)

    # 8. カメラ設計（完全三脚固定 ＆ シネマティック被写界深度）
    bpy.ops.object.camera_add(location=(-3.2, -9.8, 3.8))
    cam = bpy.context.active_object
    cam.name = "Stationary_Quantum_Camera"
    cam.rotation_euler = (math.radians(70), 0, math.radians(-18))
    cam.data.lens = 42.0

    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 10.8
    cam.data.dof.aperture_fstop = 2.4

    scene.camera = cam

    # 保存
    blend_file = OUTPUT_DIR.parent / "blender_projects" / "quantum_ai_data_core.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Quantum Core Scene Saved: {blend_file}")

    # レンダリング実行
    print("🎬 Rendering 1080p High-End Animation Frames...")
    bpy.ops.render.render(animation=True)
    print("✅ 1080p Frames Render Complete!")

    # CSVメタデータ生成
    print("📄 Generating Adobe Stock Submission CSV...")
    headers = ["Filename", "Title", "Keywords", "Category"]
    row = [
        FINAL_4K_VIDEO.name,
        "3D Quantum AI Data Core with Flowing Neon Ribbons Seamless Loop",
        "quantum computing, ai data core, artificial intelligence, glowing ribbons, future technology, abstract 3d background, machine learning, digital transformation, modern corporate b-roll, copy space, negative space, 4k commercial, seamless loop",
        3
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ Metadata CSV Created: {CSV_FILE}")

if __name__ == "__main__":
    build_scene(total_frames=90, fps=30)
