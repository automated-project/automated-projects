import bpy
import math

# 1. シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "JellySliceScene"

# 120フレーム = 4.0秒 @ 30fps
scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 30

# 2. EEVEE設定
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 16

scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 3. スタジオライティング
world = bpy.data.worlds.new("JellyStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.93, 0.95, 0.97, 1.0)
bg.inputs['Strength'].default_value = 1.0

# メインキーライト
bpy.ops.object.light_add(type='AREA', location=(-2.5, -4.0, 6.0))
key = bpy.context.active_object
key.data.energy = 950.0
key.data.size = 4.5
key.data.color = (1.0, 0.98, 0.95)
key.rotation_euler = (math.radians(45), math.radians(-15), math.radians(-25))

# フィルライト
bpy.ops.object.light_add(type='AREA', location=(3.5, -3.0, 5.0))
fill = bpy.context.active_object
fill.data.energy = 550.0
fill.data.size = 4.0
fill.data.color = (0.95, 0.98, 1.0)
fill.rotation_euler = (math.radians(45), math.radians(25), math.radians(15))

# リムライト
bpy.ops.object.light_add(type='AREA', location=(0.0, 4.0, 5.5))
rim = bpy.context.active_object
rim.data.energy = 800.0
rim.data.size = 4.0
rim.rotation_euler = (math.radians(-45), 0, 0)

# 4. マテリアル
mat_jelly = bpy.data.materials.new(name="MatJelly")
mat_jelly.use_nodes = True
bsdf_j = mat_jelly.node_tree.nodes.get("Principled BSDF")
bsdf_j.inputs['Base Color'].default_value = (1.0, 0.05, 0.32, 1.0)
bsdf_j.inputs['Roughness'].default_value = 0.04
bsdf_j.inputs['IOR'].default_value = 1.35
if 'Subsurface Weight' in bsdf_j.inputs:
    bsdf_j.inputs['Subsurface Weight'].default_value = 0.35
    bsdf_j.inputs['Subsurface Radius'].default_value = (0.6, 0.2, 0.2)
elif 'Subsurface' in bsdf_j.inputs:
    bsdf_j.inputs['Subsurface'].default_value = 0.35

if 'Coat Weight' in bsdf_j.inputs:
    bsdf_j.inputs['Coat Weight'].default_value = 1.0
    bsdf_j.inputs['Coat Roughness'].default_value = 0.02
elif 'Clearcoat' in bsdf_j.inputs:
    bsdf_j.inputs['Clearcoat'].default_value = 1.0

mat_chrome = bpy.data.materials.new(name="MatChrome")
mat_chrome.use_nodes = True
bsdf_c = mat_chrome.node_tree.nodes.get("Principled BSDF")
bsdf_c.inputs['Base Color'].default_value = (0.95, 0.95, 0.98, 1.0)
bsdf_c.inputs['Metallic'].default_value = 1.0
bsdf_c.inputs['Roughness'].default_value = 0.10

mat_wire_gold = bpy.data.materials.new(name="MatWireGold")
mat_wire_gold.use_nodes = True
bsdf_wg = mat_wire_gold.node_tree.nodes.get("Principled BSDF")
bsdf_wg.inputs['Base Color'].default_value = (1.0, 0.80, 0.15, 1.0)
bsdf_wg.inputs['Metallic'].default_value = 1.0
bsdf_wg.inputs['Roughness'].default_value = 0.12

mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.86, 0.88, 0.92, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.25

# 5. 床とカッター
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.5))
floor = bpy.context.active_object
floor.scale = (30, 30, 1.0)
bpy.ops.object.transform_apply(scale=True)
floor.data.materials.append(mat_floor)

# カッター枠: Z = 1.0
cutter_z = 1.0
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.35,
    minor_radius=0.10,
    major_segments=48,
    minor_segments=16,
    location=(0, 0, cutter_z)
)
torus_frame = bpy.context.active_object
bpy.ops.object.shade_smooth()
torus_frame.data.materials.append(mat_chrome)

# ワイヤー
wire_pos = 0.28
for pos in [-wire_pos, wire_pos]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.016, depth=2.6, location=(0, pos, cutter_z))
    wx = bpy.context.active_object
    wx.rotation_euler = (0, math.radians(90), 0)
    wx.data.materials.append(mat_wire_gold)
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.016, depth=2.6, location=(pos, 0, cutter_z))
    wy = bpy.context.active_object
    wy.rotation_euler = (math.radians(90), 0, 0)
    wy.data.materials.append(mat_wire_gold)

# 6. ゼリーモデル
jelly_w = 1.65
jelly_h = 0.85
piece_size = 0.52
piece_coords = [-0.56, 0.0, 0.56]

# A. 切断前の「単一巨大ゼリー」
# 原点を中心に持つメッシュを作成
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
master_jelly = bpy.context.active_object
master_jelly.name = "MasterJelly"
master_jelly.scale = (jelly_w, jelly_w, jelly_h)
bpy.ops.object.transform_apply(scale=True)
mod_bev_m = master_jelly.modifiers.new(name="Bevel", type='BEVEL')
mod_bev_m.width = 0.12
mod_bev_m.segments = 4
mod_sub_m = master_jelly.modifiers.new(name="Subsurf", type='SUBSURF')
mod_sub_m.levels = 1
bpy.ops.object.shade_smooth()
master_jelly.data.materials.append(mat_jelly)

# MasterJelly アニメーション
# フレーム1: Z = 2.4 (画面上部に美しく登場)
master_jelly.location = (0, 0, 2.4)
master_jelly.keyframe_insert(data_path="location", frame=1)
master_jelly.hide_render = False
master_jelly.hide_viewport = False
master_jelly.keyframe_insert(data_path="hide_render", frame=1)
master_jelly.keyframe_insert(data_path="hide_viewport", frame=1)

# フレーム22: カッター直上 (Z = 1.425)
master_jelly.location = (0, 0, 1.425)
master_jelly.keyframe_insert(data_path="location", frame=22)

# フレーム26: ワイヤー食い込み (Z = 1.0)
master_jelly.location = (0, 0, 1.0)
master_jelly.keyframe_insert(data_path="location", frame=26)
master_jelly.hide_render = False
master_jelly.hide_viewport = False
master_jelly.keyframe_insert(data_path="hide_render", frame=26)
master_jelly.keyframe_insert(data_path="hide_viewport", frame=26)

# フレーム27: 非表示切り替え
master_jelly.hide_render = True
master_jelly.hide_viewport = True
master_jelly.keyframe_insert(data_path="hide_render", frame=27)
master_jelly.keyframe_insert(data_path="hide_viewport", frame=27)


# B. 切断後の「9個の分割ピース」
# 各ピースも原点(0,0,0)でスケール適用した後に位置を設定
for xi, gx in enumerate(piece_coords):
    for yi, gy in enumerate(piece_coords):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
        p = bpy.context.active_object
        p.name = f"JellyPiece_{xi}_{yi}"
        p.scale = (piece_size, piece_size, jelly_h)
        bpy.ops.object.transform_apply(scale=True)
        
        mod_bev = p.modifiers.new(name="Bevel", type='BEVEL')
        mod_bev.width = 0.05
        mod_bev.segments = 3
        mod_sub = p.modifiers.new(name="Subsurf", type='SUBSURF')
        mod_sub.levels = 1
        bpy.ops.object.shade_smooth()
        p.data.materials.append(mat_jelly)
        
        # 可視性
        p.hide_render = True
        p.hide_viewport = True
        p.keyframe_insert(data_path="hide_render", frame=1)
        p.keyframe_insert(data_path="hide_viewport", frame=1)
        p.keyframe_insert(data_path="hide_render", frame=26)
        p.keyframe_insert(data_path="hide_viewport", frame=26)
        
        p.hide_render = False
        p.hide_viewport = False
        p.keyframe_insert(data_path="hide_render", frame=27)
        p.keyframe_insert(data_path="hide_viewport", frame=27)
        
        # 動きキーフレーム
        # フレーム27: ワイヤー通過開始位置 (Z = 1.0)
        p.location = (gx, gy, 1.0)
        p.scale = (1.0, 1.0, 1.0)
        p.keyframe_insert(data_path="location", frame=27)
        p.keyframe_insert(data_path="scale", frame=27)
        
        # フレーム32: カッター通過直後
        spread_mid = 1.15
        p.location = (gx * spread_mid, gy * spread_mid, 0.70)
        p.scale = (1.02, 1.02, 0.98)
        p.keyframe_insert(data_path="location", frame=32)
        p.keyframe_insert(data_path="scale", frame=32)
        
        # フレーム42: 床に着地（Z = jelly_h/2 = 0.425）
        spread_land = 1.45
        lx = gx * spread_land
        ly = gy * spread_land
        p.location = (lx, ly, 0.425)
        p.keyframe_insert(data_path="location", frame=42)
        
        # フレーム45: スクワッシュ潰れ
        p.scale = (1.30, 1.30, 0.58)
        p.keyframe_insert(data_path="scale", frame=45)
        
        # フレーム53: ボヨヨンリバウンド
        p.location = (lx, ly, 0.68)
        p.scale = (0.85, 0.85, 1.25)
        p.keyframe_insert(data_path="location", frame=53)
        p.keyframe_insert(data_path="scale", frame=53)
        
        # フレーム62: 着地2
        p.location = (lx, ly, 0.425)
        p.scale = (1.10, 1.10, 0.90)
        p.keyframe_insert(data_path="location", frame=62)
        p.keyframe_insert(data_path="scale", frame=62)
        
        # フレーム74: 安定復元
        p.location = (lx, ly, 0.425)
        p.scale = (1.0, 1.0, 1.0)
        p.keyframe_insert(data_path="location", frame=74)
        p.keyframe_insert(data_path="scale", frame=74)

# 7. カメラ設定
bpy.ops.object.camera_add(
    location=(0.0, -4.5, 3.2),
    rotation=(math.radians(62), 0, 0)
)
cam = bpy.context.active_object
cam.data.lens = 42
scene.camera = cam

# プロジェクト保存
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/jelly_slice.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved perfect origin Jelly Slice blend to", blend_path)
