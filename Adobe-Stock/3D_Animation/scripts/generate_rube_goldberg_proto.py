"""
ピタゴラスイッチ / ASMR おもちゃワールド（トイ・キャンディ風）
【完全版・正面ダイナミック構図】：
・ゴール側から奥を見渡す迫力のアングル
・奥の暗闇を解消する美しいパステルスタジオ壁＆全方位ライティング
・ドミノと木琴ステップを手前に向かって滑らかに下りてくるダイナミックカメラ
・ゴールカップへ吸い込まれフラッグがポンッと立ち上がるフィニッシュ
"""

import bpy
import bmesh
import math
from mathutils import Vector, Euler
from pathlib import Path
import wave
import struct

def create_toy_asmr_machine():
    fps = 30
    duration_sec = 8
    total_frames = fps * duration_sec

    # 1. シーン初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = total_frames
    
    # 物理ワールド設定
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames
    rb_world.substeps_per_frame = 50
    rb_world.solver_iterations = 50

    print("🎨 Building Perfect Front-Facing Toy World ASMR Machine...")

    # ==========================================
    # 2. マテリアル定義 (明るく温かいスタジオトイ)
    # ==========================================
    def make_material(name, color, metallic=0.0, roughness=0.25):
        mat = bpy.data.materials.new(name=name)
        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        if principled:
            principled.inputs['Base Color'].default_value = color
            principled.inputs['Metallic'].default_value = metallic
            principled.inputs['Roughness'].default_value = roughness
        return mat

    # 空間マテリアル (明るいミントホワイトのスタジオ)
    mat_floor = make_material("Playroom_Floor", (0.94, 0.95, 0.97, 1.0), roughness=0.2)
    mat_backwall = make_material("Studio_Backwall", (0.88, 0.92, 0.96, 1.0), roughness=0.35)
    mat_wood_rail = make_material("Toy_Birch_Wood", (0.94, 0.86, 0.72, 1.0), roughness=0.35)
    
    # ボール（光沢のある鮮やかなキャンディコーラル）
    mat_ball = make_material("Candy_Ball", (1.0, 0.22, 0.40, 1.0), metallic=0.05, roughness=0.08)

    # ドミノマテリアル (カラフル4色)
    mat_domino_1 = make_material("Domino_Orange", (1.0, 0.55, 0.15, 1.0), roughness=0.2)
    mat_domino_2 = make_material("Domino_Yellow", (1.0, 0.85, 0.20, 1.0), roughness=0.2)
    mat_domino_3 = make_material("Domino_Lime", (0.50, 0.88, 0.25, 1.0), roughness=0.2)
    mat_domino_4 = make_material("Domino_Cyan", (0.20, 0.80, 0.95, 1.0), roughness=0.2)
    domino_mats = [mat_domino_1, mat_domino_2, mat_domino_3, mat_domino_4]

    # 木琴マテリアル (マカロンパステル)
    mat_xylo_1 = make_material("Pastel_Coral", (1.0, 0.45, 0.48, 1.0), roughness=0.2)
    mat_xylo_2 = make_material("Pastel_Yellow", (1.0, 0.82, 0.32, 1.0), roughness=0.2)
    mat_xylo_3 = make_material("Pastel_Mint", (0.35, 0.90, 0.68, 1.0), roughness=0.2)
    mat_xylo_4 = make_material("Pastel_SkyBlue", (0.35, 0.72, 1.0, 1.0), roughness=0.2)
    
    # ゴール・フラッグ
    mat_cup = make_material("Lavender_Cup", (0.75, 0.48, 0.95, 1.0), roughness=0.15)
    mat_flag_pole = make_material("Gold_Pole", (0.95, 0.78, 0.35, 1.0), metallic=0.85, roughness=0.2)
    mat_flag = make_material("Flag_Red", (1.0, 0.18, 0.25, 1.0), roughness=0.3)

    # 背景用デコレーション
    mat_deco_1 = make_material("Deco_Purple", (0.65, 0.45, 0.85, 1.0), roughness=0.3)
    mat_deco_2 = make_material("Deco_Teal", (0.25, 0.75, 0.75, 1.0), roughness=0.3)

    # ==========================================
    # 3. スタジオ環境（フロア ＋ 背景カーブウォール）
    # ==========================================
    # 床
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Playroom_Floor"
    floor.data.materials.append(mat_floor)
    bpy.ops.rigidbody.object_add()
    floor.rigid_body.type = 'PASSIVE'
    floor.rigid_body.collision_shape = 'BOX'
    floor.rigid_body.friction = 0.5
    floor.rigid_body.restitution = 0.2

    # 奥の背景壁（暗闇を解消する明るいスタジオバックドロップ）
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, -8.0, 8.0))
    backwall = bpy.context.active_object
    backwall.name = "Studio_Backwall"
    backwall.rotation_euler = (math.radians(90), 0, 0)
    backwall.data.materials.append(mat_backwall)

    # 背景の可愛いおもちゃブロック（ボケ感用）
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-3.2, -4.5, 0.75))
    b1 = bpy.context.active_object
    b1.rotation_euler = (0, 0, math.radians(25))
    b1.data.materials.append(mat_deco_1)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=2.0, location=(3.2, -3.5, 1.0))
    b2 = bpy.context.active_object
    b2.data.materials.append(mat_deco_2)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(-2.6, -1.5, 0.7))
    b3 = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    b3.data.materials.append(mat_domino_1)

    # ==========================================
    # 4. コース構築（ベベル付きU字レール ＆ ドミノ ＆ 木琴）
    # ==========================================

    def create_u_rail(name, p_start, p_end, width=0.85, wall_h=0.16, mat=mat_wood_rail):
        """ベベル（角丸）付きのU字レール"""
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()
        p1 = Vector(p_start)
        p2 = Vector(p_end)
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
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = 'PASSIVE'
        obj.rigid_body.collision_shape = 'MESH'
        obj.rigid_body.friction = 0.05
        obj.rigid_body.restitution = 0.2
        return obj

    # 1. スタートスロープ (奥 Y: -4.8 -> -3.2, Z: 5.2 -> 4.5)
    create_u_rail("Start_Ramp", (0, -4.8, 5.2), (0, -3.2, 4.5), width=0.85, mat=mat_wood_rail)

    # 2. ドミノステージ (奥 Y: -3.2 -> -1.6, Z: 4.45)
    create_u_rail("Domino_Table", (0, -3.2, 4.45), (0, -1.6, 4.45), width=0.9, wall_h=0.06, mat=mat_wood_rail)

    # 4連カラフルドミノ (奥から手前へ)
    domino_y_positions = [-2.9, -2.5, -2.1, -1.7]
    for idx, dy in enumerate(domino_y_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, dy, 4.75))
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
        d_obj.rigid_body.mass = 0.3
        d_obj.rigid_body.friction = 0.3
        d_obj.rigid_body.collision_shape = 'BOX'

    # 3. 4段マカロン木琴ステップ (手前に向かって下る Y: -1.5 -> 3.3, Z: 4.2 -> 1.1)
    xylophone_bars = [
        {"name": "Xylophone_C5", "start": (0, -1.5, 4.2), "end": (0, -0.3, 3.5), "width": 1.15, "mat": mat_xylo_1},
        {"name": "Xylophone_E5", "start": (0, -0.2, 3.4), "end": (0, 0.9, 2.7),  "width": 1.10, "mat": mat_xylo_2},
        {"name": "Xylophone_G5", "start": (0, 1.0, 2.6),  "end": (0, 2.1, 1.9),  "width": 1.05, "mat": mat_xylo_3},
        {"name": "Xylophone_C6", "start": (0, 2.2, 1.8),  "end": (0, 3.3, 1.1),  "width": 1.00, "mat": mat_xylo_4},
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

    # 4. ゴール前スロープ (手前 Y: 3.4 -> 5.0, Z: 1.0 -> 0.4)
    create_u_rail("Finish_Ramp", (0, 3.4, 1.0), (0, 5.0, 0.4), width=0.85, mat=mat_wood_rail)

    # 5. フィニッシュカップ & バックストッパー (手前 Y: 5.6)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.8, location=(0, 5.6, 0.4))
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
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 6.4, 0.8))
    stopper = bpy.context.active_object
    stopper.name = "Cup_Backstop"
    stopper.scale = (1.5, 0.2, 1.2)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    stopper.data.materials.append(mat_wood_rail)
    bpy.ops.rigidbody.object_add()
    stopper.rigid_body.type = 'PASSIVE'
    stopper.rigid_body.collision_shape = 'BOX'

    # 6. ポップアップ・ゴールフラッグ（ボールを遮らないよう右側に配置）
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.6, location=(1.0, 5.8, 0.8))
    pole = bpy.context.active_object
    pole.name = "Flag_Pole"
    pole.data.materials.append(mat_flag_pole)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 5.8, 0.8))
    flag = bpy.context.active_object
    flag.name = "Goal_Flag"
    flag.scale = (0.5, 0.02, 0.3)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    flag.data.materials.append(mat_flag)

    # 7. キャンディボール
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.28, location=(0, -4.5, 5.5))
    ball = bpy.context.active_object
    ball.name = "Candy_Ball"
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(mat_ball)
    
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.type = 'ACTIVE'
    ball.rigid_body.mass = 2.0
    ball.rigid_body.friction = 0.08
    ball.rigid_body.restitution = 0.3
    ball.rigid_body.collision_shape = 'SPHERE'
    ball.rigid_body.linear_damping = 0.04
    ball.rigid_body.angular_damping = 0.04

    # ==========================================
    # 5. スタジオライティング (奥・手前・全体の均一照明)
    # ==========================================
    bpy.ops.object.light_add(type='AREA', location=(3.5, 3.0, 7.5))
    light_front = bpy.context.active_object
    light_front.data.energy = 750.0
    light_front.data.size = 5.0
    light_front.data.color = (1.0, 0.98, 0.95)
    light_front.rotation_euler = (math.radians(-35), math.radians(20), 0)

    bpy.ops.object.light_add(type='AREA', location=(-3.5, -4.0, 8.0))
    light_back = bpy.context.active_object
    light_back.data.energy = 700.0
    light_back.data.size = 6.0
    light_back.data.color = (0.95, 0.98, 1.0)

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 15))
    light_sun = bpy.context.active_object
    light_sun.data.energy = 3.5
    light_sun.data.color = (1.0, 1.0, 1.0)

    # ==========================================
    # 6. 物理ベイク ➔ キーフレーム確定
    # ==========================================
    print(f"⏳ Simulating & Baking Physics (1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics bake completed!")

    ball_trajectory = []
    domino_objs = [bpy.data.objects[f"Domino_{i+1}"] for i in range(4)]
    domino_trajectories = [[] for _ in range(4)]

    for frame in range(1, total_frames + 1):
        scene.frame_set(frame)
        b_mat = ball.matrix_world.copy()
        ball_trajectory.append((b_mat.to_translation(), b_mat.to_euler()))
        
        for i, d_obj in enumerate(domino_objs):
            d_mat = d_obj.matrix_world.copy()
            domino_trajectories[i].append((d_mat.to_translation(), d_mat.to_euler()))

    for obj, traj in [(ball, ball_trajectory)] + list(zip(domino_objs, domino_trajectories)):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_remove()
        
        for frame, (loc, rot) in enumerate(traj, start=1):
            obj.location = loc
            obj.rotation_euler = rot
            obj.keyframe_insert(data_path="location", frame=frame)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("✅ Physics trajectories successfully baked to keyframes!")

    # ==========================================
    # 7. ゴールフラッグのポップアップ演出
    # ==========================================
    goal_frame = 80
    for frame in range(1, total_frames):
        if ball_trajectory[frame - 1][0].y > 4.6:
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
    # 8. 【最適化された正面パースペクティブカメラ】
    # ==========================================
    print("🎥 Configuring Front-Facing Perspective Camera with Perfect Framing...")
    bpy.ops.object.camera_add(location=(1.5, 8.5, 4.2))
    cam = bpy.context.active_object
    cam.name = "ASMR_Camera"
    cam.data.lens = 42 # 画角を少し広げて全体と迫力を両立
    
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = ball
    cam.data.dof.aperture_fstop = 2.8
    
    scene.camera = cam

    for frame in range(1, total_frames + 1):
        b_loc = ball_trajectory[frame - 1][0]
        
        # ボール進行度 (0.0=スタート奥, 1.0=ゴール手前)
        progress = min(1.0, max(0.0, (b_loc.y + 4.5) / 9.5))
        
        # ボールが迫ってくるのに合わせて適度に引き、ゴールイン時も完璧に収まるカメラワーク
        cam_x = 1.2 * (1.0 - progress * 0.4) # 適度なサイド角で立体感
        cam_y = 8.6 - progress * 0.8         # 手前に寄りすぎず全体を美しく収める
        cam_z = 4.2 - progress * 1.0         # 適度な目線高さを維持
        
        cam.location = Vector((cam_x, cam_y, cam_z))
        
        # ボールを中央やや下に捉え続ける
        look_target = Vector((b_loc.x, b_loc.y, b_loc.z + 0.1))
        direction = look_target - cam.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam.rotation_euler = rot_quat.to_euler()
        
        cam.keyframe_insert(data_path="location", frame=frame)
        cam.keyframe_insert(data_path="rotation_euler", frame=frame)

    # レンダリング設定 (1080x1920 9:16 Shorts)
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    render_out_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames")
    render_out_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(render_out_dir / "frame_")

    # .blendファイルの保存
    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_path = blend_dir / "rube_goldberg_asmr_proto.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"✅ Blend file saved successfully: {blend_path}")

    # ==========================================
    # 9. フルサウンドデザイン（転がり音＋ドミノ＋木琴＋ゴールファンファーレ）
    # ==========================================
    print("🎵 Synthesizing Full ASMR Soundscape...")
    
    sample_rate = 44100
    total_samples = int(duration_sec * sample_rate)
    audio_data = [0.0] * total_samples

    def add_rolling_sound(start_f, end_f):
        start_s = int((start_f / fps) * sample_rate)
        end_s = min(total_samples, int((end_f / fps) * sample_rate))
        for i in range(start_s, end_s):
            t = (i - start_s) / sample_rate
            prog = (i - start_s) / max(1, end_s - start_s)
            vol = 0.06 + 0.05 * prog
            rumble = (math.sin(2 * math.pi * 180 * t) * 0.3 + 
                      math.sin(2 * math.pi * 320 * t) * 0.2 +
                      math.sin(2 * math.pi * 80 * t) * 0.5)
            audio_data[i] += rumble * vol

    add_rolling_sound(1, goal_frame)

    def add_domino_click(frame_idx, pitch=1200):
        start_s = int((frame_idx / fps) * sample_rate)
        click_samples = int(0.08 * sample_rate)
        for i in range(click_samples):
            if start_s + i >= total_samples:
                break
            t = i / sample_rate
            decay = math.exp(-60.0 * t)
            click_wave = math.sin(2 * math.pi * pitch * t) + 0.5 * math.sin(2 * math.pi * (pitch * 1.6) * t)
            audio_data[start_s + i] += click_wave * decay * 0.35

    domino_frames = []
    for dy in [-2.9, -2.5, -2.1, -1.7]:
        for f in range(1, total_frames):
            if ball_trajectory[f-1][0].y >= dy:
                domino_frames.append(f)
                break
    for i, df in enumerate(domino_frames):
        add_domino_click(df, pitch=1100 + i * 150)

    xylo_thresholds = [-1.5, -0.2, 1.0, 2.2]
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

    goal_sample = int((goal_frame / fps) * sample_rate)
    def add_bell_chord(start_s):
        chord_freqs = [1046.50, 1318.51, 1567.98]
        for freq in chord_freqs:
            for i in range(int(2.0 * sample_rate)):
                if start_s + i >= total_samples:
                    break
                t = i / sample_rate
                decay = math.exp(-3.0 * t)
                wave_val = math.sin(2 * math.pi * freq * t) * 0.3
                audio_data[start_s + i] += wave_val * decay * 0.45

    add_bell_chord(goal_sample)

    audio_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets")
    audio_dir.mkdir(parents=True, exist_ok=True)
    wav_path = audio_dir / "xylophone_asmr_proto.wav"
    
    with wave.open(str(wav_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for sample in audio_data:
            clamped = max(-1.0, min(1.0, sample))
            packed_val = struct.pack('<h', int(clamped * 32767))
            wf.writeframes(packed_val)

    print(f"✅ Full ASMR Audio generated at: {wav_path}")

if __name__ == "__main__":
    create_toy_asmr_machine()
