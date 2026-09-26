import bpy
import math

# 1. シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "RhythmSlicerScene"

# 180フレーム = 6.0秒 @ 30fps
scene.frame_start = 1
scene.frame_end = 180
scene.render.fps = 30

# 2. 高画質・爆速 EEVEE 設定 (1フレーム約1秒)
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 16

scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Punchy'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920

# 3. ポップ＆クリーンなスタジオライティング
world = bpy.data.worlds.new("RhythmStudio")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = (0.95, 0.96, 0.98, 1.0)
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
rim.data.energy = 850.0
rim.data.size = 4.0
rim.rotation_euler = (math.radians(-45), 0, 0)

# 4. マテリアルパレット（鮮やかなポップカラー）
def create_jelly_material(name, color_rgba, sss_radius=(0.5, 0.2, 0.2)):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color_rgba
    bsdf.inputs['Roughness'].default_value = 0.04
    bsdf.inputs['IOR'].default_value = 1.35
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.35
        bsdf.inputs['Subsurface Radius'].default_value = sss_radius
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = 0.35
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
        bsdf.inputs['Coat Roughness'].default_value = 0.02
    return mat

mat_ruby = create_jelly_material("MatRuby", (1.0, 0.05, 0.32, 1.0), (0.6, 0.2, 0.2)) # ストロベリー
mat_cyan = create_jelly_material("MatCyan", (0.05, 0.65, 1.0, 1.0), (0.2, 0.4, 0.6)) # ブルーハワイ
mat_gold = create_jelly_material("MatGold", (1.0, 0.75, 0.08, 1.0), (0.5, 0.4, 0.1)) # マンゴーゴールド
mat_lime = create_jelly_material("MatLime", (0.15, 0.95, 0.35, 1.0), (0.2, 0.6, 0.2)) # ライムグリーン

# メタリックフレーム＆ゴールドワイヤー
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

# スタジオ床
mat_floor = bpy.data.materials.new(name="MatFloor")
mat_floor.use_nodes = True
bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
bsdf_fl.inputs['Base Color'].default_value = (0.88, 0.90, 0.93, 1.0)
bsdf_fl.inputs['Roughness'].default_value = 0.25

# 5. 床とカッター
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.5))
floor = bpy.context.active_object
floor.scale = (30, 30, 1.0)
bpy.ops.object.transform_apply(scale=True)
floor.data.materials.append(mat_floor)

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

# ワイヤー格子 (3x3 = ±0.28)
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

# 6. ビートシンク・4連続スライス構築
# 各ステージ定義: (開始フレーム, 切断フレーム, 着地フレーム, 終了フレーム, マテリアル)
stages = [
    (1, 23, 35, 45, mat_ruby),     # Stage 0: Ruby Strawberry (Drop 1)
    (46, 68, 80, 90, mat_cyan),    # Stage 1: Cyan Blue Hawaii (Drop 2)
    (91, 113, 125, 135, mat_gold), # Stage 2: Mango Gold (Drop 3)
    (136, 158, 170, 180, mat_lime) # Stage 3: Lime Emerald (Drop 4)
]

jelly_w = 1.65
jelly_h = 0.85
piece_size = 0.52
piece_coords = [-0.56, 0.0, 0.56]

for stage_idx, (f_start, f_cut, f_land, f_end, mat) in enumerate(stages):
    # --- A. 切断前の単一巨大ゼリー ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    master = bpy.context.active_object
    master.name = f"MasterJelly_{stage_idx}"
    master.scale = (jelly_w, jelly_w, jelly_h)
    bpy.ops.object.transform_apply(scale=True)
    
    mod_bev = master.modifiers.new(name="Bevel", type='BEVEL')
    mod_bev.width = 0.12
    mod_bev.segments = 4
    mod_sub = master.modifiers.new(name="Subsurf", type='SUBSURF')
    mod_sub.levels = 1
    bpy.ops.object.shade_smooth()
    master.data.materials.append(mat)
    
    # 可視性キーフレーム
    master.hide_render = True
    master.hide_viewport = True
    master.keyframe_insert(data_path="hide_render", frame=1)
    master.keyframe_insert(data_path="hide_viewport", frame=1)
    if f_start > 1:
        master.keyframe_insert(data_path="hide_render", frame=f_start - 1)
        master.keyframe_insert(data_path="hide_viewport", frame=f_start - 1)
        
    master.hide_render = False
    master.hide_viewport = False
    master.keyframe_insert(data_path="hide_render", frame=f_start)
    master.keyframe_insert(data_path="hide_viewport", frame=f_start)
    master.keyframe_insert(data_path="hide_render", frame=f_cut - 1)
    master.keyframe_insert(data_path="hide_viewport", frame=f_cut - 1)
    
    master.hide_render = True
    master.hide_viewport = True
    master.keyframe_insert(data_path="hide_render", frame=f_cut)
    master.keyframe_insert(data_path="hide_viewport", frame=f_cut)
    
    # 落下アニメーション
    master.location = (0, 0, 2.4)
    master.keyframe_insert(data_path="location", frame=f_start)
    
    master.location = (0, 0, 1.425)
    master.keyframe_insert(data_path="location", frame=f_cut - 3)
    
    master.location = (0, 0, 1.0)
    master.keyframe_insert(data_path="location", frame=f_cut - 1)

    # --- B. 切断後の9個の分割ピース ---
    for xi, gx in enumerate(piece_coords):
        for yi, gy in enumerate(piece_coords):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
            p = bpy.context.active_object
            p.name = f"JellyPiece_{stage_idx}_{xi}_{yi}"
            p.scale = (piece_size, piece_size, jelly_h)
            bpy.ops.object.transform_apply(scale=True)
            
            mod_pbev = p.modifiers.new(name="Bevel", type='BEVEL')
            mod_pbev.width = 0.05
            mod_pbev.segments = 3
            mod_psub = p.modifiers.new(name="Subsurf", type='SUBSURF')
            mod_psub.levels = 1
            bpy.ops.object.shade_smooth()
            p.data.materials.append(mat)
            
            # 可視性
            p.hide_render = True
            p.hide_viewport = True
            p.keyframe_insert(data_path="hide_render", frame=1)
            p.keyframe_insert(data_path="hide_viewport", frame=1)
            p.keyframe_insert(data_path="hide_render", frame=f_cut - 1)
            p.keyframe_insert(data_path="hide_viewport", frame=f_cut - 1)
            
            p.hide_render = False
            p.hide_viewport = False
            p.keyframe_insert(data_path="hide_render", frame=f_cut)
            p.keyframe_insert(data_path="hide_viewport", frame=f_cut)
            p.keyframe_insert(data_path="hide_render", frame=f_end)
            p.keyframe_insert(data_path="hide_viewport", frame=f_end)
            
            p.hide_render = True
            p.hide_viewport = True
            p.keyframe_insert(data_path="hide_render", frame=f_end + 1)
            p.keyframe_insert(data_path="hide_viewport", frame=f_end + 1)
            
            # 動きアニメーション
            # 1. 切断開始
            p.location = (gx, gy, 1.0)
            p.scale = (1.0, 1.0, 1.0)
            p.keyframe_insert(data_path="location", frame=f_cut)
            p.keyframe_insert(data_path="scale", frame=f_cut)
            
            # 2. カッター通過
            spread_mid = 1.15
            p.location = (gx * spread_mid, gy * spread_mid, 0.70)
            p.scale = (1.02, 1.02, 0.98)
            p.keyframe_insert(data_path="location", frame=f_cut + 4)
            p.keyframe_insert(data_path="scale", frame=f_cut + 4)
            
            # 3. 床着地
            spread_land = 1.45
            lx = gx * spread_land
            ly = gy * spread_land
            p.location = (lx, ly, 0.425)
            p.keyframe_insert(data_path="location", frame=f_land)
            
            # 4. スクワッシュ潰れ
            p.scale = (1.30, 1.30, 0.58)
            p.keyframe_insert(data_path="scale", frame=f_land + 2)
            
            # 5. ボヨヨンリバウンド
            p.location = (lx, ly, 0.65)
            p.scale = (0.85, 0.85, 1.25)
            p.keyframe_insert(data_path="location", frame=f_land + 6)
            p.keyframe_insert(data_path="scale", frame=f_land + 6)
            
            # 6. 着地・外側へスライドアウト（次のゼリーのために画面外へサッと退場）
            p.location = (lx * 1.8, ly * 1.8, 0.425)
            p.scale = (1.0, 1.0, 1.0)
            p.keyframe_insert(data_path="location", frame=f_end)
            p.keyframe_insert(data_path="scale", frame=f_end)

# 7. カメラ設定（見下ろし構図）
bpy.ops.object.camera_add(
    location=(0.0, -4.5, 3.2),
    rotation=(math.radians(62), 0, 0)
)
cam = bpy.context.active_object
cam.data.lens = 42
scene.camera = cam

# プロジェクト保存
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/rhythm_slicer.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved Rhythm Slicer blend to", blend_path)
