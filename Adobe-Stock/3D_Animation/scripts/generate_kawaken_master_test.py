import bpy
import math
import random

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 1. レンダラー
scene.render.engine = 'BLENDER_EEVEE'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 2. ワールド環境（濃いグラデーションでボールとガラスを際立たせる）
world = bpy.data.worlds.new("StudioWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.05, 0.06, 0.08, 1.0)
bg.inputs['Strength'].default_value = 0.5

# 3. スタジオライティング（Kawaken風の鮮烈なハイライトと陰影）
# キーライト（左上からの超ソフト大光量）
bpy.ops.object.light_add(type='AREA', location=(-3.0, -3.0, 5.0))
key = bpy.context.active_object
key.data.energy = 800.0
key.data.size = 3.5
key.data.color = (1.0, 0.98, 0.95)
key.rotation_euler = (math.radians(45), math.radians(-25), math.radians(-35))

# フィルライト（右サイドからのクールな青白い光）
bpy.ops.object.light_add(type='AREA', location=(3.5, -1.5, 3.5))
fill = bpy.context.active_object
fill.data.energy = 400.0
fill.data.size = 3.0
fill.data.color = (0.85, 0.92, 1.0)
fill.rotation_euler = (math.radians(30), math.radians(45), math.radians(60))

# リムライト（真後ろ上空からエッジを白く輝かせる）
bpy.ops.object.light_add(type='AREA', location=(0.0, 3.0, 4.0))
rim = bpy.context.active_object
rim.data.energy = 600.0
rim.data.size = 2.5
rim.rotation_euler = (math.radians(-50), 0, 0)

# アンダーライト（すり鉢とシリンダーを底から光らせる）
bpy.ops.object.light_add(type='POINT', location=(0, 0, -1.5))
under = bpy.context.active_object
under.data.energy = 150.0
under.data.color = (0.9, 0.95, 1.0)

# 4. マテリアル
def create_candy(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.03 # 超ツヤツヤ
    bsdf.inputs['IOR'].default_value = 1.45
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
        bsdf.inputs['Coat Roughness'].default_value = 0.01
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.01
    return mat

# ビビッドで美味しそうなKawakenカラー
colors = [
    (0.98, 0.12, 0.35), # ルビーレッド
    (0.10, 0.65, 0.98), # シアンブルー
    (0.98, 0.78, 0.05), # ネオンイエロー
    (0.15, 0.88, 0.45), # ミントライム
    (0.75, 0.18, 0.95), # ネオンパープル
    (0.98, 0.45, 0.10), # マンダリンオレンジ
]
candy_mats = [create_candy(f"Candy_{i}", c) for i, c in enumerate(colors)]

# アクリルすり鉢（Kawakenのトレードマーク：美しい半透明スモークアクリル）
mat_funnel = bpy.data.materials.new(name="MatFunnel")
mat_funnel.use_nodes = True
bsdf_f = mat_funnel.node_tree.nodes.get("Principled BSDF")
bsdf_f.inputs['Base Color'].default_value = (0.85, 0.90, 0.98, 1.0)
bsdf_f.inputs['Roughness'].default_value = 0.08
bsdf_f.inputs['IOR'].default_value = 1.491
if 'Transmission Weight' in bsdf_f.inputs:
    bsdf_f.inputs['Transmission Weight'].default_value = 0.85
elif 'Transmission' in bsdf_f.inputs:
    bsdf_f.inputs['Transmission'].default_value = 0.85

# スタジオ床（反射が美しいダークグレーフロア）
mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.08, 0.09, 0.11, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.18

# 5. メッシュ作成
# 床
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -3.2))
bpy.context.active_object.data.materials.append(mat_floor)

# 開口したすり鉢（Coneではなく、上面と下面が開いた円錐台メッシュ）
# 円柱からテーパーをかけて上を開口
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.4, depth=1.5, location=(0, 0, 0.0))
funnel = bpy.context.active_object
# 頂点を変形してすり鉢（上が広く、下が狭い）
bpy.ops.object.mode_set(mode='OBJECT')
mesh = funnel.data
for v in mesh.vertices:
    if v.co.z < 0:
        v.co.x *= (0.48 / 2.4)
        v.co.y *= (0.48 / 2.4)
    else:
        # 上面のフタを削除（開口）
        pass

# 上下のフタの面を削除して開口パイプにする
import bmesh
bm = bmesh.new()
bm.from_mesh(mesh)
# zが極端な面（上下キャップ）を削除
faces_to_remove = [f for f in bm.faces if abs(f.normal.z) > 0.9]
bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
bm.to_mesh(mesh)
bm.free()

mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_solid.thickness = 0.06
mod_sub = funnel.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub.levels = 2
bpy.ops.object.shade_smooth()
funnel.data.materials.append(mat_funnel)

# ガラスシリンダー
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.46, depth=2.0, location=(0, 0, -1.75))
cyl = bpy.context.active_object
bm_c = bmesh.new()
bm_c.from_mesh(cyl.data)
faces_c = [f for f in bm_c.faces if f.normal.z > 0.9] # 上面のみ削除
bmesh.ops.delete(bm_c, geom=faces_c, context='FACES')
bm_c.to_mesh(cyl.data)
bm_c.free()

mod_s_c = cyl.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_s_c.thickness = 0.04
mod_sub_c = cyl.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub_c.levels = 2
bpy.ops.object.shade_smooth()
cyl.data.materials.append(mat_funnel)

# 6. ボール配置（すり鉢の内壁に沿って美しく渦巻く40個のキャンディボール）
random.seed(42)
for i in range(40):
    t = i / 40.0
    r = 0.58 + t * 1.65
    theta = t * math.pi * 5.8 + random.uniform(-0.1, 0.1)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    z = -0.65 + (r - 0.48) * (1.5 / (2.4 - 0.48)) + 0.12
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.12, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[i % len(candy_mats)])

# シリンダー内に溜まったボール
for j in range(12):
    z = -2.5 + j * 0.22
    r = random.uniform(0.0, 0.18)
    ang = random.uniform(0, math.pi * 2)
    x = r * math.cos(ang)
    y = r * math.sin(ang)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.12, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[(j * 2 + 1) % len(candy_mats)])

# 7. カメラ（すり鉢の中を見下ろす美しいアングル）
bpy.ops.object.camera_add(location=(0, -4.2, 3.8))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(52), 0, 0)
cam.data.lens = 55
scene.camera = cam

# 被写界深度
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 5.2
cam.data.dof.aperture_fstop = 2.4

# 保存 & レンダリング
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/kawaken_master_test.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

out_png = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/kawaken_master_test_render.png"
scene.render.filepath = out_png
bpy.ops.render.render(write_still=True)
print("Finished rendering Kawaken Master Test!")
