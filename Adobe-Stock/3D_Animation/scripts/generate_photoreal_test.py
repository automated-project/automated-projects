import bpy
import math
import os

# 1. 既存シーンの初期化
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "PhotorealScene"

# 2. Cycles + Metal GPU レンダリング設定
scene.render.engine = 'CYCLES'
cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
cycles_prefs.compute_device_type = 'METAL'
cycles_prefs.get_devices()
for d in cycles_prefs.devices:
    if 'GPU' in d.name or 'METAL' in d.type:
        d.use = True
    else:
        d.use = False

scene.cycles.device = 'GPU'
scene.cycles.samples = 64
scene.cycles.preview_samples = 32
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 8

# カラーマネジメント（映画・CMクオリティのAgX/Filmicトーンマッピング）
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - High Contrast'

# 解像度設定 (1080x1920 縦型)
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

# 3. スタジオ環境ライティング（プロ仕様の多重ソフトボックス）
# ワールド背景（完全な暗黒ではなく、微弱なスタジオアンビエント）
world = bpy.data.worlds.new("StudioWorld")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
bg_node.inputs['Color'].default_value = (0.04, 0.04, 0.05, 1.0)
bg_node.inputs['Strength'].default_value = 0.8

# キーライト（巨大ソフトボックス：美しいグラデーションハイライトを生む）
bpy.ops.object.light_add(type='AREA', location=(-2.5, -2.5, 4.0))
key_light = bpy.context.active_object
key_light.data.energy = 450.0
key_light.data.size = 2.5
key_light.data.size_y = 3.5
key_light.data.color = (1.0, 0.98, 0.95)
key_light.rotation_euler = (math.radians(35), math.radians(-25), math.radians(-45))

# フィルライト（青みがかった柔らかなサイド光）
bpy.ops.object.light_add(type='AREA', location=(3.0, -1.5, 2.5))
fill_light = bpy.context.active_object
fill_light.data.energy = 180.0
fill_light.data.size = 3.0
fill_light.data.color = (0.9, 0.95, 1.0)
fill_light.rotation_euler = (math.radians(20), math.radians(45), math.radians(60))

# リムライト / トップライト（エッジを際立たせる白光）
bpy.ops.object.light_add(type='AREA', location=(0.0, 2.8, 3.5))
rim_light = bpy.context.active_object
rim_light.data.energy = 300.0
rim_light.data.size = 2.0
rim_light.data.color = (1.0, 1.0, 1.0)
rim_light.rotation_euler = (math.radians(-45), 0, 0)

# アンダーアップライト（すり鉢とガラスシリンダーの透明感を下から照らす）
bpy.ops.object.light_add(type='POINT', location=(0.0, 0.0, -1.8))
under_light = bpy.context.active_object
under_light.data.energy = 80.0
under_light.data.color = (1.0, 1.0, 1.0)
under_light.data.shadow_soft_size = 0.3

# 4. 超リアルマテリアル生成関数
def create_candy_material(name, base_color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # ベースカラー（鮮やかで深みのある色）
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    # 表面の粗さ（超高光沢）
    bsdf.inputs['Roughness'].default_value = 0.04
    # IOR（アクリル・キャンディ樹脂の屈折率 1.45）
    bsdf.inputs['IOR'].default_value = 1.45
    # Clearcoat（二層ラッカー塗装・飴細工のクリア層）
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
        bsdf.inputs['Coat Roughness'].default_value = 0.02
        bsdf.inputs['Coat IOR'].default_value = 1.5
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.02
    
    # 微小なサブサーフェス（光が内部で少し散乱するリッチなプラスチック感）
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.08
        bsdf.inputs['Subsurface Radius'].default_value = (0.1, 0.1, 0.1)
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = 0.08
        
    return mat

def create_frosted_acrylic_mat():
    mat = bpy.data.materials.new(name="FrostedAcrylic")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    bsdf.inputs['Base Color'].default_value = (0.95, 0.98, 1.0, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.15  # 高級感あるすりガラス
    bsdf.inputs['IOR'].default_value = 1.491       # PMMA(アクリル)の正確な屈折率
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 0.88
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 0.88
    return mat

def create_clear_glass_mat():
    mat = bpy.data.materials.new(name="ClearGlass")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.01  # 完全クリアガラス
    bsdf.inputs['IOR'].default_value = 1.52        # クラウンガラスの屈折率
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 1.0
    return mat

def create_studio_floor_mat():
    mat = bpy.data.materials.new(name="StudioFloor")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    bsdf.inputs['Base Color'].default_value = (0.07, 0.08, 0.10, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.25
    bsdf.inputs['Metallic'].default_value = 0.1
    return mat

# パレット（Kawaken風ビビッド・パステルキャンディ）
colors = [
    (0.98, 0.18, 0.35), # ルビーピンク
    (0.15, 0.58, 0.98), # シアンブルー
    (0.98, 0.72, 0.12), # サンシャインイエロー
    (0.18, 0.85, 0.55), # エメラルドグリーン
    (0.72, 0.22, 0.95), # パープル
    (0.98, 0.42, 0.15), # ネオンオレンジ
]
candy_mats = [create_candy_material(f"Candy_{i}", c) for i, c in enumerate(colors)]
acrylic_mat = create_frosted_acrylic_mat()
glass_mat = create_clear_glass_mat()
floor_mat = create_studio_floor_mat()

# 5. オブジェクト配置
# 背景・床（なだらかなインフィニティスタジオ背景）
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -2.5))
floor = bpy.context.active_object
floor.data.materials.append(floor_mat)

# ファンネル（すり鉢）
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=2.5, radius2=0.48, depth=1.6, location=(0, 0, 0.8))
funnel = bpy.context.active_object
funnel.rotation_euler = (0, 0, 0)
# 厚みをつける（Solidify）ことで本物のガラスの屈折とエッジのハイライトが生まれる！
mod_solid = funnel.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_solid.thickness = 0.08
mod_sub = funnel.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub.levels = 2
mod_sub.render_levels = 2
bpy.ops.object.shade_smooth()
funnel.data.materials.append(acrylic_mat)

# ガラスシリンダー
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.46, depth=2.8, location=(0, 0, -1.0))
cylinder = bpy.context.active_object
mod_solid_cyl = cylinder.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_solid_cyl.thickness = 0.05
mod_sub_cyl = cylinder.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub_cyl.levels = 2
bpy.ops.object.shade_smooth()
cylinder.data.materials.append(glass_mat)

# キャンディボール（ファンネル内で渦を巻いているリアルなスナップショット配置）
import random
random.seed(42)

balls = []
# ファンネル内の螺旋配置（約40個）
for i in range(45):
    t = i / 45.0
    r = 0.55 + t * 1.55 + random.uniform(-0.08, 0.08)
    theta = t * math.pi * 5.5 + random.uniform(-0.2, 0.2)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    # 円錐の傾斜に沿ったz座標
    z = 0.15 + t * 1.35 + random.uniform(-0.02, 0.05)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.13, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[i % len(candy_mats)])
    balls.append(ball)

# シリンダー内に既に落下して溜まっているボール（約15個）
for j in range(15):
    z = -2.2 + j * 0.21
    r = random.uniform(0.0, 0.22)
    ang = random.uniform(0, math.pi * 2)
    x = r * math.cos(ang)
    y = r * math.sin(ang)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.13, location=(x, y, z))
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(candy_mats[(j * 3 + 2) % len(candy_mats)])

# 6. カメラ設定（被写界深度 Depth of Field で手前・奥をボカす）
bpy.ops.object.camera_add(location=(0, -4.2, 2.0))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(72), 0, 0)
cam.data.lens = 55 # 中望遠（歪みのない美しいパース感）
scene.camera = cam

# 被写界深度（DoF）設定
cam.data.dof.use_dof = True
# ピントを合わせるターゲット：ファンネル中央で渦を巻くボール
cam.data.dof.focus_distance = 4.45
cam.data.dof.aperture_fstop = 2.4 # f/2.4の美しいボケ味

# 7. プロジェクト保存 & レンダリング
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/photoreal_test.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved blend to", blend_path)

out_png = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/renders/photoreal_test_render.png"
scene.render.filepath = out_png
bpy.ops.render.render(write_still=True)
print("Rendered photoreal test image to", out_png)
