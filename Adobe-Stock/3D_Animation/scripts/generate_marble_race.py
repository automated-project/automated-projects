import bpy
import bmesh
import math
import os
import subprocess
from pathlib import Path

def create_marble_race():
    print("🚀 Building Epic 4-Color Marble Run Race Scene...")
    
    # 既存オブジェクトの全初期化
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    scene = bpy.context.scene
    fps = 30
    duration_sec = 18 # 18秒間
    total_frames = fps * duration_sec # 540フレーム
    
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = fps
    
    # 剛体ワールド設定 (高精度物理演算)
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.substeps_per_frame = 10
    rb_world.solver_iterations = 20
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = total_frames

    # ==========================================
    # 1. マテリアル作成
    # ==========================================
    # コース用マテリアル (高級感のあるダークスレート ＋ メタルエッジ)
    mat_track = bpy.data.materials.new(name="Mat_Track")
    bsdf = mat_track.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.08, 0.09, 0.12, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Metallic'].default_value = 0.2

    # ガイドレール/障害物用マテリアル (ゴールド)
    mat_gold = bpy.data.materials.new(name="Mat_Gold")
    bsdf = mat_gold.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.8, 0.2, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.15
        bsdf.inputs['Metallic'].default_value = 0.9

    # 4色のボール用マテリアル (高光沢・鮮やか)
    ball_colors = {
        "Red": (0.95, 0.05, 0.1, 1.0),
        "Blue": (0.05, 0.35, 1.0, 1.0),
        "Green": (0.05, 0.85, 0.15, 1.0),
        "Yellow": (1.0, 0.85, 0.0, 1.0),
    }
    ball_materials = {}
    for name, col in ball_colors.items():
        mat = bpy.data.materials.new(name=f"Mat_{name}")
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = col
            bsdf.inputs['Roughness'].default_value = 0.05
            bsdf.inputs['Metallic'].default_value = 0.85
        ball_materials[name] = mat

    # ==========================================
    # 2. コース構造の生成（ヘルパー関数）
    # ==========================================
    def add_ramp(name, loc, size, rot_deg):
        """傾斜スロープ（U字壁付きレール）を作成"""
        # 底面
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        ramp = bpy.context.active_object
        ramp.name = name
        ramp.scale = size
        ramp.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # 剛体設定 (PASSIVE / MESH)
        bpy.ops.rigidbody.object_add()
        ramp.rigid_body.type = 'PASSIVE'
        ramp.rigid_body.collision_shape = 'BOX' if rot_deg[0] == 0 and rot_deg[1] == 0 else 'CONVEX_HULL'
        ramp.rigid_body.friction = 0.02
        ramp.rigid_body.restitution = 0.2
        ramp.data.materials.append(mat_track)
        return ramp

    def add_wall(name, loc, size, rot_deg):
        """ガードレール壁を作成"""
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        wall = bpy.context.active_object
        wall.name = name
        wall.scale = size
        wall.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.rigidbody.object_add()
        wall.rigid_body.type = 'PASSIVE'
        wall.rigid_body.collision_shape = 'BOX'
        wall.rigid_body.friction = 0.02
        wall.data.materials.append(mat_gold)
        return wall

    # --- セクション1: スタート台 & 第1スロープ (Z=20 -> 15) ---
    # スタート床
    add_ramp("Start_Platform", (0, 0, 20), (2.4, 1.5, 0.1), (0, 0, 0))
    # スタート後方・左右の壁
    add_wall("Start_Wall_Back", (0, -0.75, 20.5), (2.4, 0.1, 1.0), (0, 0, 0))
    add_wall("Start_Wall_L", (-1.2, 0, 20.5), (0.1, 1.5, 1.0), (0, 0, 0))
    add_wall("Start_Wall_R", (1.2, 0, 20.5), (0.1, 1.5, 1.0), (0, 0, 0))

    # 第1スロープ (前傾斜 20度、幅2.0m、長さ10m)
    add_ramp("Ramp_1", (0, 5.0, 18.0), (2.2, 10.0, 0.1), (22, 0, 0))
    add_wall("Ramp_1_Wall_L", (-1.1, 5.0, 18.4), (0.1, 10.2, 0.8), (22, 0, 0))
    add_wall("Ramp_1_Wall_R", (1.1, 5.0, 18.4), (0.1, 10.2, 0.8), (22, 0, 0))

    # --- セクション2: 第1ターン ＆ ジグザグスロープ (Z=14 -> 9) ---
    # ターン1受け皿
    add_ramp("Turn_1_Platform", (0, 10.5, 14.2), (3.0, 2.5, 0.1), (0, 0, 0))
    add_wall("Turn_1_Wall_Front", (0, 11.7, 14.8), (3.0, 0.1, 1.2), (0, 0, 0))
    add_wall("Turn_1_Wall_R", (1.5, 10.5, 14.8), (0.1, 2.5, 1.2), (0, 0, 0))

    # 横スロープ (右から左へ下降 - 18度傾斜)
    add_ramp("Ramp_2_Side", (-4.5, 9.8, 12.2), (8.0, 1.8, 0.1), (0, 18, 0))
    add_wall("Ramp_2_Wall_Back", (-4.5, 10.7, 12.6), (8.2, 0.1, 0.8), (0, 18, 0))
    add_wall("Ramp_2_Wall_Front", (-4.5, 8.9, 12.6), (8.2, 0.1, 0.8), (0, 18, 0))

    # ターン2受け皿 (左端)
    add_ramp("Turn_2_Platform", (-9.0, 9.8, 9.8), (2.2, 2.2, 0.1), (0, 0, 0))
    add_wall("Turn_2_Wall_L", (-10.1, 9.8, 10.4), (0.1, 2.2, 1.2), (0, 0, 0))
    add_wall("Turn_2_Wall_Back", (-9.0, 10.9, 10.4), (2.2, 0.1, 1.2), (0, 0, 0))

    # --- セクション3: ピンボール・障害物ゾーン (Z=9 -> 4) ---
    # 戻りスロープ (左から中央前方向へ傾斜、ピン配列)
    add_ramp("Plinko_Board", (-4.0, 5.0, 7.0), (9.0, 8.0, 0.1), (-20, -10, 0))
    add_wall("Plinko_Wall_L", (-8.5, 5.0, 7.5), (0.1, 8.2, 1.0), (-20, -10, 0))
    add_wall("Plinko_Wall_R", (0.5, 5.0, 7.5), (0.1, 8.2, 1.0), (-20, -10, 0))

    # ピンの配列（シリンダー剛体）
    pin_rows = 4
    for r in range(pin_rows):
        y_pin = 8.0 - (r * 1.8)
        cols = 3 if r % 2 == 0 else 4
        x_offset = -4.0 + (0.6 if r % 2 == 1 else 0.0)
        for c in range(cols):
            x_pin = x_offset + (c - cols/2.0 + 0.5) * 1.6
            z_pin = 7.0 + (8.0 - y_pin) * 0.35 + (x_pin + 4.0) * 0.18
            
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(x_pin, y_pin, z_pin + 0.3))
            pin = bpy.context.active_object
            pin.name = f"Pin_{r}_{c}"
            bpy.ops.rigidbody.object_add()
            pin.rigid_body.type = 'PASSIVE'
            pin.rigid_body.collision_shape = 'CYLINDER'
            pin.rigid_body.restitution = 0.8 # 高反発
            pin.data.materials.append(mat_gold)

    # --- セクション4: ファンネル / すり鉢ボウル (Z=3 -> 1) ---
    # すり鉢受け皿
    bpy.ops.mesh.primitive_cone_add(radius1=3.2, radius2=0.6, depth=1.8, location=(-3.0, -1.0, 2.8))
    funnel = bpy.context.active_object
    funnel.name = "Funnel_Bowl"
    # 上下逆さにして穴を開ける
    funnel.rotation_euler = (math.radians(180), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # ソリッド化モディファイアで厚みをつける
    mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = 0.15
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    bpy.ops.rigidbody.object_add()
    funnel.rigid_body.type = 'PASSIVE'
    funnel.rigid_body.collision_shape = 'MESH'
    funnel.rigid_body.friction = 0.02
    funnel.rigid_body.restitution = 0.3
    funnel.data.materials.append(mat_track)

    # --- セクション5: ゴール直線レール ＆ フィニッシュライン (Z=1 -> 0) ---
    add_ramp("Finish_Ramp", (-3.0, -6.0, 0.8), (1.6, 8.0, 0.1), (15, 0, 0))
    add_wall("Finish_Wall_L", (-3.8, -6.0, 1.2), (0.1, 8.2, 0.8), (15, 0, 0))
    add_wall("Finish_Wall_R", (-2.2, -6.0, 1.2), (0.1, 8.2, 0.8), (15, 0, 0))
    add_wall("Finish_Stop_Wall", (-3.0, -10.0, 0.6), (1.8, 0.1, 1.2), (0, 0, 0))

    # ゴールゲートアーチ (Finish Gate)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.08, location=(-3.0, -8.0, 0.8))
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
        (-0.75, -0.3, 20.4), # Red
        (-0.25, -0.3, 20.4), # Blue
        (0.25, -0.3, 20.4),  # Green
        (0.75, -0.3, 20.4),  # Yellow
    ]
    
    for i, name in enumerate(ball_names):
        pos = start_positions[i]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=pos)
        ball = bpy.context.active_object
        ball.name = f"Marble_{name}"
        
        bpy.ops.rigidbody.object_add()
        ball.rigid_body.type = 'ACTIVE'
        ball.rigid_body.mass = 2.0
        ball.rigid_body.friction = 0.01
        ball.rigid_body.restitution = 0.35
        ball.rigid_body.collision_shape = 'SPHERE'
        ball.rigid_body.linear_damping = 0.02
        ball.rigid_body.angular_damping = 0.02
        
        ball.data.materials.append(ball_materials[name])
        ball_objects.append(ball)

    # ==========================================
    # 4. ライティング & 環境
    # ==========================================
    # メインサンライト
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 30))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    sun.rotation_euler = (math.radians(50), math.radians(20), math.radians(35))

    # 各セクションを照らすエリアライト
    light_positions = [
        (0, 5, 24),
        (-4.5, 9.8, 18),
        (-4.0, 5.0, 12),
        (-3.0, -4.0, 6)
    ]
    for idx, lpos in enumerate(light_positions):
        bpy.ops.object.light_add(type='POINT', location=lpos)
        pt = bpy.context.active_object
        pt.name = f"Light_{idx}"
        pt.data.energy = 800.0
        pt.data.color = (0.95, 0.98, 1.0)

    # ==========================================
    # 5. 追従カメラ (Vertical Shorts 9:16)
    # ==========================================
    bpy.ops.object.camera_add(location=(0, -6.0, 24.0))
    camera = bpy.context.active_object
    camera.name = "Follow_Camera"
    scene.camera = camera
    
    # カメラのキーフレームアニメーション (コースの進行に合わせてスムーズに降下・旋回)
    # Frame 1: スタート地点見下ろし
    camera.location = (0, -4.5, 23.5)
    camera.rotation_euler = (math.radians(60), 0, 0)
    camera.keyframe_insert(data_path="location", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=1)

    # Frame 90 (3秒): 第1スロープ〜ターン1
    camera.location = (0, 3.0, 21.0)
    camera.rotation_euler = (math.radians(65), 0, 0)
    camera.keyframe_insert(data_path="location", frame=90)
    camera.keyframe_insert(data_path="rotation_euler", frame=90)

    # Frame 180 (6秒): 横スロープ追従
    camera.location = (-4.0, 3.5, 16.5)
    camera.rotation_euler = (math.radians(60), math.radians(-10), math.radians(-15))
    camera.keyframe_insert(data_path="location", frame=180)
    camera.keyframe_insert(data_path="rotation_euler", frame=180)

    # Frame 270 (9秒): ピン障害物ゾーン
    camera.location = (-4.0, -1.0, 12.0)
    camera.rotation_euler = (math.radians(55), 0, 0)
    camera.keyframe_insert(data_path="location", frame=270)
    camera.keyframe_insert(data_path="rotation_euler", frame=270)

    # Frame 380 (12.6秒): すり鉢ファンネル
    camera.location = (-3.0, -4.5, 7.5)
    camera.rotation_euler = (math.radians(50), 0, 0)
    camera.keyframe_insert(data_path="location", frame=380)
    camera.keyframe_insert(data_path="rotation_euler", frame=380)

    # Frame 540 (18秒): ゴールゲート激突・フィニッシュ
    camera.location = (-3.0, -9.5, 4.0)
    camera.rotation_euler = (math.radians(35), 0, 0)
    camera.keyframe_insert(data_path="location", frame=540)
    camera.keyframe_insert(data_path="rotation_euler", frame=540)

    # ==========================================
    # 6. レンダリング設定 (縦型 720x1280 Shorts)
    # ==========================================
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 720
    scene.render.resolution_y = 1280
    scene.render.resolution_percentage = 100
    
    frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_race_v1")
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames_dir / "frame_")
    scene.render.image_settings.file_format = 'PNG'

    # .blend ファイルの保存
    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_file = blend_dir / "marble_run_race_v1.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend file saved successfully: {blend_file}")

    # 剛体物理シミュレーションのベイク
    print(f"⏳ Baking Rigid Body Physics (Frames 1..{total_frames})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics bake completed.")

if __name__ == "__main__":
    create_marble_race()
