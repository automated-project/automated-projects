import bpy
import math
import random

# 1. シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "SmashTowerScene"

scene.frame_start = 1
scene.frame_end = 180
scene.render.fps = 30

# 2. 超高速EEVEE (1フレーム約1秒)
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 16

scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 3. スタジオライティング
world = bpy.data.worlds.new("ToyStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.10, 0.12, 0.16, 1.0)
bg.inputs['Strength'].default_value = 0.8

# サンライト
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.data.color = (1.0, 0.98, 0.92)
sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-30))

# 4. マテリアル
def create_toy_mat(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.15
    return mat

colors = [
    (1.0, 0.20, 0.30), # ビビッドレッド
    (0.10, 0.70, 1.0),  # ネオンシアン
    (1.0, 0.85, 0.10), # レモンイエロー
    (0.20, 0.90, 0.40), # ライムグリーン
    (0.80, 0.20, 1.0),  # マゼンタパープル
    (1.0, 0.50, 0.10), # オレンジ
]
toy_mats = [create_toy_mat(f"Toy_{i}", c) for i, c in enumerate(colors)]

mat_wrecking = bpy.data.materials.new(name="MatWrecking")
mat_wrecking.use_nodes = True
bsdf_w = mat_wrecking.node_tree.nodes.get("Principled BSDF")
bsdf_w.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
bsdf_w.inputs['Metallic'].default_value = 0.95
bsdf_w.inputs['Roughness'].default_value = 0.08

mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.07, 0.08, 0.10, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.25

# 5. 剛体ワールド初期化
bpy.ops.rigidbody.world_add()
rbw = scene.rigidbody_world
rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 180

# 床（PASSIVE BOX。上面がぴったり z=0.0）
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.5))
floor = bpy.context.active_object
floor.scale = (30, 30, 1.0)
bpy.ops.object.transform_apply(scale=True)
floor.data.materials.append(mat_floor)
bpy.ops.rigidbody.object_add()
floor.rigid_body.type = 'PASSIVE'
floor.rigid_body.collision_shape = 'BOX'
floor.rigid_body.friction = 0.6
floor.rigid_body.restitution = 0.3

# 6. カラフルなタワーブロック
block_w = 1.2
block_d = 0.38
block_h = 0.24
num_layers = 14
blocks = []

for layer in range(num_layers):
    # 各ブロックの間に微小な隙間 (0.005) を設けて初期重なりを完全排除
    z = (block_h / 2.0) + (layer * (block_h + 0.005))
    is_even = (layer % 2 == 0)
    mat = toy_mats[layer % len(toy_mats)]
    
    for i in range(3):
        offset = (i - 1) * (block_d + 0.02)
        if is_even:
            bx = 0
            by = offset
            rot_z = 0
            sx, sy, sz = block_w, block_d, block_h
        else:
            bx = offset
            by = 0
            rot_z = math.pi / 2.0
            sx, sy, sz = block_d, block_w, block_h
            
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, z))
        b_obj = bpy.context.active_object
        b_obj.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        b_obj.rotation_euler = (0, 0, rot_z)
        bpy.ops.object.transform_apply(rotation=True)
        
        mod_bev = b_obj.modifiers.new(name="Bevel", type='BEVEL')
        mod_bev.width = 0.02
        mod_bev.segments = 2
        bpy.ops.object.shade_smooth()
        b_obj.data.materials.append(mat)
        
        bpy.ops.rigidbody.object_add()
        b_obj.rigid_body.type = 'ACTIVE'
        b_obj.rigid_body.collision_shape = 'BOX'
        b_obj.rigid_body.mass = 0.4
        b_obj.rigid_body.friction = 0.7
        b_obj.rigid_body.restitution = 0.15
        # 線形・回転ダンピングで初期姿勢を安定化
        b_obj.rigid_body.linear_damping = 0.1
        b_obj.rigid_body.angular_damping = 0.1
        blocks.append(b_obj)

# 7. 巨大鉄球
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.6, location=(0, -4.5, 3.5))
wrecking_ball = bpy.context.active_object
bpy.ops.object.shade_smooth()
wrecking_ball.data.materials.append(mat_wrecking)

bpy.ops.rigidbody.object_add()
wrecking_ball.rigid_body.type = 'ACTIVE'
wrecking_ball.rigid_body.collision_shape = 'SPHERE'
wrecking_ball.rigid_body.mass = 35.0
wrecking_ball.rigid_body.friction = 0.2
wrecking_ball.rigid_body.restitution = 0.5

# 鉄球アニメーション（フレーム1〜18で突撃し、18で物理解放）
wrecking_ball.rigid_body.kinematic = True
wrecking_ball.location = (0, -4.5, 3.5)
wrecking_ball.keyframe_insert(data_path="location", frame=1)
wrecking_ball.location = (0, -1.2, 1.8) # タワー中腹に激突
wrecking_ball.keyframe_insert(data_path="location", frame=18)

wrecking_ball.keyframe_insert(data_path="rigid_body.kinematic", frame=17)
wrecking_ball.rigid_body.kinematic = False
wrecking_ball.keyframe_insert(data_path="rigid_body.kinematic", frame=18)

# 8. カメラ
bpy.ops.object.camera_add(location=(0, -6.8, 2.6), rotation=(math.radians(76), 0, 0))
cam = bpy.context.active_object
cam.data.lens = 45
scene.camera = cam

# 9. キーフレームベイク
print("Simulating smash tower step-by-step...")
sim_objects = blocks + [wrecking_ball]
for f in range(1, 181):
    scene.frame_set(f)
    for obj in sim_objects:
        obj.location = obj.matrix_world.translation
        obj.rotation_euler = obj.matrix_world.to_euler()
        obj.keyframe_insert(data_path="location", frame=f)
        obj.keyframe_insert(data_path="rotation_euler", frame=f)

for obj in sim_objects:
    obj.rigid_body.type = 'PASSIVE'
    obj.rigid_body.kinematic = True

blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/smash_tower.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved blend project to", blend_path)
