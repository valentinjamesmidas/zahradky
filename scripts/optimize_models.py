"""Batch static GLB meshes by material without changing their world geometry.
Run: blender -b --python scripts/optimize_models.py
Original exports remain available; runtime uses public/models/optimized.
"""
import bpy,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/models/optimized';OUT.mkdir(exist_ok=True)
def info(path):
    b=path.read_bytes();j=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]])
    return {'bytes':len(b),'meshes':len(j.get('meshes',[])),'primitives':sum(len(m['primitives']) for m in j.get('meshes',[]))}
report={}
for path in sorted((ROOT/'public/models').glob('*.glb')):
    if path.stem in ['house_nova','addons','offgrid_tech']:continue
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(path))
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':
            matrix=o.matrix_world.copy();o.parent=None;o.matrix_world=matrix
    groups={}
    for o in bpy.context.scene.objects:
        if o.type=='MESH':groups.setdefault(tuple(m.name for m in o.data.materials),[]).append(o)
    joined=[]
    for names,objects in groups.items():
        bpy.ops.object.select_all(action='DESELECT')
        for o in objects:o.select_set(True)
        bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
        o=bpy.context.object;o.name=path.stem+'_'+('_'.join(names));joined.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in joined:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/path.name),export_format='GLB',use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
    report[path.stem]={'before':info(path),'after':info(OUT/path.name)}
(ROOT/'docs/model-optimization.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
