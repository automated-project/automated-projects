import bpy
import math
from pathlib import Path

def create_and_bake_marble_race():
    print("🚀 Building Fixed Marble Race Scene (v3 with CONVEX_HULL & Auto-Cam)...")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    scene = bpy.context.scene
    fps = 30
    duration_sec = 18 # 18秒間
    total_frames = fps * duration_sec # 540フレーム
    
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

    # ==========================================
    # 1. マテリアル作成
    # ==========================================
    mat_track = bpy.data.materials.new(name="Mat_Track")
    bsdf = mat_track.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.08, 0.09, 0.12, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Metallic'].default_value = 0.2

    mat_gold = bpy.data.materials.new(name="Mat_Gold")
    bsdf = mat_gold.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.8, 0.2, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.15
        bsdf.inputs['Metallic'].default_value = 0.9

    ball_colors = {
        "Red": (0.95, 0.05, 0.1, 1.0),
        "Blue": (0.05, 0.4, 1.0, 1.0),
        "Green": (0.05, 0.9, 0.15, 1.0),
        "Yellow": (1.0, 0.85, 0.0, 1.0),
    }
    ball_materials = {}
    for name, col in ball_colors.items():
        mat = bpy.data.materials.new(name=f"Mat_{name}")
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = col
            bsdf.inputs['Roughness'].default_value = 0.05
            bsdf.inputs['Metallic'].default_value = 0.9
        ball_materials[name] = mat

    # ==========================================
    # 2. コース構造の生成 (CONVEX_HULL コリジョン)
    # ==========================================
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

    # --- セクション1: 急傾斜スタートスロープ (26度前傾斜 / Z=22 -> 15) ---
    add_ramp("Ramp_1", (0, 3.5, 18.5), (2.2, 12.0, 0.1), (26, 0, 0))
    add_wall("Ramp_1_Wall_L", (-1.1, 3.5, 19.0), (0.1, 12.2, 1.0), (26, 0, 0))
    add_wall("Ramp_1_Wall_R", (1.1, 3.5, 19.0), (0.1, 12.2, 1.0), (26, 0, 0))
    add_wall("Ramp_1_Wall_Back", (0, -2.5, 21.5), (2.2, 0.1, 1.2), (0, 0, 0))

    # --- セクション2: 第1カーブ ＆ 横スロープ (Z=15 -> 10) ---
    add_ramp("Turn_1_Platform", (0, 9.5, 14.8), (3.0, 2.5, 0.1), (10, 0, 0))
    add_wall("Turn_1_Wall_Front", (0, 10.8, 15.6), (3.2, 0.1, 1.5), (0, 0, 0))
    add_wall("Turn_1_Wall_R", (1.5, 9.5, 15.6), (0.1, 2.5, 1.5), (0, 0, 0))

    # 横スロープ (右から左へ下降 - 20度傾斜)
    add_ramp("Ramp_2_Side", (-4.5, 8.8, 12.5), (8.0, 2.0, 0.1), (0, 20, 0))
    add_wall("Ramp_2_Wall_Back", (-4.5, 9.8, 13.1), (8.2, 0.1, 1.0), (0, 20, 0))
    add_wall("Ramp_2_Wall_Front", (-4.5, 7.8, 13.1), (8.2, 0.1, 1.0), (0, 20, 0))

    # ターン2受け皿 (左端)
    add_ramp("Turn_2_Platform", (-9.0, 8.8, 9.8), (2.4, 2.4, 0.1), (0, 5, 0))
    add_wall("Turn_2_Wall_L", (-10.2, 8.8, 10.6), (0.1, 2.4, 1.5), (0, 0, 0))
    add_wall("Turn_2_Wall_Back", (-9.0, 10.0, 10.6), (2.4, 0.1, 1.5), (0, 0, 0))

    # --- セクション3: ピンボール障害物ゾーン (Z=9 -> 4) ---
    add_ramp("Plinko_Board", (-4.5, 4.0, 6.8), (8.5, 9.0, 0.1), (-22, -12, 0))
    add_wall("Plinko_Wall_L", (-8.8, 4.0, 7.5), (0.1, 9.2, 1.2), (-22, -12, 0))
    add_wall("Plinko_Wall_R", (-0.2, 4.0, 7.5), (0.1, 9.2, 1.2), (-22, -12, 0))

    pin_rows = 4
    for r in range(pin_rows):
        y_pin = 7.0 - (r * 2.0)
        cols = 3 if r % 2 == 0 else 4
        x_offset = -4.5 + (0.6 if r % 2 == 1 else 0.0)
        for c in range(cols):
            x_pin = x_offset + (c - cols/2.0 + 0.5) * 1.5
            z_pin = 6.8 + (7.0 - y_pin) * 0.38 + (x_pin + 4.5) * 0.18
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.0, location=(x_pin, y_pin, z_pin + 0.4))
            pin = bpy.context.active_object
            pin.name = f"Pin_{r}_{c}"
            bpy.ops.rigidbody.object_add()
            pin.rigid_body.type = 'PASSIVE'
            pin.rigid_body.collision_shape = 'CYLINDER'
            pin.rigid_body.restitution = 0.8
            pin.data.materials.append(mat_gold)

    # --- セクション4: すり鉢ファンネル (Z=3 -> 1) ---
    bpy.ops.mesh.primitive_cone_add(radius1=3.0, radius2=0.8, depth=1.8, location=(-3.0, -1.5, 2.6))
    funnel = bpy.context.active_object
    funnel.name = "Funnel_Bowl"
    funnel.rotation_euler = (math.radians(180), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = 0.15
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    bpy.ops.rigidbody.object_add()
    funnel.rigid_body.type = 'PASSIVE'
    funnel.rigid_body.collision_shape = 'MESH'
    funnel.rigid_body.friction = 0.01
    funnel.rigid_body.restitution = 0.2
    funnel.data.materials.append(mat_track)

    # --- セクション5: ゴール直線レール ＆ フィニッシュライン (Z=1 -> 0) ---
    add_ramp("Finish_Ramp", (-3.0, -7.0, 0.7), (1.6, 9.0, 0.1), (15, 0, 0))
    add_wall("Finish_Wall_L", (-3.8, -7.0, 1.1), (0.1, 9.2, 0.8), (15, 0, 0))
    add_wall("Finish_Wall_R", (-2.2, -7.0, 1.1), (0.1, 9.2, 0.8), (15, 0, 0))
    add_wall("Finish_Stop_Wall", (-3.0, -11.5, 0.5), (1.8, 0.1, 1.2), (0, 0, 0))

    # ゴールゲートアーチ
    bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.08, location=(-3.0, -9.0, 0.7))
    gate = bpy.context.active_object
    gate.name = "Finish_Gate"
    gate.rotation_euler = (math.radians(90), 0, 0)
    gate.data.materials.append(mat_gold)

    # ==========================================
    # 3. 4色のマーブルボールの作成
    # ==========================================
    ball_names = ["Red", "Blue", "Green", "Yellow"]
    ball_objects = []
    
    start_positions = [
        (-0.6, -1.0, 21.8), # Red
        (-0.2, -1.0, 21.8), # Blue
        (0.2, -1.0, 21.8),  # Green
        (0.6, -1.0, 21.8),  # Yellow
    ]
    
    for i, name in enumerate(ball_names):
        pos = start_positions[i]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=pos)
        ball = bpy.context.active_object
        ball.name = f"Marble_{name}"
        
        bpy.ops.rigidbody.object_add()
        ball.rigid_body.type = 'ACTIVE'
        ball.rigid_body.mass = 4.0
        ball.rigid_body.friction = 0.01
        ball.rigid_body.restitution = 0.35
        ball.rigid_body.collision_shape = 'SPHERE'
        ball.rigid_body.linear_damping = 0.005
        ball.rigid_body.angular_damping = 0.005
        
        ball.data.materials.append(ball_materials[name])
        ball_objects.append(ball)

    # ==========================================
    # 4. ライティング
    # ==========================================
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 30))
    sun = bpy.context.active_object
    sun.data.energy = 4.5
    sun.rotation_euler = (math.radians(50), math.radians(20), math.radians(35))

    light_positions = [
        (0, 5, 24),
        (-4.5, 10.2, 18),
        (-4.5, 5.0, 12),
        (-3.0, -4.0, 6)
    ]
    for idx, lpos in enumerate(light_positions):
        bpy.ops.object.light_add(type='POINT', location=lpos)
        pt = bpy.context.active_object
        pt.data.energy = 700.0
        pt.data.color = (0.95, 0.98, 1.0)

    # ==========================================
    # 5. 【剛体物理ベイク ➔ キーフレーム確定保存】
    # ==========================================
    print(f"⏳ Baking Rigid Body Physics simulation (1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics simulation baked successfully!")

    # ベイクされた座標を読み取り、キーフレームアニメーションに変換
    ball_trajectories = {b.name: [] for b in ball_objects}
    for frame in range(1, total_frames + 1):
        scene.frame_set(frame)
        for b in ball_objects:
            mat = b.matrix_world.copy()
            loc = mat.to_translation()
            rot = mat.to_euler()
            ball_trajectories[b.name].append((loc, rot))

    # 剛体を削除し、直接キーフレーム登録
    for b in ball_objects:
        bpy.ops.object.select_all(action='DESELECT')
        b.select_set(True)
        bpy.context.view_layer.objects.active = b
        bpy.ops.rigidbody.object_remove()
        
        for frame, (loc, rot) in enumerate(ball_trajectories[b.name], start=1):
            b.location = loc
            b.rotation_euler = rot
            b.keyframe_insert(data_path="location", frame=frame)
            b.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ Physics trajectories transformed to absolute keyframes!")

    # ==========================================
    # 6. ボール重心へのダイナミック追従カメラ
    # ==========================================
    print("🎥 Configuring Dynamic Auto-Follow Camera...")
    bpy.ops.object.camera_add(location=(0, -6.0, 24.0))
    camera = bpy.context.active_object
    camera.name = "Follow_Camera"
    scene.camera = camera
    
    for frame in range(1, total_frames + 1):
        locs = [ball_trajectories[name][frame - 1][0] for name in ball_trajectories]
        avg_x = sum(loc.x for loc in locs) / len(locs)
        avg_y = sum(loc.y for loc in locs) / len(locs)
        avg_z = sum(loc.z for loc in locs) / len(locs)
        
        # カメラ位置 (ボール重心の上空斜め後ろから見下ろす)
        cam_offset_x = 0.0
        cam_offset_y = -4.2
        cam_offset_z = 3.6
        
        camera.location = (avg_x + cam_offset_x, avg_y + cam_offset_y, avg_z + cam_offset_z)
        camera.rotation_euler = (math.radians(52), 0, 0)
        
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ Camera keyframes generated for all frames!")

    # ==========================================
    # 7. レンダリング設定 (720x1280 縦型 Shorts)
    # ==========================================
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.taa_render_samples = 16
    scene.render.resolution_x = 720
    scene.render.resolution_y = 1280
    scene.render.resolution_percentage = 100
    
    frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_race_v3")
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames_dir / "frame_")
    scene.render.image_settings.file_format = 'PNG'

    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_file = blend_dir / "marble_run_race_v3.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend file saved successfully: {blend_file}")

if __name__ == "__main__":
    create_and_bake_marble_race()
