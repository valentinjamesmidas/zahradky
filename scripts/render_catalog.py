"""Consistent thumbnails for the existing catalog, generated from actual GLBs.
blender -b -t 4 --python scripts/render_catalog.py
python scripts/encode_catalog.py
"""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'work/catalog-renders';OUT.mkdir(parents=True,exist_ok=True)
names=['tiny_liberte','tiny_millhome','tiny_baluchon','tiny_anna','orchard_trees','terrace','corten_beds','firepit_pergola','solar_tech','water_tech','offgrid_tech']
for name in names:
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    path=ROOT/'public/models/optimized'/f'{name}.glb'
    if not path.exists():path=ROOT/'public/models'/f'{name}.glb'
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    bounds=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box]
    low=Vector(tuple(min(v[i] for v in bounds) for i in range(3)));high=Vector(tuple(max(v[i] for v in bounds) for i in range(3)))
    center=(low+high)*.5;size=max(high-low)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,low.z-.03))
    ground=bpy.data.materials.new('Studio');ground.diffuse_color=(.065,.095,.077,1);bpy.context.object.data.materials.append(ground)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False
    scene.render.resolution_x=480;scene.render.resolution_y=360;scene.render.resolution_percentage=100
    scene.world.color=(.24,.24,.24)
    for pos,power,diam in [((2,-4,7),1700,6),((-4,-1,4),1000,5),((1,4,5),2100,4)]:
        bpy.ops.object.light_add(type='AREA',location=center+Vector(pos)*max(1,size/5))
        l=bpy.context.object;l.data.energy=power*max(1,size/5)**2;l.data.shape='DISK';l.data.size=diam
        l.rotation_euler=(center-l.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.camera_add(location=center+Vector((1.1,-1.5,.95))*size)
    cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.48;scene.camera=cam
    scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/f'{name}.png')
    bpy.ops.render.render(write_still=True)
    print('THUMBNAIL_DONE',name,flush=True)
