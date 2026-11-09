"""Render a local still as the non-WebGL accessibility fallback."""
import bpy,os,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def pos(v):return (v[0],-v[2],v[1])
for name in ['plot_base','orchard_trees','tiny_liberte','terrace']:
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT,'public','models',name+'.glb'))
    if name=='tiny_liberte':
        for o in set(bpy.data.objects)-before:
            if not o.parent:o.location+=Vector(pos((-2.7,.05,-2.7)))
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.86))
m=bpy.data.materials.new('Okolní krajina');m.diffuse_color=(.39,.46,.32,1);bpy.context.object.data.materials.append(m)
bpy.ops.object.camera_add(location=pos((23,21,27)))
camera=bpy.context.object;camera.rotation_euler=(Vector(pos((0,.3,0)))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=47;bpy.context.scene.camera=camera
bpy.ops.object.light_add(type='AREA',location=pos((-12,22,7)));bpy.context.object.data.energy=3800;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=12
bpy.context.object.rotation_euler=(Vector((0,0,0))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='SUN',location=(0,0,20));bpy.context.object.data.energy=2;bpy.context.object.rotation_euler=(.4,-.5,-.4);bpy.context.object.data.angle=.15
scene=bpy.context.scene;scene.world.color=(.45,.5,.4);scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False
scene.render.resolution_x=1400;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(ROOT,'work','garden-preview.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'work','garden-scene.blend'))
bpy.ops.render.render(write_still=True)
