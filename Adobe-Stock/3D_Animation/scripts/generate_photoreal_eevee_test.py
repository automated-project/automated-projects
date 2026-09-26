import bpy
import math

bpy.ops.wm.open_mainfile(filepath="/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/photoreal_test.blend")
scene = bpy.context.scene

# Blender 5.2 では EEVEE が 'BLENDER_EEVEE' で次世代仕様（Raytracing内蔵）
scene.render.engine = 'BLENDER_EEVEE'

# EEVEE設定
if hasattr(scene, 'eevee'):
    eevee = scene.eevee
    if hasattr(eevee, 'use_raytracing'):
        eevee.use_raytracing = True
    if hasattr(eevee, 'taa_render_samples'):
        eevee.taa_render_samples = 64
    if hasattr(eevee, 'shadow_cascade_size'):
        eevee.shadow_cascade_size = '2048'

# プロジェクト上書き保存
bpy.ops.wm.save_as_mainfile(filepath="/Users/base/Automated-Projects/YouTube/02_3D_Animation/blender_projects/photoreal_test.blend")
print("Saved blend as BLENDER_EEVEE")
