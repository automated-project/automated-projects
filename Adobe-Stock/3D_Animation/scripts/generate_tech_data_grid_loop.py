#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adobe Stock 特化型 3D動画素材生成スクリプト (v3.0 商業ハイエンド)
ジャンル①：テクノロジー・DX・データ通信系（最大需要）
テーマ：Cyber Tech 3D Data Grid Wave & Glowing Neural Nodes
規格：4K UHD (3840x2160), 60fps, シームレスループ, 完全三脚固定, コピースペース確保
"""

import os
import sys
import math
import bpy

def setup_tech_data_grid_scene(output_blend_path, total_frames=240, fps=60):
    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "TechDataGridScene"

    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps

    # 2. レンダリング設定 (EEVEE 5.2 - 高速＆超高画質)
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene, 'eevee'):
        scene.eevee.taa_render_samples = 16
        if hasattr(scene.eevee, 'use_raytracing'):
            scene.eevee.use_raytracing = True

    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Punchy'
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100

    # 3. ワールド環境（深い宇宙・サイバーダーク）
    world = bpy.data.worlds.new("TechWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.008, 0.012, 0.025, 1.0)
    bg.inputs['Strength'].default_value = 0.6

    # 4. ライティング設計（ドラマチックな陰影とエッジ反射）
    # メインキーライト（クールシアン）
    bpy.ops.object.light_add(type='AREA', location=(-6.0, -12.0, 10.0))
    key_light = bpy.context.active_object
    key_light.data.energy = 1200.0
    key_light.data.size = 10.0
    key_light.data.color = (0.2, 0.8, 1.0)
    key_light.rotation_euler = (math.radians(55), math.radians(-15), math.radians(-25))

    # サイドフィルライト（エレクトリックバイオレット）
    bpy.ops.object.light_add(type='AREA', location=(12.0, -4.0, 8.0))
    side_light = bpy.context.active_object
    side_light.data.energy = 800.0
    side_light.data.size = 12.0
    side_light.data.color = (0.3, 0.1, 0.9)
    side_light.rotation_euler = (math.radians(45), math.radians(20), math.radians(10))

    # バックリムライト（クリスプスカイブルー）
    bpy.ops.object.light_add(type='AREA', location=(0.0, 14.0, 8.0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 1400.0
    rim_light.data.size = 14.0
    rim_light.data.color = (0.1, 0.9, 1.0)
    rim_light.rotation_euler = (math.radians(-60), 0, 0)

    # 5. マテリアル設計
    # A. 高級マットダークチタン（キューブの基本マテリアル）
    mat_dark_titanium = bpy.data.materials.new(name="MatDarkTitanium")
    mat_dark_titanium.use_nodes = True
    bsdf_dt = mat_dark_titanium.node_tree.nodes.get("Principled BSDF")
    bsdf_dt.inputs['Base Color'].default_value = (0.025, 0.035, 0.055, 1.0)
    bsdf_dt.inputs['Metallic'].default_value = 0.92
    bsdf_dt.inputs['Roughness'].default_value = 0.18

    # B. 発光シアンノード（キーキューブの天面・アクセント）
    mat_cyan_accent = bpy.data.materials.new(name="MatCyanAccent")
    mat_cyan_accent.use_nodes = True
    bsdf_ca = mat_cyan_accent.node_tree.nodes.get("Principled BSDF")
    bsdf_ca.inputs['Base Color'].default_value = (0.01, 0.03, 0.06, 1.0)
    bsdf_ca.inputs['Metallic'].default_value = 0.9
    bsdf_ca.inputs['Roughness'].default_value = 0.12
    if 'Emission Color' in bsdf_ca.inputs:
        bsdf_ca.inputs['Emission Color'].default_value = (0.0, 0.85, 1.0, 1.0)
        bsdf_ca.inputs['Emission Strength'].default_value = 1.6

    # C. 発光ブルーノード
    mat_blue_accent = bpy.data.materials.new(name="MatBlueAccent")
    mat_blue_accent.use_nodes = True
    bsdf_ba = mat_blue_accent.node_tree.nodes.get("Principled BSDF")
    bsdf_ba.inputs['Base Color'].default_value = (0.01, 0.02, 0.05, 1.0)
    bsdf_ba.inputs['Metallic'].default_value = 0.9
    bsdf_ba.inputs['Roughness'].default_value = 0.15
    if 'Emission Color' in bsdf_ba.inputs:
        bsdf_ba.inputs['Emission Color'].default_value = (0.1, 0.4, 1.0, 1.0)
        bsdf_ba.inputs['Emission Strength'].default_value = 1.2

    # D. グリッドフロア（反射ミラー床）
    mat_floor = bpy.data.materials.new(name="MatFloor")
    mat_floor.use_nodes = True
    bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
    bsdf_fl.inputs['Base Color'].default_value = (0.006, 0.009, 0.018, 1.0)
    bsdf_fl.inputs['Metallic'].default_value = 0.96
    bsdf_fl.inputs['Roughness'].default_value = 0.22

    # 6. 反射床
    bpy.ops.mesh.primitive_plane_add(size=120.0, location=(0, 0, -0.6))
    floor_obj = bpy.context.active_object
    floor_obj.data.materials.append(mat_floor)

    # 7. グリッドキューブ群の生成（右寄せ配置・左側に大空間コピースペース）
    cols = 22
    rows = 16
    spacing = 0.82
    cube_size = 0.74
    offset_x = 3.5  # 右に寄せて左側に大空間を確保
    offset_y = -0.5

    print(f"📦 Generating 3D High-End Cyber Grid ({cols}x{rows} = {cols*rows} elements)...")

    frames = range(1, total_frames + 1, 4)

    for r in range(rows):
        for c in range(cols):
            gx = (c - cols / 2.0) * spacing + offset_x
            gy = (r - rows / 2.0) * spacing + offset_y
            
            # 中心からの距離
            dist = math.sqrt((c - cols*0.4)**2 + (r - rows*0.45)**2)

            bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(0, 0, 0))
            cube = bpy.context.active_object
            cube.name = f"GridCube_{r}_{c}"

            # ベベルモディファイア（美しいエッジの光の反射）
            bev = cube.modifiers.new(name="Bevel", type='BEVEL')
            bev.width = 0.035
            bev.segments = 2

            # マテリアル割り当て（大半はダークメタル、一部が発光ノード）
            if (r + c) % 5 == 0:
                cube.data.materials.append(mat_cyan_accent)
            elif (r * c) % 7 == 0:
                cube.data.materials.append(mat_blue_accent)
            else:
                cube.data.materials.append(mat_dark_titanium)

            # 数学的シームレス波紋キーフレーム
            for f in frames:
                t = (f - 1) / total_frames # 0.0 -> 1.0 (完全ループ)
                phase = t * 2.0 * math.pi
                
                # 複合波動（滑らかな有機的波紋）
                wave1 = math.sin(phase * 2.0 - dist * 0.45)
                wave2 = math.cos(phase * 1.0 + (c * 0.3) - (r * 0.2))
                wave3 = math.sin(phase * 3.0 + dist * 0.15) * 0.25
                
                z_height = 0.3 + (wave1 * 0.8 + wave2 * 0.5 + wave3 + 1.4) * 0.65
                cube.location = (gx, gy, z_height / 2.0)
                cube.scale = (1.0, 1.0, z_height)
                
                cube.keyframe_insert(data_path="location", frame=f)
                cube.keyframe_insert(data_path="scale", frame=f)

    # 8. 浮遊するデータ通信パケット粒子（Neural Nodes）
    print("✨ Generating Floating Neural Pulse Nodes...")
    mat_packet_cyan = bpy.data.materials.new(name="MatPacketCyan")
    mat_packet_cyan.use_nodes = True
    nodes_pc = mat_packet_cyan.node_tree.nodes
    nodes_pc.clear()
    node_emit_pc = nodes_pc.new(type='ShaderNodeEmission')
    node_emit_pc.inputs['Color'].default_value = (0.3, 0.95, 1.0, 1.0)
    node_emit_pc.inputs['Strength'].default_value = 8.0
    node_out_pc = nodes_pc.new(type='ShaderNodeOutputMaterial')
    mat_packet_cyan.node_tree.links.new(node_emit_pc.outputs['Emission'], node_out_pc.inputs['Surface'])

    num_particles = 32
    for i in range(num_particles):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.065, location=(0, 0, 0))
        part = bpy.context.active_object
        part.name = f"NeuralNode_{i}"
        part.data.materials.append(mat_packet_cyan)

        orbit_r = 3.8 + (i % 7) * 1.2
        speed = 1.0 if (i % 2 == 0) else -1.0
        z_base = 1.2 + (i % 8) * 0.35
        phase_offset = (i / num_particles) * 2.0 * math.pi

        for f in frames:
            t = (f - 1) / total_frames
            angle = phase_offset + t * 2.0 * math.pi * speed
            px = offset_x + math.cos(angle) * orbit_r
            py = offset_y + math.sin(angle) * (orbit_r * 0.65)
            pz = z_base + math.sin(t * 4.0 * math.pi + i) * 0.35

            part.location = (px, py, pz)
            part.keyframe_insert(data_path="location", frame=f)

    # 9. カメラ設定（完全三脚固定 Locked-off ＆ 黄金コピースペース構図）
    print("🎥 Configuring Stationary Locked-off 4K Camera...")
    bpy.ops.object.camera_add(location=(-6.8, -16.5, 9.2))
    cam = bpy.context.active_object
    cam.name = "Stationary_4K_Camera"
    cam.rotation_euler = (math.radians(61), 0, math.radians(-23))
    cam.data.lens = 45.0

    # 被写界深度
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 18.0
    cam.data.dof.aperture_fstop = 2.8

    scene.camera = cam

    # 10. 保存
    os.makedirs(os.path.dirname(output_blend_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)
    print(f"✅ High-End Scene Saved to: {output_blend_path}")

if __name__ == "__main__":
    blend_path = "/Users/base/Automated-Projects/Adobe-Stock/3D_Animation/blender_projects/tech_data_grid_wave_4k.blend"
    setup_tech_data_grid_scene(blend_path, total_frames=240, fps=60)
