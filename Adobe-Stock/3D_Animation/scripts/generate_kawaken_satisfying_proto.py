"""
Kawaken 3DCG スタイル / 大量カラフルボールのすり鉢＆スパイラル・ファンネル ASMR
・75個のカラフルキャンディボールが上空から一斉シャワー落下
・巨大すり鉢（ファンネル）の内部で渦を巻きながら中央穴に吸い込まれる
・下部ガラスシリンダーへ美しくパイルアップ（ストック）
・正面やや見下ろしのアングルで全貌と吸い込みの満足感を完全キャプチャ
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Euler
from pathlib import Path
import wave
import struct

def create_kawaken_satisfying_simulation():
    fps = 30
    duration_sec = 8
    total_frames = fps * duration_sec
    num_balls = 75

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = total_frames
    
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames
    rb_world.substeps_per_frame = 50
    rb_world.solver_iterations = 50

    print("🔮 Building Perfectly Framed Kawaken Funnel Simulation...")

    # マテリアル
    def make_mat(name, color, metallic=0.0, roughness=0.1, transmission=0.0, ior=1.45):
        mat = bpy.data.materials.new(name=name)
        nodes = mat.node_tree.nodes
        p = nodes.get("Principled BSDF")
        if p:
            p.inputs['Base Color'].default_value = color
            p.inputs['Metallic'].default_value = metallic
            p.inputs['Roughness'].default_value = roughness
            if 'Transmission Weight' in p.inputs:
                p.inputs['Transmission Weight'].default_value = transmission
            elif 'Transmission' in p.inputs:
                p.inputs['Transmission'].default_value = transmission
            if 'IOR' in p.inputs:
                p.inputs['IOR'].default_value = ior
        return mat

    mat_floor = make_mat("Studio_Floor", (0.94, 0.95, 0.97, 1.0), roughness=0.15)
    mat_backwall = make_mat("Studio_Backwall", (0.88, 0.92, 0.96, 1.0), roughness=0.35)
    mat_funnel = make_mat("Frosted_Acrylic", (0.95, 0.95, 0.98, 1.0), roughness=0.12, transmission=0.6)
    mat_glass = make_mat("Clear_Glass", (0.98, 0.98, 1.0, 1.0), roughness=0.05, transmission=0.92, ior=1.5)
    mat_gold = make_mat("Polished_Gold", (0.95, 0.78, 0.35, 1.0), metallic=0.9, roughness=0.15)

    ball_colors = [
        (1.00, 0.22, 0.38, 1.0), # ルビーピンク
        (1.00, 0.55, 0.15, 1.0), # オレンジ
        (1.00, 0.85, 0.20, 1.0), # レモンイエロー
        (0.20, 0.85, 0.50, 1.0), # エメラルドグリーン
        (0.18, 0.70, 1.00, 1.0), # オーシャンシアン
        (0.68, 0.38, 0.95, 1.0), # パープル
    ]
    ball_mats = [make_mat(f"Ball_Mat_{i+1}", col, metallic=0.05, roughness=0.08) for i, col in enumerate(ball_colors)]

    # 床 ＆ バックドロップ壁
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    floor.data.materials.append(mat_floor)
    bpy.ops.rigidbody.object_add()
    floor.rigid_body.type = 'PASSIVE'
    floor.rigid_body.collision_shape = 'BOX'

    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 10.0, 10.0))
    backwall = bpy.context.active_object
    backwall.name = "Studio_Backwall"
    backwall.rotation_euler = (math.radians(-90), 0, 0)
    backwall.data.materials.append(mat_backwall)

    # 巨大ファンネル (上径R=2.8, 下径R=0.55, 高さH=2.8, Z=3.2)
    # カメラの正面・中央に配置
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=2.8, radius2=0.55, depth=2.8, location=(0, 0, 3.2))
    funnel = bpy.context.active_object
    funnel.name = "Satisfying_Funnel"
    bpy.ops.object.shade_smooth()
    
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(funnel.data)
    del_faces = [f for f in bm.faces if abs(f.normal.z) > 0.8]
    bmesh.ops.delete(bm, geom=del_faces, context='FACES')
    bmesh.update_edit_mesh(funnel.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    mod_sol = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_sol.thickness = 0.10
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    mod_bev = funnel.modifiers.new(name="Bevel", type='BEVEL')
    mod_bev.width = 0.02
    mod_bev.segments = 2
    bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_smooth()

    funnel.data.materials.append(mat_funnel)
    bpy.ops.rigidbody.object_add()
    funnel.rigid_body.type = 'PASSIVE'
    funnel.rigid_body.collision_shape = 'MESH'
    funnel.rigid_body.friction = 0.02
    funnel.rigid_body.restitution = 0.35

    # 上部ゴールドリング
    bpy.ops.mesh.primitive_torus_add(major_radius=2.8, minor_radius=0.08, location=(0, 0, 4.6))
    ring_top = bpy.context.active_object
    ring_top.name = "Gold_Ring_Top"
    bpy.ops.object.shade_smooth()
    ring_top.data.materials.append(mat_gold)

    # 下部ガラスシリンダー (落ちたボールが美しくストックされる)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.75, depth=1.8, location=(0, 0, 0.9))
    cylinder = bpy.context.active_object
    cylinder.name = "Glass_Cylinder"
    bpy.ops.object.shade_smooth()

    bpy.ops.object.mode_set(mode='EDIT')
    bm_c = bmesh.from_edit_mesh(cylinder.data)
    del_c_faces = [f for f in bm_c.faces if f.normal.z > 0.8]
    bmesh.ops.delete(bm_c, geom=del_c_faces, context='FACES')
    bmesh.update_edit_mesh(cylinder.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    mod_sol_c = cylinder.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_sol_c.thickness = 0.08
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    cylinder.data.materials.append(mat_glass)
    bpy.ops.rigidbody.object_add()
    cylinder.rigid_body.type = 'PASSIVE'
    cylinder.rigid_body.collision_shape = 'MESH'
    cylinder.rigid_body.friction = 0.4
    cylinder.rigid_body.restitution = 0.15

    # 75個のボールスポーン（ファンネル上空 R: 1.0〜2.4, Z: 5.2〜8.5）
    print(f"🫧 Spawning {num_balls} colorful physics balls...")
    random.seed(42)
    balls = []
    ball_radius = 0.18

    for i in range(num_balls):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.8, 2.4)
        bx = r * math.cos(angle)
        by = r * math.sin(angle)
        bz = 5.2 + (i // 5) * 0.45 + random.uniform(0.0, 0.15)

        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=ball_radius, location=(bx, by, bz))
        b_obj = bpy.context.active_object
        b_obj.name = f"Ball_{i+1:03d}"
        bpy.ops.object.shade_smooth()
        
        mat_idx = i % len(ball_mats)
        b_obj.data.materials.append(ball_mats[mat_idx])

        bpy.ops.rigidbody.object_add()
        b_obj.rigid_body.type = 'ACTIVE'
        b_obj.rigid_body.mass = 1.0
        b_obj.rigid_body.friction = 0.03
        b_obj.rigid_body.restitution = 0.45
        b_obj.rigid_body.linear_damping = 0.02
        b_obj.rigid_body.angular_damping = 0.02

        balls.append(b_obj)

    # ライティング
    bpy.ops.object.light_add(type='AREA', location=(4.0, -5.0, 8.5))
    l_key = bpy.context.active_object
    l_key.data.energy = 950.0
    l_key.data.size = 6.0
    l_key.data.color = (1.0, 0.98, 0.95)
    l_key.rotation_euler = (math.radians(45), math.radians(25), math.radians(20))

    bpy.ops.object.light_add(type='AREA', location=(-4.0, -4.5, 7.5))
    l_fill = bpy.context.active_object
    l_fill.data.energy = 650.0
    l_fill.data.size = 5.0
    l_fill.data.color = (0.94, 0.97, 1.0)
    l_fill.rotation_euler = (math.radians(45), math.radians(-25), math.radians(-20))

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 15))
    l_sun = bpy.context.active_object
    l_sun.data.energy = 3.5
    l_sun.data.color = (1.0, 1.0, 1.0)

    # 物理ベイク
    print(f"⏳ Simulating & Baking 75-Ball Physics (1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics simulation completed!")

    ball_trajectories = [[] for _ in range(num_balls)]

    for frame in range(1, total_frames + 1):
        scene.frame_set(frame)
        for i, b_obj in enumerate(balls):
            ball_trajectories[i].append((b_obj.matrix_world.to_translation().copy(), b_obj.matrix_world.to_euler().copy()))

    for i, b_obj in enumerate(balls):
        bpy.ops.object.select_all(action='DESELECT')
        b_obj.select_set(True)
        bpy.context.view_layer.objects.active = b_obj
        bpy.ops.rigidbody.object_remove()
        
        for frame, (loc, rot) in enumerate(ball_trajectories[i], start=1):
            b_obj.location = loc
            b_obj.rotation_euler = rot
            b_obj.keyframe_insert(data_path="location", frame=frame)
            b_obj.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ All 75 ball trajectories baked to keyframes!")

    # 【最適なKawakenカメラアングル】
    # Y=-6.2, Z=5.0からすり鉢の口（Z=4.6）と底のシリンダー（Z=0.9）を完璧に見下ろす画角
    print("🎥 Configuring Perfect Kawaken Satisfying Camera Angle...")
    bpy.ops.object.camera_add(location=(0.0, -6.2, 5.0))
    cam = bpy.context.active_object
    cam.name = "Satisfying_Camera"
    cam.data.lens = 42
    
    # すり鉢の中心（0, 0, 2.8）を注視
    direction = Vector((0.0, 0.0, 2.8)) - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()
    
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 6.4
    cam.data.dof.aperture_fstop = 3.5
    scene.camera = cam

    # レンダリング設定 (1080x1920 9:16 Shorts)
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    render_out_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames")
    render_out_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(render_out_dir / "frame_")

    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_path = blend_dir / "kawaken_satisfying_proto.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"✅ Blend file saved successfully: {blend_path}")

    # ASMR音響
    sample_rate = 44100
    total_samples = int(duration_sec * sample_rate)
    audio_data = [0.0] * total_samples

    funnel_pass_frames = []
    for traj in ball_trajectories:
        for f in range(1, total_frames):
            z_curr = traj[f-1][0].z
            z_next = traj[f][0].z
            if z_curr >= 2.0 > z_next:
                funnel_pass_frames.append(f)
                break

    for s in range(total_samples):
        t = s / sample_rate
        env = math.exp(-0.5 * ((t - 3.2) / 1.6) ** 2)
        noise = (math.sin(2 * math.pi * 220 * t) * 0.3 + 
                 math.sin(2 * math.pi * 440 * t) * 0.2 +
                 math.sin(2 * math.pi * 880 * t) * 0.1)
        audio_data[s] += noise * env * 0.08

    pitches = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98]
    for i, pf in enumerate(funnel_pass_frames):
        start_s = int((pf / fps) * sample_rate)
        pitch = pitches[i % len(pitches)]
        for s in range(int(0.12 * sample_rate)):
            if start_s + s >= total_samples:
                break
            t = s / sample_rate
            decay = math.exp(-30.0 * t)
            wave_val = math.sin(2 * math.pi * pitch * t) + 0.3 * math.sin(2 * math.pi * (pitch * 2.0) * t)
            audio_data[start_s + s] += wave_val * decay * 0.18

    audio_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets")
    audio_dir.mkdir(parents=True, exist_ok=True)
    wav_path = audio_dir / "kawaken_satisfying_soundscape.wav"
    
    with wave.open(str(wav_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for sample in audio_data:
            clamped = max(-1.0, min(1.0, sample))
            packed_val = struct.pack('<h', int(clamped * 32767))
            wf.writeframes(packed_val)

    print(f"✅ Satisfying ASMR Audio generated at: {wav_path}")

if __name__ == "__main__":
    create_kawaken_satisfying_simulation()
