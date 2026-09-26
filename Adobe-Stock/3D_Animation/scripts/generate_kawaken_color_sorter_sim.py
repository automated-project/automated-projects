import bpy
import math
import random
import bmesh

# 1. シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "ColorSorterScene"

scene.frame_start = 1
scene.frame_end = 240
scene.render.fps = 30

# レンダラー設定 (EEVEE 高画質)
scene.render.engine = 'BLENDER_EEVEE'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 2. ワールド環境（濃紺スタジオ）
world = bpy.data.worlds.new("SorterStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.04, 0.05, 0.07, 1.0)
bg.inputs['Strength'].default_value = 0.6

# 3. スタジオライティング
bpy.ops.object.light_add(type='AREA', location=(-2.8, -2.8, 5.2))
key = bpy.context.active_object
key.data.energy = 850.0
key.data.size = 3.5
key.data.color = (1.0, 0.98, 0.95)
key.rotation_euler = (math.radians(45), math.radians(-25), math.radians(-35))

bpy.ops.object.light_add(type='AREA', location=(3.2, -1.8, 3.8))
fill = bpy.context.active_object
fill.data.energy = 450.0
fill.data.size = 3.0
fill.data.color = (0.85, 0.92, 1.0)
fill.rotation_euler = (math.radians(30), math.radians(45), math.radians(60))

bpy.ops.object.light_add(type='AREA', location=(0.0, 2.8, 4.5))
rim = bpy.context.active_object
rim.data.energy = 650.0
rim.data.size = 2.5
rim.rotation_euler = (math.radians(-50), 0, 0)

bpy.ops.object.light_add(type='POINT', location=(0, 0, -1.8))
under = bpy.context.active_object
under.data.energy = 180.0
under.data.color = (0.9, 0.95, 1.0)

# 4. マテリアル
def create_candy(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.03
    bsdf.inputs['IOR'].default_value = 1.45
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
        bsdf.inputs['Coat Roughness'].default_value = 0.01
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.01
    return mat

colors = [
    (0.98, 0.15, 0.35), # ルビーレッド
    (0.12, 0.65, 0.98), # シアンブルー
    (0.98, 0.78, 0.08), # ネオンイエロー
    (0.15, 0.88, 0.45), # エメラルドグリーン
]
candy_mats = [create_candy(f"Candy_{i}", c) for i, c in enumerate(colors)]

# アクリルすり鉢
mat_acrylic = bpy.data.materials.new(name="MatAcrylic")
mat_acrylic.use_nodes = True
bsdf_a = mat_acrylic.node_tree.nodes.get("Principled BSDF")
bsdf_a.inputs['Base Color'].default_value = (0.85, 0.90, 0.98, 1.0)
bsdf_a.inputs['Roughness'].default_value = 0.08
bsdf_a.inputs['IOR'].default_value = 1.491
if 'Transmission Weight' in bsdf_a.inputs:
    bsdf_a.inputs['Transmission Weight'].default_value = 0.85
elif 'Transmission' in bsdf_a.inputs:
    bsdf_a.inputs['Transmission'].default_value = 0.85

def create_tinted_glass(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['IOR'].default_value = 1.52
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 0.92
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 0.92
    return mat

tube_mats = [create_tinted_glass(f"TubeMat_{i}", c) for i, c in enumerate(colors)]

mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.08, 0.09, 0.11, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.18

# 5. 剛体ワールド初期化
bpy.ops.rigidbody.world_add()
rbw = scene.rigidbody_world
rbw.time_scale = 1.0
rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 240

# 床
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -3.2))
floor = bpy.context.active_object
floor.data.materials.append(mat_floor)
bpy.ops.rigidbody.object_add()
floor.rigid_body.type = 'PASSIVE'

# すり鉢ファンネル
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.4, depth=1.5, location=(0, 0, 0.0))
funnel = bpy.context.active_object
mesh = funnel.data
for v in mesh.vertices:
    if v.co.z < 0:
        v.co.x *= (0.48 / 2.4)
        v.co.y *= (0.48 / 2.4)

bm = bmesh.new()
bm.from_mesh(mesh)
faces_to_remove = [f for f in bm.faces if abs(f.normal.z) > 0.9]
bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
bm.to_mesh(mesh)
bm.free()

mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_solid.thickness = 0.06
mod_sub = funnel.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub.levels = 2
bpy.ops.object.shade_smooth()
funnel.data.materials.append(mat_acrylic)

bpy.ops.rigidbody.object_add()
funnel.rigid_body.type = 'PASSIVE'
funnel.rigid_body.collision_shape = 'MESH'
funnel.rigid_body.friction = 0.02
funnel.rigid_body.restitution = 0.45

# 4方向のカラーソーター・チューブ
tube_radius = 0.22
tube_dist = 0.45
tube_angles = [0, math.pi/2, math.pi, math.pi*1.5]

for idx, ang in enumerate(tube_angles):
    tx = tube_dist * math.cos(ang)
    ty = tube_dist * math.sin(ang)
    tz = -1.8
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=tube_radius, depth=2.1, location=(tx, ty, tz))
    tube = bpy.context.active_object
    bm_t = bmesh.new()
    bm_t.from_mesh(tube.data)
    faces_t = [f for f in bm_t.faces if f.normal.z > 0.9]
    bmesh.ops.delete(bm_t, geom=faces_t, context='FACES')
    bm_t.to_mesh(tube.data)
    bm_t.free()
    
    mod_st = tube.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_st.thickness = 0.03
    mod_subt = tube.modifiers.new(name="Subsurf", type='SUBSURF')
    mod_subt.levels = 1
    bpy.ops.object.shade_smooth()
    tube.data.materials.append(tube_mats[idx])
    
    bpy.ops.rigidbody.object_add()
    tube.rigid_body.type = 'PASSIVE'
    tube.rigid_body.collision_shape = 'MESH'
    tube.rigid_body.friction = 0.05
    tube.rigid_body.restitution = 0.3

# 6. ボール生成（80個：4色 × 20個）
random.seed(999)
num_balls_per_color = 20
ball_radius = 0.11

for col_idx in range(4):
    base_ang = tube_angles[col_idx]
    for b_i in range(num_balls_per_color):
        z = 1.2 + b_i * 0.12 + random.uniform(-0.02, 0.02)
        r = 1.1 + (b_i / num_balls_per_color) * 0.9 + random.uniform(-0.06, 0.06)
        ang = base_ang + random.uniform(-0.35, 0.35)
        x = r * math.cos(ang)
        y = r * math.sin(ang)
        
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=ball_radius, location=(x, y, z))
        ball = bpy.context.active_object
        bpy.ops.object.shade_smooth()
        ball.data.materials.append(candy_mats[col_idx])
        
        bpy.ops.rigidbody.object_add()
        ball.rigid_body.type = 'ACTIVE'
        ball.rigid_body.collision_shape = 'SPHERE'
        ball.rigid_body.mass = 0.2
        ball.rigid_body.friction = 0.03
        ball.rigid_body.restitution = 0.5
        ball.rigid_body.linear_damping = 0.04
        ball.rigid_body.angular_damping = 0.04

# 7. カメラ
bpy.ops.object.camera_add(location=(0, -4.2, 3.8))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(52), 0, 0)
cam.data.lens = 55
scene.camera = cam

cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 5.2
cam.data.dof.aperture_fstop = 2.8

# 8. プロジェクト保存
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/kawaken_color_sorter.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved blend project to", blend_path)
