import bpy
import math
import subprocess
from pathlib import Path

def setup_scene():
    print("🚀 Initializing 3D Physics Scene...")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 90  # 3秒間 (30fps)
    scene.render.fps = 30
    
    # 剛体ワールドの作成
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rb_world = scene.rigidbody_world
    rb_world.point_cache.frame_start = 1
    rb_world.point_cache.frame_end = 90

    # 1. 床 (Floor)
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    bpy.ops.rigidbody.object_add()
    floor.rigid_body.type = 'PASSIVE'
    floor.rigid_body.friction = 0.5
    floor.rigid_body.restitution = 0.2

    # 床のマテリアル (ダークマット)
    mat_floor = bpy.data.materials.new(name="Mat_Floor")
    bsdf = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.06, 0.08, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
    floor.data.materials.append(mat_floor)

    # 2. 傾斜スロープ (Slope)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-3.0, 0, 1.8))
    slope = bpy.context.active_object
    slope.name = "Slope"
    slope.scale = (3.5, 1.0, 0.1)
    slope.rotation_euler = (0, math.radians(22), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.rigidbody.object_add()
    slope.rigid_body.type = 'PASSIVE'
    slope.rigid_body.friction = 0.05
    slope.rigid_body.restitution = 0.1

    # スロープのマテリアル (シアン)
    mat_slope = bpy.data.materials.new(name="Mat_Slope")
    bsdf = mat_slope.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.0, 0.75, 0.9, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Metallic'].default_value = 0.4
    slope.data.materials.append(mat_slope)

    # 3. 転がる球体 (Marble Ball)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(-4.2, 0, 3.2))
    ball = bpy.context.active_object
    ball.name = "MarbleBall"
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.type = 'ACTIVE'
    ball.rigid_body.mass = 5.0
    ball.rigid_body.friction = 0.05
    ball.rigid_body.restitution = 0.4
    ball.rigid_body.collision_shape = 'SPHERE'

    # ボールのマテリアル (ゴールドメタル)
    mat_ball = bpy.data.materials.new(name="Mat_Ball")
    bsdf = mat_ball.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.78, 0.15, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.95
        bsdf.inputs['Roughness'].default_value = 0.1
    ball.data.materials.append(mat_ball)

    # 4. ドミノの列 (Dominoes)
    domino_colors = [
        (1.0, 0.2, 0.3, 1.0), # レッド
        (1.0, 0.55, 0.0, 1.0), # オレンジ
        (0.2, 0.85, 0.2, 1.0), # グリーン
        (0.2, 0.55, 1.0, 1.0), # ブルー
        (0.85, 0.2, 0.9, 1.0), # パープル
        (1.0, 0.9, 0.1, 1.0), # イエロー
    ]
    
    start_x = -1.0
    spacing = 0.65
    num_dominoes = 6
    
    for i in range(num_dominoes):
        x_pos = start_x + (i * spacing)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 0.55))
        domino = bpy.context.active_object
        domino.name = f"Domino_{i+1}"
        domino.scale = (0.1, 0.45, 1.1)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        bpy.ops.rigidbody.object_add()
        domino.rigid_body.type = 'ACTIVE'
        domino.rigid_body.mass = 0.4
        domino.rigid_body.friction = 0.4
        domino.rigid_body.restitution = 0.1
        domino.rigid_body.collision_shape = 'BOX'
        
        # マテリアル
        mat = bpy.data.materials.new(name=f"Mat_Domino_{i+1}")
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = domino_colors[i % len(domino_colors)]
            bsdf.inputs['Roughness'].default_value = 0.25
        domino.data.materials.append(mat)

    # 5. 照明 (Lights)
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 4.5
    sun.rotation_euler = (math.radians(45), math.radians(15), math.radians(45))

    bpy.ops.object.light_add(type='POINT', location=(-2, -3, 4))
    point = bpy.context.active_object
    point.data.energy = 600.0
    point.data.color = (0.9, 0.95, 1.0)

    # 6. カメラ (Camera)
    bpy.ops.object.camera_add(location=(0, -8.0, 4.0))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(65), 0, 0)
    scene.camera = camera

    # レンダリング設定 (PNG連番)
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    
    frames_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/frames_test")
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames_dir / "frame_")
    scene.render.image_settings.file_format = 'PNG'

    # .blend ファイルの保存
    blend_dir = Path("/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects")
    blend_dir.mkdir(parents=True, exist_ok=True)
    blend_file = blend_dir / "test_marble_domino.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    print(f"✅ Blend file saved successfully to: {blend_file}")

    # 剛体物理シミュレーションのベイク
    print("⏳ Baking Rigid Body Physics (Frames 1..90)...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("✅ Physics bake completed.")

if __name__ == "__main__":
    setup_scene()
