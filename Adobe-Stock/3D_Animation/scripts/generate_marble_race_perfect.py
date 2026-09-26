import bpy
import math
from pathlib import Path

def create_and_bake_marble_race():
    print("🚀 Building Perfect Marble Run Race (Guaranteed Course Navigation)...")
    
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    scene = bpy.context.scene
    fps = 30
    duration_sec = 18
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
            bsdf.inputs['Metallic'].default_value = 0.95
        ball_materials[name] = mat

    # ==========================================
    # 2. コース構造の生成 (高壁＆完全セーフティ)
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

    # --- セクション1: スタート〜第1スロープ (直進加速) ---
    # スロープ1 (傾斜 24度, 長さ 12m)
    add_ramp("Ramp_1", (0, 4.0, 18.5), (2.4, 12.0, 0.1), (24, 0, 0))
    add_wall("Ramp_1_Wall_L", (-1.2, 4.0, 19.3), (0.1, 12.2, 1.6), (24, 0, 0))
    add_wall("Ramp_1_Wall_R", (1.2, 4.0, 19.3), (0.1, 12.2, 1.6), (24, 0, 0))
    add_wall("Ramp_1_Wall_Back", (0, -1.8, 22.0), (2.5, 0.1, 2.0), (0, 0, 0))

    # --- セクション2: ターン1 ＆ 横スロープ ---
    add_ramp("Turn_1_Platform", (0, 10.5, 15.6), (3.6, 3.2, 0.1), (12, 0, 0))
    add_wall("Turn_1_Wall_Front", (0, 12.0, 16.6), (3.6, 0.1, 2.0), (0, 0, 0))
    add_wall("Turn_1_Wall_R", (1.8, 10.5, 16.6), (0.1, 3.2, 2.0), (0, 0, 0))

    # 横スロープ (右から左へ下降 - 18度傾斜)
    add_ramp("Ramp_2_Side", (-5.0, 10.2, 13.5), (9.0, 2.4, 0.1), (0, 18, 0))
    add_wall("Ramp_2_Wall_Back", (-5.0, 11.4, 14.3), (9.2, 0.1, 1.6), (0, 18, 0))
    add_wall("Ramp_2_Wall_Front", (-5.0, 9.0, 14.3), (9.2, 0.1, 1.6), (0, 18, 0))

    # ターン2受け皿 (左端)
    add_ramp("Turn_2_Platform", (-10.0, 10.2, 11.5), (3.0, 3.0, 0.1), (0, 8, 0))
    add_wall("Turn_2_Wall_L", (-11.5, 10.2, 12.5), (0.1, 3.0, 2.0), (0, 0, 0))
    add_wall("Turn_2_Wall_Back", (-10.0, 11.7, 12.5), (3.0, 0.1, 2.0), (0, 0, 0))

    # --- セクション3: ピンボール障害物ゾーン (Z=11 -> 5) ---
    # 左から中央前方向へ下降傾斜 (-20度, -12度)
    add_ramp("Plinko_Board", (-5.0, 4.5, 8.5), (9.0, 10.0, 0.1), (-20, -12, 0))
    add_wall("Plinko_Wall_L", (-9.5, 4.5, 9.3), (0.1, 10.2, 1.6), (-20, -12, 0))
    add_wall("Plinko_Wall_R", (-0.5, 4.5, 9.3), (0.1, 10.2, 1.6), (-20, -12, 0))

    pin_rows = 5
    for r in range(pin_rows):
        y_pin = 8.0 - (r * 1.8)
        cols = 3 if r % 2 == 0 else 4
        x_offset = -5.0 + (0.6 if r % 2 == 1 else 0.0)
        for c in range(cols):
            x_pin = x_offset + (c - cols/2.0 + 0.5) * 1.5
            z_pin = 8.5 + (8.0 - y_pin) * 0.35 + (x_pin + 5.0) * 0.20
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.2, location=(x_pin, y_pin, z_pin + 0.5))
            pin = bpy.context.active_object
            pin.name = f"Pin_{r}_{c}"
            bpy.ops.rigidbody.object_add()
            pin.rigid_body.type = 'PASSIVE'
            pin.rigid_body.collision_shape = 'CYLINDER'
            pin.rigid_body.restitution = 0.8
            pin.data.materials.append(mat_gold)

    # --- セクション4: スパイラル漏斗 / ファンネル (Z=4 -> 2) ---
    bpy.ops.mesh.primitive_cone_add(radius1=3.5, radius2=0.8, depth=2.0, location=(-3.0, -2.0, 3.8))
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
    funnel.rigid_body.restitution = 0.25
    funnel.data.materials.append(mat_track)

    # --- セクション5: ゴール直線レール ＆ フィニッシュライン (Z=2 -> 0) ---
    add_ramp("Finish_Ramp", (-3.0, -8.0, 1.2), (1.8, 10.0, 0.1), (15, 0, 0))
    add_wall("Finish_Wall_L", (-3.9, -8.0, 1.8), (0.1, 10.2, 1.2), (15, 0, 0))
    add_wall("Finish_Wall_R", (-2.1, -8.0, 1.8), (0.1, 10.2, 1.2), (15, 0, 0))
    add_wall("Finish_Stop_Wall", (-3.0, -13.0, 0.8), (2.0, 0.1, 1.5), (0, 0, 0))

    # ゴールゲートアーチ
    bpy.ops.mesh.primitive_torus_add(major_radius=0.95, minor_radius=0.08, location=(-3.0, -10.5, 1.2))
    gate = bpy.context.active_object
    gate.name = "Finish_Gate"
    gate.rotation_euler = (math.radians(90), 0, 0)
    gate.data.materials.append(mat_gold)

    # ==========================================
    # 3. 4色のマーブルボールの作成（スロープ上部に確実に着地）
    # ==========================================
    ball_names = ["Red", "Blue", "Green", "Yellow"]
    ball_objects = []
    
    # スロープ1の最上部内側に均等配置
    start_positions = [
        (-0.6, -0.5, 20.8), # Red
        (-0.2, -0.5, 20.8), # Blue
        (0.2, -0.5, 20.8),  # Green
        (0.6, -0.5, 20.8),  # Yellow
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
        (-5.0, 10.2, 18),
        (-5.0, 4.5, 13),
        (-3.0, -5.0, 6)
    ]
    for idx, lpos in enumerate(light_positions):
        bpy.ops.object.light_add(type='POINT', location=lpos)
        pt = bpy.context.active_object
        pt.data.energy = 700.0
        pt.data.color = (0.95, 0.98, 1.0)

    # ==========================================
    # 5. 【物理ベイク ➔ 座標取得 ➔ キーフレーム確定】
    # ==========================================
    print(f"⏳ Baking Rigid Body Physics simulation (1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics simulation baked successfully!")

    ball_trajectories = {b.name: [] for b in ball_objects}
    for frame in range(1, total_frames + 1):
        scene.frame_set(frame)
        for b in ball_objects:
            mat = b.matrix_world.copy()
            loc = mat.to_translation()
            rot = mat.to_euler()
            ball_trajectories[b.name].append((loc, rot))

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
    # 6. 先頭・重心ダイナミック追従カメラ
    # ==========================================
    print("🎥 Configuring Dynamic Auto-Follow Camera...")
    bpy.ops.object.camera_add(location=(0, -6.0, 24.0))
    camera = bpy.context.active_object
    camera.name = "Follow_Camera"
    scene.camera = camera
    
    for frame in range(1, total_frames + 1):
        locs = [ball_trajectories[name][frame - 1][0] for name in ball_trajectories]
        # 有効な（コース上にいる）ボールの重心を計算
        valid_locs = [loc for loc in locs if loc.z > -5.0]
        if not valid_locs:
            valid_locs = locs
            
        avg_x = sum(loc.x for loc in valid_locs) / len(valid_locs)
        avg_y = sum(loc.y for loc in valid_locs) / len(valid_locs)
        avg_z = sum(loc.z for loc in valid_locs) / len(valid_locs)
        
        cam_offset_x = 0.0
        cam_offset_y = -4.5
        cam_offset_z = 3.8
        
        camera.location = (avg_x + cam_offset_x, avg_y + cam_offset_y, avg_z + cam_offset_z)
        camera.rotation_euler = (math.radians(52), 0, 0)
        
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ Camera keyframes generated for all frames!")

    # ==========================================
    # 7. レンダリング設定
    # ==========================================
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.taa_render_samples = 16
    scene.render.resolution_x = 720
    scene.render.resolution_y = 1280
    scene.render.resolution_percentage = 100
    
    frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_race_perfect")
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames_dir / "frame_")
    scene.render.image_settings.file_format = 'PNG'

    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_file = blend_dir / "marble_run_race_perfect.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend file saved successfully: {blend_file}")

if __name__ == "__main__":
    create_and_bake_marble_race()
