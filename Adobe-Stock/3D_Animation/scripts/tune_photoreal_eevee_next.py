import bpy
import math

scene = bpy.context.scene

# EEVEE (Next) を最高品質で構成
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# EEVEE Nextのレイトレーシング・スクリーンスペースリフレクション
if hasattr(scene, 'eevee'):
    eevee = scene.eevee
    if hasattr(eevee, 'use_raytracing'):
        eevee.use_raytracing = True
        eevee.ray_tracing_method = 'SCREEN'
        eevee.screen_trace_quality = 1.0
    if hasattr(eevee, 'use_gtao'):
        eevee.use_gtao = True
        eevee.gtao_distance = 0.5
    if hasattr(eevee, 'use_bloom'):
        eevee.use_bloom = True
    if hasattr(eevee, 'taa_render_samples'):
        eevee.taa_render_samples = 64

# 各マテリアルの透過・屈折・シャドウ設定
for mat in bpy.data.materials:
    if "Acrylic" in mat.name or "Glass" in mat.name:
        if hasattr(mat, 'use_screen_refraction'):
            mat.use_screen_refraction = True
        if hasattr(mat, 'refraction_depth'):
            mat.refraction_depth = 0.08
        if hasattr(mat, 'blend_method'):
            mat.blend_method = 'HASHED'
        if hasattr(mat, 'shadow_method'):
            mat.shadow_method = 'HASHED'

# プロジェクト保存
blend_path = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/photoreal_test.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Updated blend settings for EEVEE Next Photorealism.")
