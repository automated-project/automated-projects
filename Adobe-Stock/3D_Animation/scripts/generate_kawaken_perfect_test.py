import bpy
import math
import random

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 1. レンダラー設定 (EEVEE 高品質・高速)
scene.render.engine = 'BLENDER_EEVEE'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 2. ワールド環境（Kawaken風のクリーンで明るいスタジオ）
world = bpy.data.worlds.new("BrightStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.92, 0.94, 0.96, 1.0)
bg.inputs['Strength'].default_value = 1.2

# 3. スタジオライティング
# メインライト（斜め上からの柔らかな大光量）
bpy.ops.object.light_add(type='AREA', location=(-2.0, -3.0, 5.0))
key = bpy.context.active_object
key.data.energy = 600.0
key.data.size = 4.0
key.data.color = (1.0, 0.98, 0.95)
key.rotation_euler = (math.radians(40), math.radians(-20), math.radians(-30))

# フィルライト
bpy.ops.object.light_add(type='AREA', location=(3.0, -2.0, 4.0))
fill = bpy.context.active_object
fill.data.energy = 300.0
fill.data.size = 3.5
fill.data.color = (0.95, 0.98, 1.0)
fill.rotation_euler = (math.radians(30), math.radians(35), math.radians(45))

# トップライト（すり鉢の上部エッジを美しく光らせる）
bpy.ops.object.light_add(type='AREA', location=(0, 0, 6.0))
top = bpy.context.active_object
top.data.energy = 400.0
top.data.size = 3.0

# 4. マテリアル
def create_candy(name, col):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.05
    bsdf.inputs['IOR'].default_value = 1.45
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
        bsdf.inputs['Coat Roughness'].default_value = 0.02
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.02
    return mat

colors = [
    (0.95, 0.20, 0.35), # ストロベリーピンク
    (0.12, 0.65, 0.95), # ソーダブルー
    (0.98, 0.78, 0.15), # レモンイエロー
    (0.20, 0.85, 0.50), # ライムグリーン
    (0.70, 0.25, 0.95), # グレープパープル
    (0.98, 0.45, 0.15), # オレンジ
]
candy_mats = [create_candy(f"Candy_{i}", c) for i, c in enumerate(colors)]

# アクリルすり鉢マテリアル（Kawaken風：白っぽく美しい半透明感）
mat_funnel = bpy.data.materials.new(name="MatFunnel")
mat_funnel.use_nodes = True
bsdf_f = mat_funnel.node_tree.nodes.get("Principled BSDF")
bsdf_f.inputs['Base Color'].default_value = (0.95, 0.96, 0.98, 1.0)
bsdf_f.inputs['Roughness'].default_value = 0.12
bsdf_f.inputs['IOR'].default_value = 1.49
if 'Transmission Weight' in bsdf_f.inputs:
    bsdf_f.inputs['Transmission Weight'].default_value = 0.75
elif 'Transmission' in bsdf_f.inputs:
    bsdf_f.inputs['Transmission'].default_value = 0.75

# クリアガラスシリンダー
mat_glass = bpy.data.materials.new(name="MatGlass")
mat_glass.use_nodes = True
bsdf_g = mat_glass.node_tree.nodes.get("Principled BSDF")
bsdf_g.inputs['Base Color'].default_value = (0.98, 0.99, 1.0, 1.0)
bsdf_g.inputs['Roughness'].default_value = 0.02
bsdf_g.inputs['IOR'].default_value = 1.52
if 'Transmission Weight' in bsdf_g.inputs:
    bsdf_g.inputs['Transmission Weight'].default_value = 0.95
elif 'Transmission' in bsdf_g.inputs:
    bsdf_g.inputs['Transmission'].default_value = 0.95

# スタジオの床
mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.85, 0.88, 0.92, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.2

# 5. メッシュ作成
# 床
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -3.0))
bpy.context.active_object.data.materials.append(mat_floor)

# 正しい向きのすり鉢（上部 radius=2.5、下部 radius=0.48、高さ=1.6）
# radius1(下)=0.48, radius2(上)=2.5
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.48, radius2=2.5, depth=1.6, location=(0, 0, 0.0))
funnel = bpy.context.active_object
mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_solid.thickness = 0.06
mod_sub = funnel.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub.levels = 2
bpy.ops.object.shade_smooth()
funnel.data.materials.append(mat_funnel)

# ガラスシリンダー（すり鉢の下に接続）
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.46, depth=2.2, location=(0, 0, -1.9))
cyl = bpy.context.active_object
mod_s_c = cyl.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_s_c.thickness = 0.04
mod_sub_c = cyl.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub_c.levels = 2
bpy.ops.object.shade_smooth()
cyl.data.materials.append(mat_glass)

# 6. ボールの配置（すり鉢の斜面を美しく渦巻いて滑り落ちる配置）
random.seed(123)
for i in range(50):
    t = i / 50.0
    r = 0.65 + t * 1.65 + random.uniform(-0.06, 0.06)
    theta = t * math.pi * 5.2 + random.uniform(-0.15, 0.15)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    # 傾斜に合わせたz座標 (下部z=-0.7, 上部z=0.7)
    z = -0.65 + (r - 0.48) * (1.6 / (2.5 - 0.48)) + 0.12
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.12, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[i % len(candy_mats)])

# シリンダー内に落ちているボール
for j in range(12):
    z = -2.8 + j * 0.22
    r = random.uniform(0.0, 0.2)
    ang = random.uniform(0, math.pi * 2)
    x = r * math.cos(ang)
    y = r * math.sin(ang)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.12, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[(j * 2 + 1) % len(candy_mats)])

# 7. カメラ（上からすり鉢の内部と渦巻きが見渡せるベストアングル）
bpy.ops.object.camera_add(location=(0, -3.8, 3.2))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(52), 0, 0)
cam.data.lens = 50
scene.camera = cam

# 被写界深度
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 4.8
cam.data.dof.aperture_fstop = 2.8

# 保存 & レンダリング
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/kawaken_perfect_test.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

out_png = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/kawaken_perfect_test_render.png"
scene.render.filepath = out_png
bpy.ops.render.render(write_still=True)
print("Finished rendering Kawaken perfect test shot!")
