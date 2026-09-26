import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "DominoSpiralScene"

scene.frame_start = 1
scene.frame_end = 180
scene.render.fps = 30

# 爆速EEVEE
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 16

scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# スタジオライティング
world = bpy.data.worlds.new("ToyStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.08, 0.10, 0.14, 1.0)
bg.inputs['Strength'].default_value = 0.8

bpy.ops.object.light_add(type='SUN', location=(4, -4, 8))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.data.color = (1.0, 0.98, 0.92)
sun.rotation_euler = (math.radians(55), math.radians(20), math.radians(-35))

# マテリアル
def create_toy_mat(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.12
    return mat

colors = [
    (1.0, 0.18, 0.32), # ネオンレッド
    (0.12, 0.68, 1.0),  # ネオンブルー
    (1.0, 0.82, 0.08), # ネオンイエロー
    (0.18, 0.90, 0.42), # ネオングリーン
    (0.85, 0.20, 0.98), # ネオンパープル
    (1.0, 0.48, 0.12), # ネオンオレンジ
]
domino_mats = [create_toy_mat(f"Dom_{i}", c) for i, c in enumerate(colors)]

mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.05, 0.06, 0.08, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.3

# 床
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.5))
floor = bpy.context.active_object
floor.scale = (30, 30, 1.0)
bpy.ops.object.transform_apply(scale=True)
floor.data.materials.append(mat_floor)

# 80枚の幾何学ドミノ（美しい数学的連鎖倒壊アニメーション）
num_dominoes = 80
dom_w = 0.12
dom_d = 0.45
dom_h = 0.90

for i in range(num_dominoes):
    t = i / float(num_dominoes)
    r = 0.8 + t * 2.8
    theta = t * math.pi * 5.2
    
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    z = dom_h / 2.0
    
    tangent_angle = theta + math.pi / 2.0
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
    dom = bpy.context.active_object
    dom.scale = (dom_w, dom_d, dom_h)
    bpy.ops.object.transform_apply(scale=True)
    
    # 起点（Z回転）
    dom.rotation_euler = (0, 0, tangent_angle)
    dom.data.materials.append(domino_mats[i % len(domino_mats)])
    
    # 倒れるタイミング（フレーム 10 + i * 1.8）
    start_f = 10 + int(i * 1.8)
    end_f = start_f + 8
    
    # 倒れる方向（進行方向へピタッと倒れるアニメーションキーフレーム）
    dom.keyframe_insert(data_path="rotation_euler", frame=1)
    dom.keyframe_insert(data_path="rotation_euler", frame=start_f)
    
    # 倒れた後の角度 (前方に70度傾く)
    fall_pitch = math.radians(70)
    # ローカルX軸またはY軸周りに倒す
    dom.rotation_euler = (math.sin(tangent_angle) * fall_pitch, -math.cos(tangent_angle) * fall_pitch, tangent_angle)
    dom.keyframe_insert(data_path="rotation_euler", frame=end_f)

# カメラ（螺旋の中心から全体を見渡す完璧な構図）
bpy.ops.object.camera_add(location=(0, -5.5, 6.2), rotation=(math.radians(48), 0, 0))
cam = bpy.context.active_object
cam.data.lens = 38
scene.camera = cam

blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/domino_spiral.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved procedural domino blend to", blend_path)
