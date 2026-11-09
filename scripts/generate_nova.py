"""TŘY D NOVA: reference-based architectural model, not construction documentation.
Source: https://tryd.cz/hybridni-dum-nova/ (accessed 2026-11-09).
Published footprint: 4 x 3 m. Roof heights, recess and openings are estimated from
manufacturer's exterior illustrations. No trailer, wheels or solar array included.
Run: blender --background --python scripts/generate_nova.py [-- --render]
Exports a self-contained GLB and an editable Blender file without presentation props.
"""
import bpy, math, os, sys, random
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'public','models');os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.preferences.filepaths.save_version=0
for block in list(bpy.data.materials):bpy.data.materials.remove(block)
def pos(p):return (p[0],-p[2],p[1])
def linear(v):return ((v+.055)/1.055)**2.4 if v>.04045 else v/12.92
def color(h):return tuple(linear(int(h[i:i+2],16)/255) for i in [0,2,4])
def material(name,h,rough=.6,metal=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color(h),1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
wood=material('NOVA Thermowood — tepelně upravená borovice','A58254',.74)
wood_dark=material('NOVA Thermowood — tmavší lamely','927047',.76)
# Packed raster grain is portable in glTF and editable in Blender.
rng=random.Random(83);image=bpy.data.images.new('NOVA — textura borovicového dřeva',width=64,height=256)
pixels=[]
base=color('A58254')
for y in range(256):
 for x in range(64):
  grain=1+.08*math.sin(x*.72+.45*math.sin(y*.028))+.035*math.sin(x*2.7+y*.011)+rng.uniform(-.02,.02)
  pixels.extend([min(1,c*grain) for c in base]+[1])
image.pixels.foreach_set(pixels);image.pack()
node=wood.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;wood.node_tree.links.new(node.outputs['Color'],wood.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
metal=material('NOVA Classic click — antracitový plech','33383C',.43,.65)
frame=material('NOVA antracitové rámy','282C2E',.35,.5)
interior=material('NOVA světlé vnitřní palubky','D5C4A4',.8)
steel=material('NOVA kotevní patky','777C7B',.42,.75)
glass=material('NOVA průhledné zasklení','DAE4DF',.1,0)
p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.95;p.inputs['IOR'].default_value=1.45
warm=material('NOVA teplé osvětlení zápraží','FFDBAA',.4)
p=warm.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(*color('FFDBAA'),1);p.inputs['Emission Strength'].default_value=2.2

def cube(name,p,d,m,bevel=.008):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos(p));o=bpy.context.object;o.name=name;o.dimensions=(d[0],d[2],d[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:
  mod=o.modifiers.new('Zaoblení skutečných hran','BEVEL');mod.width=bevel;mod.segments=2;o.modifiers.new('Vážené normály','WEIGHTED_NORMAL')
 return o

def poly(name,vertices,faces,m):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata([pos(v) for v in vertices],[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(m)
 uv=mesh.uv_layers.new(name='NOVA — svislá kresba dřeva')
 for face in mesh.polygons:
  for li in face.loop_indices:
   v=mesh.vertices[mesh.loops[li].vertex_index].co
   uv.data[li].uv=((v.x+2)*8,v.z*.35)
 return o

def prism(name,x0,x1,bottom,top0,top1,z0,z1,m):
 return poly(name,[(x0,bottom,z0),(x1,bottom,z0),(x1,top1,z0),(x0,top0,z0),(x0,bottom,z1),(x1,bottom,z1),(x1,top1,z1),(x0,top0,z1)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)],m)

def beam(name,a,b,w,d,m):
 delta=Vector(pos(b))-Vector(pos(a));o=cube(name,tuple((a[i]+b[i])/2 for i in range(3)),(w,delta.length,d),m,.005);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o

W,D=4,3;floor=.27;eave=2.65;ridge=3.55;front=1.13;rear=-1.5
# Raised foundation feet represent an illustrative support solution, not a trailer.
for x in [-1.65,0,1.65]:
 for z in [-1.25,1.25]:
  cube('NOVA — kotevní patka',(x,.07,z),(.22,.14,.22),steel)
  cube('NOVA — nosný podlahový hranol',(x,.16,z),(.15,.18,.2),wood_dark)
cube('NOVA — izolovaná podlaha',(0,.21,0),(4,.16,3),wood_dark,.015)
# Open interior, with visible floorboards rather than an opaque box behind glazing.
for i in range(26):cube('NOVA — podlahová palubka',(-1.92+i*.153,.303,-.13),(.145,.035,2.7),interior,.002)
for side in [-1,1]:
 cube('NOVA — boční stěna s izolací',(side*1.91,1.48,-.18),(.178,2.35,2.64),interior,.006)
 for k in range(15):
  z=-1.5+(k+.5)*3/15
  cube('NOVA — boční panel Classic click',(side*2.005,1.48,z),(.035,2.36,.197),metal,.003)
  cube('NOVA — boční stojatá drážka',(side*2.031,1.48,z-.097),(.032,2.36,.012),metal,.002)
 # Front returns and soffits clad with fine vertical slats.
 for j in range(3):cube('NOVA — čelní dřevěná ostění',(side*(1.72+j*.105),1.47,1.48),(.1,2.4,.095),wood if j%2 else wood_dark,.003)
 for k in range(5):cube('NOVA — dřevěné ostění zápraží',(side*1.82,1.47,1.19+k*.07),(.055,2.39,.066),wood,.003)
# Rear wall and a metal-clad gable.
cube('NOVA — zadní izolovaná stěna',(0,1.48,-1.41),(3.82,2.36,.178),interior,.006)
for i in range(20):
 x=-2+(i+.5)*.2;t0=ridge-abs(x-.1)/2*(ridge-eave);t1=ridge-abs(x+.1)/2*(ridge-eave)
 prism('NOVA — zadní plechový panel',x-.099,x+.099,.3,t0,t1,-1.535,-1.5,metal)
 cube('NOVA — zadní stojatá drážka',(x-.096,(.3+min(t0,t1))/2,-1.55),(.014,min(t0,t1)-.3,.025),metal,.002)
# Gable front: individually cut Thermowood boards above four glass door leaves.
for i in range(38):
 x=-1.9+(i+.5)*3.8/38
 t0=ridge-abs(x-.049)/2*(ridge-eave);t1=ridge-abs(x+.049)/2*(ridge-eave)
 prism('NOVA — svislá štítová palubka',x-.047,x+.047,2.48,t0,t1,front-.03,front+.035,wood if i%4 else wood_dark)
# Triple glazing appearance with four framed panes (doors shown closed).
left,right=-1.54,1.54;bottom,top=.33,2.48
for i in range(4):
 x0=left+i*(right-left)/4;x1=left+(i+1)*(right-left)/4
 cube('NOVA — čiré čtyřdílné prosklení',((x0+x1)/2,(bottom+top)/2,front+.025),(x1-x0-.075,top-bottom-.12,.025),glass,.002)
 for x in [x0+.027,x1-.027]:cube('NOVA — svislý rám Schüco',(x,(bottom+top)/2,front+.045),(.054,top-bottom,.09),frame,.003)
 for y in [bottom+.03,top-.03]:cube('NOVA — vodorovný rám Schüco',((x0+x1)/2,y,front+.045),(x1-x0,.06,.09),frame,.003)
for x in [-.095,.095]:
 cube('NOVA — dveřní klika',(x,1.25,front+.115),(.025,.19,.035),steel,.004)
 for y in [.7,2.05]:cube('NOVA — dveřní závěs',(x*8,y,front+.105),(.025,.09,.025),frame,.003)
# Front side portions between door opening and corner piers.
for side in [-1,1]:
 for k in range(3):cube('NOVA — svislý obklad u zasklení',(side*(1.59+k*.10),1.42,front),(.095,2.2,.065),wood,.003)
# Recessed timber porch, within the 4 x 3 m footprint.
for i in range(32):cube('NOVA — prkno zápraží',(-1.94+i*.125,.31,1.32),(.118,.055,.37),wood if i%4 else wood_dark,.002)
cube('NOVA — přední hrana zápraží',(0,.23,1.53),(4,.17,.06),wood,.004)
# Gable roof: accurately sloped planes, standing seams, ridge cap, timber soffit.
roof_half=2.12;rise=.96;angle=math.atan2(rise,roof_half);length=math.sqrt(roof_half**2+rise**2)
for side in [-1,1]:
 roof=cube('NOVA — sklon sedlové střechy',(side*roof_half/2,ridge-rise/2+.055,0),(length,.095,3.36),metal,.008);roof.rotation_euler[1]=side*angle
 soffit=cube('NOVA — dřevěný podhled zápraží',(side*roof_half/2,ridge-rise/2-.015,1.43),(length,.04,.48),wood,.003);soffit.rotation_euler[1]=side*angle
 # Seams run from ridge to eaves (along the slope), across each roof sheet.
 for k in range(12):
  seam=cube('NOVA — střešní stojatá drážka',(side*roof_half/2,ridge-rise/2+.115,-1.65+k*.30),(length,.035,.018),metal,.002);seam.rotation_euler[1]=side*angle
 for z in [-1.7,1.7]:
  fascia=cube('NOVA — antracitové závětrné lemování',(side*roof_half/2,ridge-rise/2+.09,z),(length,.12,.035),metal,.002);fascia.rotation_euler[1]=side*angle
  if z>0:
   # Narrow vertical cladding on the front fascia below the metal edge.
   for j in range(20):
    x=side*(j+.5)*roof_half/20;y=ridge-abs(x)/roof_half*rise-.04
    x0=x-.051;x1=x+.051;t0=ridge-abs(x0)/roof_half*rise+.03;t1=ridge-abs(x1)/roof_half*rise+.03;z0=z-.055;z1=z
    poly('NOVA — šikmo řezané čelo střechy',[(x0,t0-.14,z0),(x1,t1-.14,z0),(x1,t1,z0),(x0,t0,z0),(x0,t0-.14,z1),(x1,t1-.14,z1),(x1,t1,z1),(x0,t0,z1)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)],wood)
cube('NOVA — hřebenové oplechování',(0,ridge+.13,0),(.14,.055,3.42),metal,.004)
# Recessed warm strip; scene lighting in React controls day/evening balance.
for x in [-1,1]:cube('NOVA — zapuštěné světlo v podhledu',(x,3.00,1.34),(.10,.025,.09),warm,.008)
scene=bpy.context.scene
scene['model']='TŘY D — hybridní dům NOVA 4 × 3 m'
scene['reference']='https://tryd.cz/hybridni-dum-nova/'
scene['dimensions']='Půdorys 4 × 3 m dle výrobce; výšky a otvory odhadnuty z ilustrací.'
scene['not_included']='Doprava, montáž, založení, terasa a solární systém nejsou součástí modelu domu.'
# Save an editable, component-based source with the viewport framed around the house.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_location=(0,0,1.7)
   area.spaces.active.region_3d.view_distance=8
   area.spaces.active.region_3d.view_rotation=(Vector(pos((7.5,4.5,9.5)))-Vector(pos((0,1.65,0)))).to_track_quat('Z','Y')
   area.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'nova.blend'),compress=True)
# Join by material for the web export; retain the separate pieces in the saved blend.
for o in list(bpy.context.scene.objects):
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o
  for modifier in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
for m in list(bpy.data.materials):
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and len(o.data.materials)==1 and o.data.materials[0]==m]
 if not objects:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 bpy.context.object.name=m.name
 bpy.context.object['reference']='https://tryd.cz/hybridni-dum-nova/'

bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'house_nova.glb'),export_format='GLB',export_apply=True,export_yup=True,export_extras=True)
print('NOVA exported: house_nova.glb + nova.blend')
if '--render' in sys.argv:
 # Presentation assets are added only after saving the editable house and GLB.
 ground=material('Prezentační podklad','A2AC97',.9)
 cube('Podklad',(0,-.035,0),(200,.05,200),ground,0)
 bpy.ops.object.camera_add(location=pos((7.5,4.5,9.5)))
 camera=bpy.context.object;camera.rotation_euler=(Vector(pos((0,1.65,0)))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=53;scene.camera=camera
 bpy.ops.object.light_add(type='AREA',location=pos((-3,8,5)));bpy.context.object.data.energy=1600;bpy.context.object.data.size=5;bpy.context.object.rotation_euler=(Vector(pos((0,1,0)))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.light_add(type='AREA',location=pos((4,4,-3)));bpy.context.object.data.energy=1000;bpy.context.object.data.size=4;bpy.context.object.rotation_euler=(Vector(pos((0,1,0)))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
 scene.world.color=(.5,.5,.5);scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False
 scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
 scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(ROOT,'work','nova','nova-preview.png')
 bpy.ops.render.render(write_still=True)
