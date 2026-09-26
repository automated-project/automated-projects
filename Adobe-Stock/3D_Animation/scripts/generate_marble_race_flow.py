import bpy
import bmesh
import math
from pathlib import Path

def build_marble_race_flow():
    print("🏁 Building High-Speed Pure Flow Marble Run Race...")
    
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
    rb_world.substeps_per_frame = 25
    rb_world.solver_iterations = 50
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames

    # ==========================================
    # 1. マテリアル
    # ==========================================
    mat_track = bpy.data.materials.new(name="Mat_Track")
    bsdf = mat_track.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.08, 0.09, 0.12, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Metallic'].default_value = 0.3

    mat_gold = bpy.data.materials.new(name="Mat_Gold")
    bsdf = mat_gold.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.82, 0.18, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.1
        bsdf.inputs['Metallic'].default_value = 0.95

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
    # 2. BMeshで一直線＆ファンネル＆ピンゾーンの一体型コースを構築
    # ==========================================
    track_mesh = bpy.data.meshes.new('Track_Mesh')
    track_obj = bpy.data.objects.new('Track_Master', track_mesh)
    scene.collection.objects.link(track_obj)
    
    bm = bmesh.new()

    def add_quad_rail(p_left_start, p_right_start, p_left_end, p_right_end, wall_h=1.4):
        v_ls_top = bm.verts.new((p_left_start[0], p_left_start[1], p_left_start[2] + wall_h))
        v_ls_bot = bm.verts.new(p_left_start)
        v_rs_bot = bm.verts.new(p_right_start)
        v_rs_top = bm.verts.new((p_right_start[0], p_right_start[1], p_right_start[2] + wall_h))

        v_le_top = bm.verts.new((p_left_end[0], p_left_end[1], p_left_end[2] + wall_h))
        v_le_bot = bm.verts.new(p_left_end)
        v_re_bot = bm.verts.new(p_right_end)
        v_re_top = bm.verts.new((p_right_end[0], p_right_end[1], p_right_end[2] + wall_h))

        bm.faces.new([v_ls_top, v_ls_bot, v_le_bot, v_le_top]) # 左壁
        bm.faces.new([v_ls_bot, v_rs_bot, v_re_bot, v_le_bot]) # 底面
        bm.faces.new([v_rs_bot, v_rs_top, v_re_top, v_re_bot]) # 右壁

    # --- セクション1: スタート〜第1急傾斜スロープ (Y: -2 -> 10, Z: 24 -> 14) ---
    add_quad_rail((-1.1, -2.0, 24.0), (1.1, -2.0, 24.0), (-1.1, 10.0, 14.0), (1.1, 10.0, 14.0), wall_h=1.6)
    
    # スタート後ろ壁
    bm.faces.new([
        bm.verts.new((-1.1, -2.0, 25.6)),
        bm.verts.new((-1.1, -2.0, 24.0)),
        bm.verts.new((1.1, -2.0, 24.0)),
        bm.verts.new((1.1, -2.0, 25.6))
    ])

    # --- セクション2: ファンネル投入口 ＆ ピンゾーン (Y: 10 -> 22, Z: 14 -> 5) ---
    # 幅広スロープ (幅3.6m / X: -1.8 ~ 1.8)
    add_quad_rail((-1.1, 10.0, 14.0), (1.1, 10.0, 14.0), (-2.0, 13.0, 12.0), (2.0, 13.0, 12.0), wall_h=1.8)
    add_quad_rail((-2.0, 13.0, 12.0), (2.0, 13.0, 12.0), (-2.0, 24.0, 4.0), (2.0, 24.0, 4.0), wall_h=1.8)

    # --- セクション3: 絞り込み ＆ ゴール直線 (Y: 24 -> 36, Z: 4 -> 0) ---
    add_quad_rail((-2.0, 24.0, 4.0), (2.0, 24.0, 4.0), (-1.0, 27.0, 2.5), (1.0, 27.0, 2.5), wall_h=1.6)
    add_quad_rail((-1.0, 27.0, 2.5), (1.0, 27.0, 2.5), (-1.0, 38.0, 0.0), (1.0, 38.0, 0.0), wall_h=1.6)

    # ゴールストップ壁 (Y=38.0)
    bm.faces.new([
        bm.verts.new((-1.0, 38.0, 1.6)),
        bm.verts.new((-1.0, 38.0, 0.0)),
        bm.verts.new((1.0, 38.0, 0.0)),
        bm.verts.new((1.0, 38.0, 1.6))
    ])

    bm.to_mesh(track_mesh)
    bm.free()

    track_obj.data.materials.append(mat_track)
    
    # 剛体設定 (PASSIVE / MESH)
    bpy.context.view_layer.objects.active = track_obj
    bpy.ops.rigidbody.object_add()
    track_obj.rigid_body.type = 'PASSIVE'
    track_obj.rigid_body.collision_shape = 'MESH'
    track_obj.rigid_body.friction = 0.005
    track_obj.rigid_body.restitution = 0.3

    # --- ピン障害物（セクション2のピンゾーン Y: 14 ~ 23） ---
    pin_rows = 6
    for r in range(pin_rows):
        y_pin = 14.5 + (r * 1.5)
        cols = 3 if r % 2 == 0 else 4
        x_span = 2.4
        for c in range(cols):
            x_pin = -x_span/2.0 + (c + 0.5) * (x_span / cols)
            # スロープのZ座標計算
            z_pin = 12.0 - ((y_pin - 13.0) / 11.0) * 8.0 + 0.4
            bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=1.2, location=(x_pin, y_pin, z_pin))
            pin = bpy.context.active_object
            pin.name = f"Pin_{r}_{c}"
            bpy.ops.rigidbody.object_add()
            pin.rigid_body.type = 'PASSIVE'
            pin.rigid_body.collision_shape = 'CYLINDER'
            pin.rigid_body.restitution = 0.85
            pin.data.materials.append(mat_gold)

    # ゴールゲートアーチ (Y=34.0)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.08, location=(0, 34.0, 0.8))
    gate = bpy.context.active_object
    gate.name = "Finish_Gate"
    gate.rotation_euler = (math.radians(90), 0, 0)
    gate.data.materials.append(mat_gold)

    # ==========================================
    # 3. 4色のマーブルボールの作成
    # ==========================================
    ball_names = ["Red", "Blue", "Green", "Yellow"]
    ball_objects = []
    
    # スタート地点 (Y: -1.0, Z: 23.5)
    start_positions = [
        (-0.6, -1.0, 23.6), # Red
        (-0.2, -1.0, 23.6), # Blue
        (0.2, -1.0, 23.6),  # Green
        (0.6, -1.0, 23.6),  # Yellow
    ]
    
    for i, name in enumerate(ball_names):
        pos = start_positions[i]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=pos)
        ball = bpy.context.active_object
        ball.name = f"Marble_{name}"
        
        bpy.ops.rigidbody.object_add()
        ball.rigid_body.type = 'ACTIVE'
        ball.rigid_body.mass = 3.5
        ball.rigid_body.friction = 0.005
        ball.rigid_body.restitution = 0.4
        ball.rigid_body.collision_shape = 'SPHERE'
        ball.rigid_body.linear_damping = 0.002
        ball.rigid_body.angular_damping = 0.002
        
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
        (0, 5, 25),
        (0, 18, 16),
        (0, 30, 8),
    ]
    for idx, lpos in enumerate(light_positions):
        bpy.ops.object.light_add(type='POINT', location=lpos)
        pt = bpy.context.active_object
        pt.data.energy = 800.0
        pt.data.color = (0.95, 0.98, 1.0)

    # ==========================================
    # 5. 【物理ベイク ➔ キーフレーム確定】
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
        avg_x = sum(loc.x for loc in locs) / len(locs)
        avg_y = sum(loc.y for loc in locs) / len(locs)
        avg_z = sum(loc.z for loc in locs) / len(locs)
        
        # ボール重心の真後ろ上空から見下ろす (迫力のレース視点)
        cam_offset_x = 0.0
        cam_offset_y = -4.5
        cam_offset_z = 3.6
        
        camera.location = (avg_x + cam_offset_x, avg_y + cam_offset_y, avg_z + cam_offset_z)
        camera.rotation_euler = (math.radians(55), 0, 0)
        
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
    
    frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_race_flow")
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames_dir / "frame_")
    scene.render.image_settings.file_format = 'PNG'

    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_file = blend_dir / "marble_run_race_flow.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend file saved successfully: {blend_file}")

if __name__ == "__main__":
    build_marble_race_flow()
