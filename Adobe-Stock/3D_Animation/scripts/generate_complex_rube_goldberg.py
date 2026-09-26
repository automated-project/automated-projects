"""
本格ピタゴラスイッチ / ASMR からくり複合コース
構成ギミック（全5段階の豪華連鎖）：
1. らせんスパイラルタワー（上空からくるくると滑らかに旋回下降）
2. シーソーバランサー（ボールの自重でカタンと傾き、下のドミノへバトンタッチ）
3. 5連カラフルドミノ（パタパタパタッと連鎖倒れ）
4. 4段マカロン木琴ステップ（C5 -> E5 -> G5 -> C6 と心地よく音階バウンド）
5. 手前ゴールカップ＆ポップアップフラッグ（正面カメラに向かってスポッとゴール！）

特徴：
・モジュール化された使い回し設計
・一眼レフ風の被写界深度（DoF）
・正面ダイナミック追従カメラ
・完全同期のフルASMR音響（スパイラル摩擦音＋シーソー傾き音＋ドミノ＋木琴＋ゴールベル）
"""

import bpy
import bmesh
import math
from mathutils import Vector, Euler
from pathlib import Path
import wave
import struct

def build_complex_toy_machine():
    fps = 30
    duration_sec = 10 # 10秒の充実した展開
    total_frames = fps * duration_sec

    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = total_frames
    
    # 物理ワールド
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames
    rb_world.substeps_per_frame = 60
    rb_world.solver_iterations = 60

    print("🚀 Building Complex Multi-Gimmick Toy ASMR Machine (Spiral -> Seesaw -> Domino -> Xylo -> Goal)...")

    # ==========================================
    # 2. マテリアルパレット
    # ==========================================
    def make_mat(name, color, metallic=0.0, roughness=0.25):
        mat = bpy.data.materials.new(name=name)
        nodes = mat.node_tree.nodes
        p = nodes.get("Principled BSDF")
        if p:
            p.inputs['Base Color'].default_value = color
            p.inputs['Metallic'].default_value = metallic
            p.inputs['Roughness'].default_value = roughness
        return mat

    mat_floor = make_mat("Playroom_Floor", (0.94, 0.95, 0.97, 1.0), roughness=0.2)
    mat_backwall = make_mat("Studio_Backwall", (0.88, 0.92, 0.96, 1.0), roughness=0.35)
    mat_wood = make_mat("Toy_Birch_Wood", (0.94, 0.86, 0.72, 1.0), roughness=0.35)
    mat_seesaw = make_mat("Toy_Teal_Plank", (0.20, 0.75, 0.80, 1.0), roughness=0.2)
    mat_pivot = make_mat("Polished_Gold", (0.95, 0.78, 0.35, 1.0), metallic=0.85, roughness=0.15)
    
    # キャンディボール
    mat_ball = make_mat("Candy_Ball", (1.0, 0.22, 0.40, 1.0), metallic=0.05, roughness=0.08)

    # 5連ドミノ
    domino_colors = [
        (1.0, 0.45, 0.20, 1.0), # オレンジ
        (1.0, 0.82, 0.25, 1.0), # イエロー
        (0.45, 0.88, 0.30, 1.0), # ライム
        (0.20, 0.78, 0.95, 1.0), # シアン
        (0.65, 0.45, 0.90, 1.0), # パープル
    ]
    domino_mats = [make_mat(f"Domino_{i+1}", col, roughness=0.2) for i, col in enumerate(domino_colors)]

    # 4段木琴
    xylo_colors = [
        (1.0, 0.45, 0.48, 1.0), # C5
        (1.0, 0.82, 0.32, 1.0), # E5
        (0.35, 0.90, 0.68, 1.0), # G5
        (0.35, 0.72, 1.0, 1.0),  # C6
    ]
    xylo_mats = [make_mat(f"Xylo_{i+1}", col, roughness=0.2) for i, col in enumerate(xylo_colors)]
    
    mat_cup = make_mat("Lavender_Cup", (0.75, 0.48, 0.95, 1.0), roughness=0.15)
    mat_flag = make_mat("Flag_Red", (1.0, 0.18, 0.25, 1.0), roughness=0.3)

    # ==========================================
    # 3. スタジオ空間（床 ＋ バックドロップ壁 ＋ 背景デコレーション）
    # ==========================================
    bpy.ops.mesh.primitive_plane_add(size=70, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Playroom_Floor"
    floor.data.materials.append(mat_floor)
    bpy.ops.rigidbody.object_add()
    floor.rigid_body.type = 'PASSIVE'
    floor.rigid_body.collision_shape = 'BOX'

    bpy.ops.mesh.primitive_plane_add(size=50, location=(0, -9.0, 10.0))
    backwall = bpy.context.active_object
    backwall.name = "Studio_Backwall"
    backwall.rotation_euler = (math.radians(90), 0, 0)
    backwall.data.materials.append(mat_backwall)

    # 背景積み木（ボケ味用）
    bpy.ops.mesh.primitive_cube_add(size=1.8, location=(-3.8, -5.5, 0.9))
    b1 = bpy.context.active_object
    b1.rotation_euler = (0, 0, math.radians(25))
    b1.data.materials.append(domino_mats[4])
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=2.4, location=(3.8, -4.5, 1.2))
    b2 = bpy.context.active_object
    b2.data.materials.append(domino_mats[3])

    # ==========================================
    # 4. コースビルダー関数群（再利用可能モジュール）
    # ==========================================
    def create_u_rail(name, p_start, p_end, width=0.85, wall_h=0.16, mat=mat_wood):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()
        p1, p2 = Vector(p_start), Vector(p_end)
        fwd = (p2 - p1).normalized()
        up = Vector((0, 0, 1))
        side = fwd.cross(up).normalized() * (width / 2.0)
        wall_up = Vector((0, 0, wall_h))

        v_s0 = bm.verts.new(p1 - side + wall_up)
        v_s1 = bm.verts.new(p1 - side)
        v_s2 = bm.verts.new(p1 + side)
        v_s3 = bm.verts.new(p1 + side + wall_up)

        v_e0 = bm.verts.new(p2 - side + wall_up)
        v_e1 = bm.verts.new(p2 - side)
        v_e2 = bm.verts.new(p2 + side)
        v_e3 = bm.verts.new(p2 + side + wall_up)

        bm.faces.new([v_s0, v_s1, v_e1, v_e0])
        bm.faces.new([v_s1, v_s2, v_e2, v_e1])
        bm.faces.new([v_s2, v_s3, v_e3, v_e2])

        bm.to_mesh(mesh)
        bm.free()

        mod_sol = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        mod_sol.thickness = 0.08
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Solidify")

        mod_bev = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod_bev.width = 0.025
        mod_bev.segments = 3
        bpy.ops.object.modifier_apply(modifier="Bevel")
        bpy.ops.object.shade_smooth()

        obj.data.materials.append(mat)
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = 'PASSIVE'
        obj.rigid_body.collision_shape = 'MESH'
        obj.rigid_body.friction = 0.05
        obj.rigid_body.restitution = 0.2
        return obj

    def create_spiral_track(name, center_xy, z_start, z_end, radius=1.1, turns=1.2, segments=40, width=0.8, wall_h=0.22, mat=mat_wood):
        """らせんスパイラルレールを連続U字メッシュで生成"""
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()
        cx, cy = center_xy
        total_angle = turns * 2.0 * math.pi
        
        verts_ring = []
        for i in range(segments + 1):
            t = i / segments
            angle = -math.pi * 0.5 + t * total_angle
            z = z_start + t * (z_end - z_start)
            px = cx + radius * math.cos(angle)
            py = cy + radius * math.sin(angle)
            
            # 接線ベクトルと法線ベクトル
            tangent = Vector((-math.sin(angle), math.cos(angle), (z_end - z_start) / (total_angle * radius))).normalized()
            up = Vector((0, 0, 1))
            side = tangent.cross(up).normalized() * (width / 2.0)
            wall_up = Vector((0, 0, wall_h))
            
            p = Vector((px, py, z))
            v0 = bm.verts.new(p - side + wall_up)
            v1 = bm.verts.new(p - side)
            v2 = bm.verts.new(p + side)
            v3 = bm.verts.new(p + side + wall_up)
            verts_ring.append((v0, v1, v2, v3))

        for i in range(segments):
            rA = verts_ring[i]
            rB = verts_ring[i+1]
            bm.faces.new([rA[0], rA[1], rB[1], rB[0]])
            bm.faces.new([rA[1], rA[2], rB[2], rB[1]])
            bm.faces.new([rA[2], rA[3], rB[3], rB[2]])

        bm.to_mesh(mesh)
        bm.free()

        mod_sol = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        mod_sol.thickness = 0.08
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Solidify")

        mod_bev = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod_bev.width = 0.02
        mod_bev.segments = 2
        bpy.ops.object.modifier_apply(modifier="Bevel")
        bpy.ops.object.shade_smooth()

        obj.data.materials.append(mat)
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = 'PASSIVE'
        obj.rigid_body.collision_shape = 'MESH'
        obj.rigid_body.friction = 0.04
        obj.rigid_body.restitution = 0.15
        return obj

    # ==========================================
    # 5. ギミックコースの組み立て（5段階連鎖）
    # ==========================================

    # --- ギミック1: らせんスパイラルタワー (奥 Y: -5.0, Z: 6.8 -> 5.2) ---
    create_spiral_track("Spiral_Tower", (0.0, -5.0), z_start=6.8, z_end=5.2, radius=1.1, turns=1.2, segments=45, width=0.85, mat=mat_wood)

    # スパイラル出口からシーソーへの送りレール (Z: 5.2 -> 4.8, Y: -4.0 -> -3.0)
    create_u_rail("Ramp_to_Seesaw", (0.0, -4.0, 5.2), (0.0, -2.8, 4.8), width=0.85, mat=mat_wood)

    # --- ギミック2: シーソーバランサー (ピボット: Y=-2.0, Z=4.5) ---
    # シーソー板 (初期傾斜: 奥が下がってボールを受け取り、ボールが乗ると手前が下がってドミノへ流す)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -2.0, 4.6))
    seesaw = bpy.context.active_object
    seesaw.name = "Seesaw_Plank"
    seesaw.scale = (0.75, 1.8, 0.08)
    seesaw.rotation_euler = (math.radians(-10), 0, 0) # 奥側下がりで待機
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    mod_bev = seesaw.modifiers.new(name="Bevel", type='BEVEL')
    mod_bev.width = 0.02
    mod_bev.segments = 2
    bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_smooth()
    seesaw.data.materials.append(mat_seesaw)

    bpy.ops.rigidbody.object_add()
    seesaw.rigid_body.type = 'ACTIVE'
    seesaw.rigid_body.mass = 0.6
    seesaw.rigid_body.collision_shape = 'BOX'
    seesaw.rigid_body.friction = 0.05

    # 支柱
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.9, location=(0.0, -2.0, 4.5))
    pivot = bpy.context.active_object
    pivot.name = "Seesaw_Pivot"
    pivot.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    pivot.data.materials.append(mat_pivot)
    bpy.ops.rigidbody.object_add()
    pivot.rigid_body.type = 'PASSIVE'

    # ヒンジコンストレイント
    bpy.context.view_layer.objects.active = seesaw
    bpy.ops.rigidbody.constraint_add(type='HINGE')
    seesaw.rigid_body_constraint.object1 = seesaw
    seesaw.rigid_body_constraint.object2 = pivot

    # --- ギミック3: 5連カラフルドミノ (Y: -0.8 -> 0.4, Z: 4.15) ---
    create_u_rail("Domino_Table", (0.0, -1.0, 4.15), (0.0, 0.6, 4.15), width=0.9, wall_h=0.06, mat=mat_wood)

    domino_y_positions = [-0.7, -0.4, -0.1, 0.2, 0.5]
    for idx, dy in enumerate(domino_y_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, dy, 4.45))
        d_obj = bpy.context.active_object
        d_obj.name = f"Domino_{idx+1}"
        d_obj.scale = (0.35, 0.08, 0.5)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        mod_b = d_obj.modifiers.new(name="Bevel", type='BEVEL')
        mod_b.width = 0.03
        mod_b.segments = 2
        bpy.ops.object.modifier_apply(modifier="Bevel")
        bpy.ops.object.shade_smooth()
        d_obj.data.materials.append(domino_mats[idx])
        
        bpy.ops.rigidbody.object_add()
        d_obj.rigid_body.type = 'ACTIVE'
        d_obj.rigid_body.mass = 0.25
        d_obj.rigid_body.friction = 0.3
        d_obj.rigid_body.collision_shape = 'BOX'

    # --- ギミック4: 4段マカロン木琴ステップ (Y: 0.7 -> 4.5, Z: 3.9 -> 1.2) ---
    xylophone_bars = [
        {"name": "Xylophone_C5", "start": (0.0, 0.7, 3.9),  "end": (0.0, 1.6, 3.3),  "width": 1.15, "mat": xylo_mats[0]},
        {"name": "Xylophone_E5", "start": (0.0, 1.7, 3.2),  "end": (0.0, 2.6, 2.6),  "width": 1.10, "mat": xylo_mats[1]},
        {"name": "Xylophone_G5", "start": (0.0, 2.7, 2.5),  "end": (0.0, 3.6, 1.9),  "width": 1.05, "mat": xylo_mats[2]},
        {"name": "Xylophone_C6", "start": (0.0, 3.7, 1.8),  "end": (0.0, 4.6, 1.2),  "width": 1.00, "mat": xylo_mats[3]},
    ]

    for bar_cfg in xylophone_bars:
        create_u_rail(
            bar_cfg["name"], 
            bar_cfg["start"], 
            bar_cfg["end"], 
            width=bar_cfg["width"], 
            wall_h=0.12,
            mat=bar_cfg["mat"]
        )

    # --- ギミック5: ゴールスロープ ＆ フィニッシュカップ ＆ ポップアップフラッグ ---
    create_u_rail("Finish_Ramp", (0.0, 4.7, 1.1), (0.0, 6.0, 0.4), width=0.85, mat=mat_wood)

    # フィニッシュカップ (Y=6.6)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.8, location=(0.0, 6.6, 0.4))
    cup = bpy.context.active_object
    cup.name = "Finish_Cup"
    bpy.ops.object.shade_smooth()
    mod_solid = cup.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = 0.15
    bpy.ops.object.modifier_apply(modifier="Solidify")
    cup.data.materials.append(mat_cup)
    
    bpy.ops.rigidbody.object_add()
    cup.rigid_body.type = 'PASSIVE'
    cup.rigid_body.collision_shape = 'MESH'
    cup.rigid_body.friction = 1.0
    cup.rigid_body.restitution = 0.05

    # バックストッパー
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 7.4, 0.8))
    stopper = bpy.context.active_object
    stopper.name = "Cup_Backstop"
    stopper.scale = (1.5, 0.2, 1.2)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    stopper.data.materials.append(mat_wood)
    bpy.ops.rigidbody.object_add()
    stopper.rigid_body.type = 'PASSIVE'
    stopper.rigid_body.collision_shape = 'BOX'

    # ポップアップフラッグ
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.6, location=(1.0, 6.8, 0.8))
    pole = bpy.context.active_object
    pole.name = "Flag_Pole"
    pole.data.materials.append(mat_pivot)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 6.8, 0.8))
    flag = bpy.context.active_object
    flag.name = "Goal_Flag"
    flag.scale = (0.5, 0.02, 0.3)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    flag.data.materials.append(mat_flag)

    # キャンディボール (スパイラルトップ Y=-5.0, X=0, Z=7.1 からスタート)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.28, location=(0.0, -6.1, 7.1))
    ball = bpy.context.active_object
    ball.name = "Candy_Ball"
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(mat_ball)
    
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.type = 'ACTIVE'
    ball.rigid_body.mass = 2.2
    ball.rigid_body.friction = 0.06
    ball.rigid_body.restitution = 0.25
    ball.rigid_body.collision_shape = 'SPHERE'
    ball.rigid_body.linear_damping = 0.03
    ball.rigid_body.angular_damping = 0.03

    # ==========================================
    # 6. スタジオライティング
    # ==========================================
    bpy.ops.object.light_add(type='AREA', location=(4.0, 4.0, 8.5))
    l_front = bpy.context.active_object
    l_front.data.energy = 850.0
    l_front.data.size = 6.0
    l_front.data.color = (1.0, 0.98, 0.95)
    l_front.rotation_euler = (math.radians(-35), math.radians(20), 0)

    bpy.ops.object.light_add(type='AREA', location=(-4.0, -4.5, 9.0))
    l_back = bpy.context.active_object
    l_back.data.energy = 750.0
    l_back.data.size = 6.0
    l_back.data.color = (0.95, 0.98, 1.0)

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 16))
    l_sun = bpy.context.active_object
    l_sun.data.energy = 3.5
    l_sun.data.color = (1.0, 1.0, 1.0)

    # ==========================================
    # 7. 物理シミュレーションのベイク ➔ キーフレーム確定
    # ==========================================
    print(f"⏳ Simulating & Baking Complex Physics (1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Complex Physics bake completed!")

    ball_trajectory = []
    seesaw_trajectory = []
    domino_objs = [bpy.data.objects[f"Domino_{i+1}"] for i in range(5)]
    domino_trajectories = [[] for _ in range(5)]

    for frame in range(1, total_frames + 1):
        scene.frame_set(frame)
        ball_trajectory.append((ball.matrix_world.to_translation().copy(), ball.matrix_world.to_euler().copy()))
        seesaw_trajectory.append((seesaw.matrix_world.to_translation().copy(), seesaw.matrix_world.to_euler().copy()))
        for i, d_obj in enumerate(domino_objs):
            domino_trajectories[i].append((d_obj.matrix_world.to_translation().copy(), d_obj.matrix_world.to_euler().copy()))

    all_animated = [(ball, ball_trajectory), (seesaw, seesaw_trajectory)] + list(zip(domino_objs, domino_trajectories))
    
    for obj, traj in all_animated:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_remove()
        
        for frame, (loc, rot) in enumerate(traj, start=1):
            obj.location = loc
            obj.rotation_euler = rot
            obj.keyframe_insert(data_path="location", frame=frame)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ All complex trajectories successfully baked to keyframes!")

    # ==========================================
    # 8. ゴールフラッグのポップアップ演出
    # ==========================================
    goal_frame = 130
    for frame in range(1, total_frames):
        if ball_trajectory[frame - 1][0].y > 5.8:
            goal_frame = frame
            break

    print(f"🎉 Goal reached at frame: {goal_frame}")

    flag.location.z = 0.6
    flag.scale = (0.01, 0.01, 0.01)
    flag.keyframe_insert(data_path="location", frame=1)
    flag.keyframe_insert(data_path="scale", frame=1)
    flag.keyframe_insert(data_path="location", frame=goal_frame)
    flag.keyframe_insert(data_path="scale", frame=goal_frame)

    flag.location.z = 1.7
    flag.scale = (0.55, 0.02, 0.33)
    flag.keyframe_insert(data_path="location", frame=goal_frame + 6)
    flag.keyframe_insert(data_path="scale", frame=goal_frame + 6)

    flag.location.z = 1.55
    flag.scale = (0.5, 0.02, 0.3)
    flag.keyframe_insert(data_path="location", frame=goal_frame + 12)
    flag.keyframe_insert(data_path="scale", frame=goal_frame + 12)

    # ==========================================
    # 9. 【本格正面ダイナミック追従カメラ】
    # ==========================================
    print("🎥 Configuring Front-Facing Perspective Camera for Full Course...")
    bpy.ops.object.camera_add(location=(1.6, 9.5, 4.6))
    cam = bpy.context.active_object
    cam.name = "ASMR_Camera"
    cam.data.lens = 40 # 奥行き感と臨場感を極大化
    
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = ball
    cam.data.dof.aperture_fstop = 2.8
    scene.camera = cam

    for frame in range(1, total_frames + 1):
        b_loc = ball_trajectory[frame - 1][0]
        progress = min(1.0, max(0.0, (b_loc.y + 6.0) / 12.5))
        
        # ボールが奥のスパイラルにいる時は広めに全体を捉え、手前の木琴・ゴールに近づくにつれて寄る
        cam_x = 1.4 * (1.0 - progress * 0.5)
        cam_y = 9.8 - progress * 1.2
        cam_z = 4.8 - progress * 1.2
        
        cam.location = Vector((cam_x, cam_y, cam_z))
        
        look_target = Vector((b_loc.x, b_loc.y, b_loc.z + 0.15))
        direction = look_target - cam.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam.rotation_euler = rot_quat.to_euler()
        
        cam.keyframe_insert(data_path="location", frame=frame)
        cam.keyframe_insert(data_path="rotation_euler", frame=frame)

    # レンダリング設定
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    render_out_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames")
    render_out_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(render_out_dir / "frame_")

    # .blend保存
    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_path = blend_dir / "rube_goldberg_complex_proto.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"✅ Blend file saved successfully: {blend_path}")

    # ==========================================
    # 10. フルASMRサウンドスケープ自動合成
    # ==========================================
    print("🎵 Synthesizing Full Multi-Gimmick ASMR Audio...")
    sample_rate = 44100
    total_samples = int(duration_sec * sample_rate)
    audio_data = [0.0] * total_samples

    # 1. 転がり音（スパイラル〜ゴール）
    def add_rolling_sound(start_f, end_f):
        start_s = int((start_f / fps) * sample_rate)
        end_s = min(total_samples, int((end_f / fps) * sample_rate))
        for i in range(start_s, end_s):
            t = (i - start_s) / sample_rate
            prog = (i - start_s) / max(1, end_s - start_s)
            vol = 0.05 + 0.06 * prog
            rumble = (math.sin(2 * math.pi * 170 * t) * 0.3 + 
                      math.sin(2 * math.pi * 310 * t) * 0.2 +
                      math.sin(2 * math.pi * 75 * t) * 0.5)
            audio_data[i] += rumble * vol

    add_rolling_sound(1, goal_frame)

    # 2. シーソーの「カタンッ」音
    seesaw_tilt_frame = 40
    for f in range(1, total_frames):
        if seesaw_trajectory[f-1][1].x > math.radians(5): # 前方に傾いた瞬間
            seesaw_tilt_frame = f
            break
    
    seesaw_s = int((seesaw_tilt_frame / fps) * sample_rate)
    for i in range(int(0.15 * sample_rate)):
        if seesaw_s + i >= total_samples:
            break
        t = i / sample_rate
        decay = math.exp(-35.0 * t)
        wave_val = math.sin(2 * math.pi * 350 * t) * 0.6 + math.sin(2 * math.pi * 180 * t) * 0.4
        audio_data[seesaw_s + i] += wave_val * decay * 0.5

    # 3. 5連ドミノ倒れ音
    domino_frames = []
    for dy in domino_y_positions:
        for f in range(1, total_frames):
            if ball_trajectory[f-1][0].y >= dy:
                domino_frames.append(f)
                break

    for i, df in enumerate(domino_frames):
        start_s = int((df / fps) * sample_rate)
        pitch = 1050 + i * 140
        for s in range(int(0.08 * sample_rate)):
            if start_s + s >= total_samples:
                break
            t = s / sample_rate
            decay = math.exp(-60.0 * t)
            click_wave = math.sin(2 * math.pi * pitch * t) + 0.5 * math.sin(2 * math.pi * (pitch * 1.6) * t)
            audio_data[start_s + s] += click_wave * decay * 0.35

    # 4. 4段木琴ステップ音（C5, E5, G5, C6）
    xylo_thresholds = [0.7, 1.7, 2.7, 3.7]
    frequencies = [523.25, 659.25, 783.99, 1046.50]
    
    def add_marimba_tone(start_sample, freq):
        tone_duration = 0.8
        tone_samples = int(tone_duration * sample_rate)
        for i in range(tone_samples):
            if start_sample + i >= total_samples:
                break
            t = i / sample_rate
            decay = math.exp(-6.5 * t)
            wave_val = (math.sin(2 * math.pi * freq * t) * 0.75 + 
                        math.sin(2 * math.pi * freq * 2.75 * t) * 0.18 +
                        math.sin(2 * math.pi * freq * 4.0 * t) * 0.07)
            audio_data[start_sample + i] += wave_val * decay * 0.6

    for i, ty in enumerate(xylo_thresholds):
        for f in range(1, total_frames):
            if ball_trajectory[f-1][0].y >= ty:
                s_idx = int((f / fps) * sample_rate)
                add_marimba_tone(s_idx, frequencies[i])
                break

    # 5. ゴールファンファーレ / ベル音
    goal_sample = int((goal_frame / fps) * sample_rate)
    chord_freqs = [1046.50, 1318.51, 1567.98]
    for freq in chord_freqs:
        for i in range(int(2.2 * sample_rate)):
            if goal_sample + i >= total_samples:
                break
            t = i / sample_rate
            decay = math.exp(-3.0 * t)
            wave_val = math.sin(2 * math.pi * freq * t) * 0.3
            audio_data[goal_sample + i] += wave_val * decay * 0.45

    audio_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets")
    audio_dir.mkdir(parents=True, exist_ok=True)
    wav_path = audio_dir / "complex_asmr_soundscape.wav"
    
    with wave.open(str(wav_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for sample in audio_data:
            clamped = max(-1.0, min(1.0, sample))
            packed_val = struct.pack('<h', int(clamped * 32767))
            wf.writeframes(packed_val)

    print(f"✅ Complex ASMR Audio generated at: {wav_path}")

if __name__ == "__main__":
    build_complex_toy_machine()
