"""Original garden concept library. Blender 4.3+, metres, GLB Y-up.

blender -b --python scripts/generate_expanded_assets.py -- [--only studio] [--no-render]
No third-party models, textures, brand representations or commercial claims.
"""
import bpy, math, random, json, sys, argparse
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--only')
parser.add_argument('--no-render', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
random.seed(21)

def material(name, color, rough=.6, metal=0, alpha=1, emission=0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, alpha)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    p.inputs['Alpha'].default_value = alpha
    if alpha < 1: m.surface_render_method = 'DITHERED'
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    m.diffuse_color = (*color, alpha)
    return m

def setup():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    global wood, cedar, dark, steel, glass, linen, leaf, soil, stone, water, glow, solar, corten
    wood=material('Modrin',(.45,.28,.14)); cedar=material('Cedr',(.3,.13,.065))
    dark=material('Antracit',(.028,.04,.037),.4,.4); steel=material('Ocel',(.25,.28,.27),.3,.8)
    glass=material('Sklo',(.3,.55,.57),.18,.15,.32)
    linen=material('Len',(.79,.74,.61),.95); leaf=material('Zelen',(.14,.27,.09))
    soil=material('Substrat',(.065,.035,.02)); stone=material('Kamen',(.4,.43,.38))
    water=material('Voda',(.035,.27,.28),.15,.25)
    glow=material('Teple svetlo', (1,.55,.17),.4,0,1,3)
    solar=material('Solarni clanky',(.015,.035,.085),.23,.65)
    corten=material('Corten',(.323,.061,.018),.75,.3)

def finish(o, name, mat):
    o.name=name; o.data.materials.append(mat); return o

def box(name, pos, size, mat, rot=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o=bpy.context.object; o.dimensions=size; o.rotation_euler[2]=rot
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,mat)

def cyl(name, pos, radius, depth, mat, vertices=16, rotation=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=pos)
    o=bpy.context.object
    if rotation: o.rotation_euler=rotation
    return finish(o,name,mat)

def beam(name, a, b, width, mat):
    mid=(Vector(a)+Vector(b))/2; d=Vector(b)-Vector(a)
    o=box(name,mid,(width,width,d.length),mat)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); return o

def sphere(name,pos,scale,mat,sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=pos)
    o=bpy.context.object; o.scale=scale; return finish(o,name,mat)

def slats(x,y,z,w,h,mat= None):
    mat=mat or wood
    for i in range(max(1,int(w/.15))):
        box('Svisla lamela',(x-w/2+.075+i*.15,y,z),(.133,.065,h),mat)

def deck(w=4,d=3,x=0,y=0):
    for i in range(int(d/.16)):
        box('Prkno terasy',(x,y-d/2+.08+i*.16,.13),(w,.149,.12),wood)
    for dx in [-w/2+.2,w/2-.2]:
        for dy in [-d/2+.2,d/2-.2]: cyl('Zemni podpera',(x+dx,y+dy,.05),.055,.1,steel)

def chair(x,y,rot=0):
    # Local chair geometry rotated as a group about its centre.
    before=set(bpy.data.objects)
    for a in [-.23,.23]:
        for b in [-.23,.23]: box('Noha kresla',(a,b,.25),(.055,.055,.5),wood)
    box('Podsedak',(0,0,.51),(.57,.56,.12),linen)
    box('Operadlo',(0,.25,.82),(.59,.1,.58),linen)
    for a in [-.3,.3]: box('Podrucka',(a,0,.73),(.055,.65,.055),wood)
    for o in set(bpy.data.objects)-before:
        px,py,pz=o.location; o.location=(x+px*math.cos(rot)-py*math.sin(rot),y+px*math.sin(rot)+py*math.cos(rot),pz)
        o.rotation_euler[2]+=rot

def pot(x,y,z=0,r=.3):
    cyl('Kvetinac',(x,y,z+r*.7),r,r*1.4,corten)
    cyl('Substrat',(x,y,z+r*1.42),r*.92,.025,soil)
    for i in range(5):
        a=i*math.tau/5
        sphere('List',(x+math.cos(a)*r*.5,y+math.sin(a)*r*.5,z+r*1.9),(.14,.14,.3),leaf)

def solar_panel(x,y,z,w=1,d=1.65):
    box('Ram panelu',(x,y,z),(w,d,.065),steel)
    for i in range(4):
        for j in range(6): box('Fotovoltaicky clanek',(x-w/2+(i+.5)*w/4,y-d/2+(j+.5)*d/6,z+.04),(w/4-.012,d/6-.012,.012),solar)

def house(style):
    w=6 if style in ['panorama','pavilion'] else 5.4; d=2.55
    z=.65
    if style!='pavilion':
        box('Ram podvozku',(0,0,.47),(w+.15,d+.1,.19),steel)
        for x in [-.8,.8]:
            for y in [-1.32,1.32]:
                cyl('Pneumatika',(x,y,.32),.32,.2,dark,20,(math.pi/2,0,0))
                cyl('Rafek',(x,y*1.08,.32),.17,.025,steel,16,(math.pi/2,0,0))
        for y in [-1,1]: beam('Oj',(w/2,y,.45),(w/2+1.5,0,.45),.09,steel)
    box('Podlaha',(0,0,z),(w,d,.18),wood)
    box('Zadni stena',(0,d/2,z+1.25),(w,.13,2.5),cedar)
    for x in [-w/2,w/2]: box('Bocni stena',(x,0,z+1.25),(.14,d,2.5),wood)
    slats(0,d/2+.09,z+1.25,w,2.5,cedar)
    opening=w*.68 if style in ['panorama','pavilion'] else 2.1
    side=(w-opening)/2
    for s in [-1,1]: slats(s*(opening/2+side/2),-d/2,z+1.25,side,2.5)
    box('Celni proskleni',(0,-d/2+.03,z+1.25),(opening,.025,2.4),glass)
    for x in [-opening/2,0,opening/2]: box('Okenni profil',(x,-d/2-.025,z+1.25),(.065,.09,2.5),dark)
    for h in [z+.04,z+2.46]: box('Okenni profil',(0,-d/2-.025,h),(opening,.09,.07),dark)
    # Interior visible through glazing.
    box('Lavice',(0,.6,z+.42),(2,.68,.65),linen)
    box('Kuchynska linka',(w/2-.55,.3,z+.5),(.7,1.6,.95),wood)
    box('Pracovni deska',(w/2-.55,.3,z+1),(.76,1.67,.06),stone)
    if style=='nordic':
        for s in [-1,1]:
            o=box('Sedlova strecha',(0,s*.69,z+2.75),(w+.35,1.6,.12),dark)
            o.rotation_euler[0]=-s*.45
        cyl('Komin',(-1.5,.5,z+3.25),.12,1.1,dark)
    else:
        box('Plocha strecha',(0,0,z+2.57),(w+.3,d+.3,.16),dark)
        if style=='studio':
            solar_panel(-1,0,z+2.7); solar_panel(.1,0,z+2.7)
    if style=='pavilion':
        for x in [-2.9,-1.5,0,1.5,2.9]:
            beam('Drevene zebro',(x,-1.65,0),(x,-1.65,3.35),.11,wood)
            beam('Drevene zebro',(x,-1.65,3.35),(x,1.6,3.35),.11,wood)
    deck(w,1.5,y=-2.2)
    pot(-w/2+.5,-2.3,.2)

def pergola():
    deck(4.5,3.6)
    for x in [-2,2]:
        for y in [-1.5,1.5]: box('Sloupek',(x,y,1.35),(.15,.15,2.7),wood)
        box('Nosnik',(x,0,2.7),(.16,3.5,.18),wood)
    for i in range(13): box('Stresni lamela',(-2.1+i*.35,0,2.8),(.11,3.5,.14),wood)
    for x in [-1,1]: chair(x,.6)
    cyl('Stolek',(0,-.5,.45),.47,.08,dark)
    cyl('Noha stolku',(0,-.5,.27),.07,.4,dark)
    for i in range(11):
        x=-2+i*.4; z=2.6-.3*(1-(x/2)**2)
        sphere('Feston',(x,-1.5,z),(.065,.065,.085),glow,2)
        if i: beam('Kabel',(x-.4,-1.5,2.6-.3*(1-((x-.4)/2)**2)),(x,-1.5,z),.012,dark)

def greenhouse():
    w=3; d=4
    box('Zaklad',(0,0,.1),(w+.2,d+.2,.2),stone)
    for x in [-1.5,1.5]:
        box('Sklenena stena',(x,0,1.15),(.02,d,2),glass)
        for y in [-2,-1,0,1,2]:
            beam('Profil',(x,y,.2),(x,y,2.15),.055,dark)
            beam('Krokev',(x,y,2.15),(0,y,3),.055,dark)
        o=box('Stresni sklo',(x/2,0,2.57),(1.72,d,.02),glass);o.rotation_euler[1]=(1 if x>0 else -1)*.515
    for y in [-2,2]:
        box('Celni sklo',(0,y,1.15),(w,.02,2),glass)
        beam('Hreben',(0,-2,3),(0,2,3),.06,dark)
    for x in [-.5,.5]: beam('Dvere',(x,-2.04,.2),(x,-2.04,2.1),.06,dark)
    beam('Dvere',(-.5,-2.04,2.1),(.5,-2.04,2.1),.06,dark)
    for x in [-1,1]:
        for y in [-1.4,-.4,.6,1.4]: pot(x,y,r=.23)

def shed(sauna=False):
    w=3; d=2.5
    box('Podesta',(0,0,.1),(w+.2,d+.2,.2),wood)
    for x in [-1.5,1.5]: box('Stena',(x,0,1.25),(.12,d,2.3),wood)
    for y in [-1.25,1.25]: slats(0,y,1.25,w,2.3,cedar if sauna else wood)
    box('Strecha',(0,0,2.47),(3.3,2.8,.14),dark)
    box('Dvere',(0,-1.31,1.15),(.9,.05,2.1),glass if sauna else dark)
    box('Madlo',(.32,-1.38,1.1),(.035,.05,.35),steel)
    if sauna:
        cyl('Komin',(1,.5,2.9),.1,1,dark)
        box('Panoramaticke okno',(-1.506,.1,1.4),(.025,1.6,1.3),glass)
        deck(3.2,1,y=-1.85)

def tub():
    cyl('Dno',(0,0,.15),1.12,.2,wood,48)
    for i in range(48):
        a=i*math.tau/48
        box('Drevena duzina',(1.05*math.cos(a),1.05*math.sin(a),.65),(.13,.09,1.05),wood,a+math.pi/2)
    cyl('Hladina',(0,0,1),.99,.025,water,48)
    for z in [.35,.9]:
        bpy.ops.mesh.primitive_torus_add(major_radius=1.075,minor_radius=.025,major_segments=48,minor_segments=6,location=(0,0,z));finish(bpy.context.object,'Obruc',steel)
    for i in range(3): box('Schudek',(0,-1.7+i*.22,.12+i*.13),(.8,.3,.22+i*.26),wood)
    cyl('Kamna',(1.45,.25,.5),.24,.9,dark)
    cyl('Kourovod',(1.45,.25,1.7),.065,1.6,dark)

def pool():
    box('Vana',(0,0,.5),(4,2.5,1),dark)
    box('Voda',(0,0,1.01),(3.76,2.26,.03),water)
    for y in [-1.25,1.25]:box('Lem',(0,y,1.04),(4.25,.23,.15),wood)
    for x in [-2,2]: box('Lem',(x,0,1.04),(.23,2.5,.15),wood)
    for y in [-.3,.3]: beam('Zebrik',(-2.2,y,.1),(-2.2,y,1.5),.05,steel)
    for z in [.3,.6,.9,1.2]:beam('Pricel',(-2.2,-.3,z),(-2.2,.3,z),.04,steel)

def kitchen():
    box('Korpus',(0,0,.48),(3,.7,.95),dark)
    box('Deska',(0,0,.99),(3.12,.8,.09),stone)
    for x in [-1,-.4,.4,1]:
        box('Dvirka',(x,-.36,.5),(.51,.04,.82),wood)
        box('Madlo',(x,-.4,.75),(.25,.03,.025),steel)
    box('Gril',(-.8,0,1.08),(.9,.55,.1),dark)
    for i in range(10):box('Rost',(-1.19+i*.085,0,1.15),(.02,.48,.02),steel)
    box('Drez',(.85,0,1.045),(.55,.4,.025),steel)
    beam('Baterie',(.85,.26,1),(.85,.26,1.4),.035,steel)
    beam('Baterie',(.85,.26,1.4),(.85,0,1.4),.035,steel)

def dining():
    box('Stul',(0,0,.78),(2,.9,.09),wood)
    for x in [-.8,.8]:
        for y in [-.3,.3]:box('Noha stolu',(x,y,.38),(.065,.065,.76),dark)
    for x in [-.6,.6]:
        chair(x,1);chair(x,-1,math.pi)
    pot(0,0,.83,.1)

def lounge():
    for x in [-.85,.85]:
        box('Lehatko',(x,0,.35),(.73,1.9,.13),wood)
        box('Matrace',(x,-.2,.46),(.65,1.35,.12),linen)
        o=box('Operadlo',(x,.7,.66),(.65,.65,.12),linen);o.rotation_euler[0]=.4
        for y in [-.65,.65]:box('Podnoz',(x,y,.17),(.62,.07,.34),dark)
    cyl('Slunecnik',(2,.6,1.3),.035,2.6,dark)
    bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=1.5,radius2=.05,depth=.4,location=(2,.6,2.65));finish(bpy.context.object,'Platno',linen)

def swing():
    for x in [-1.5,1.5]:
        for y in [-.8,.8]:beam('Stojna',(x,y,0),(x,0,2.5),.12,wood)
    beam('Horni tram',(-1.7,0,2.5),(1.7,0,2.5),.15,wood)
    for x in [-.75,.75]:
        for y in [-.2,.2]:beam('Lano',(x,y,.6),(x,0,2.5),.018,linen)
    box('Lavice',(0,0,.55),(1.7,.6,.12),wood)
    box('Operadlo',(0,.3,.9),(1.7,.08,.7),wood)

def bikes():
    box('Zaklad stojanu',(0,0,.06),(2.5,.65,.12),steel)
    for x in [-.9,-.3,.3,.9]:
        for y in [-.2,.2]:beam('Stojan',(x,y,.1),(x,y,.75),.04,dark)
        beam('Stojan',(x,-.2,.75),(x,.2,.75),.04,dark)

def compost():
    for x in [-1,0,1]:
        for y in [-.5,.5]:box('Sloupek',(x,y,.5),(.08,.08,1),wood)
    for z in [.1,.28,.46,.64,.82]:
        for y in [-.5,.5]:box('Prkno',(0,y,z),(2,.07,.14),wood)
        for x in [-1,0,1]:box('Prkno',(x,0,z),(.07,1,.14),wood)
    box('Kompost',(0,0,.25),(1.85,.85,.48),soil)

def barrel():
    cyl('Nadrz',(0,0,.65),.5,1.2,dark,32)
    for i in range(28):
        a=i*math.tau/28;box('Obklad',(.5*math.cos(a),.5*math.sin(a),.65),(.1,.035,1.18),wood,a+math.pi/2)
    cyl('Viko',(0,0,1.28),.53,.06,dark,32)
    beam('Kohout',(0,-.5,.25),(0,-.65,.25),.05,steel)
    beam('Svody',(.45,.2,1.2),(.45,.2,2),.07,dark)

def beds():
    for x in [-1.1,1.1]:
        for y in [-1,1]:
            box('Zahon',(x,y,.28),(1.6,1.25,.56),corten)
            box('Puda',(x,y,.57),(1.5,1.15,.025),soil)
            for dx in [-.45,0,.45]:
                for dy in [-.32,.32]:sphere('Zelenina',(x+dx,y+dy,.7),(.19,.19,.19),leaf,2)

def canopy():
    for x in [-2,2]:
        for y in [-1.5,1.5]:box('Sloup',(x,y,1.4),(.12,.12,2.8),dark)
    for y in [-1.5,1.5]:box('Vaznik',(0,y,2.8),(4.4,.12,.15),dark)
    for x in [-1.65,-.55,.55,1.65]:
        for y in [-.86,.86]:solar_panel(x,y,2.93)
    box('Bateriova skrin',(1.65,1.15,.65),(.55,.45,1.3),linen)
    box('Displej',(1.65,.91,.95),(.25,.02,.13),dark)

def lights():
    for x in [-1.5,-.5,.5,1.5]:
        cyl('Sloupek svetla',(x,0,.4),.06,.8,dark)
        cyl('Difuzor',(x,0,.77),.075,.12,glow)
        cyl('Striska',(x,0,.86),.13,.05,dark)

CATALOG=[
 ('studio','Studio Solar','Domky','Kompaktní domek s terasou a střešními panely.',lambda:house('studio')),
 ('panorama','Panorama','Domky','Široké čelní prosklení a krytá pobytová terasa.',lambda:house('panorama')),
 ('nordic','Nordic Loft','Domky','Sedlová střecha, dřevěný obklad a komín.',lambda:house('nordic')),
 ('pavilion','Zahradní pavilon','Domky','Prosklený zahradní prostor s dřevěnými žebry.',lambda:house('pavilion')),
 ('pergola','Pergola Lounge','Odpočinek','Lamely, posezení a řetěz teplých světel.',pergola),
 ('greenhouse','Skleník Atelier','Pěstování','Prosklený skleník s antracitovými profily.',greenhouse),
 ('shed','Zahradní sklad','Vybavení','Dřevěný domek pro nářadí a sezónní vybavení.',shed),
 ('sauna','Sauna Cedar','Wellness','Zahradní sauna s teráskou a prosklenými dveřmi.',lambda:shed(True)),
 ('tub','Koupací sud','Wellness','Dřevěný sud s venkovními kamny a schůdky.',tub),
 ('pool','Ochlazovací bazén','Wellness','Kompaktní bazén s dřevěným lemem a žebříkem.',pool),
 ('kitchen','Venkovní kuchyň','Odpočinek','Gril, pracovní plocha a dřez v jedné sestavě.',kitchen),
 ('dining','Jídelní sestava','Odpočinek','Dřevěný stůl a čtyři čalouněná křesla.',dining),
 ('lounge','Lehátka a slunečník','Odpočinek','Dvojice lehátek s přírodním čalouněním.',lounge),
 ('swing','Zahradní houpačka','Odpočinek','Dřevěná závěsná lavice pro dva.',swing),
 ('bikes','Stojan na kola','Vybavení','Čtyři místa pro odložení jízdních kol.',bikes),
 ('compost','Dvoukomorový kompostér','Pěstování','Provětrávaná dřevěná sestava pro zahradní kompost.',compost),
 ('barrel','Nádrž na dešťovku','Technologie','Nadzemní nádrž s dřevěným obkladem a kohoutem.',barrel),
 ('beds','Cortenové záhony','Pěstování','Čtyři samostatné záhony s osázením.',beds),
 ('canopy','Solární přístřešek','Technologie','Přístřešek s osmi panely a bateriovou skříní.',canopy),
 ('lights','Osvětlení cesty','Technologie','Čtveřice nízkých světel s teplými difuzory.',lights),
]

def export_asset(entry):
    ident,title,category,desc,fn=entry
    setup();fn()
    # Join per material: each GLB keeps a small number of draw calls.
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    bounds=[o.matrix_world @ Vector(v) for o in meshes for v in o.bound_box]
    low=Vector(tuple(min(v[i] for v in bounds) for i in range(3)))
    high=Vector(tuple(max(v[i] for v in bounds) for i in range(3)))
    for m in list(bpy.data.materials):
        group=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.materials[0]==m]
        if not group:continue
        bpy.ops.object.select_all(action='DESELECT')
        for o in group:o.select_set(True)
        bpy.context.view_layer.objects.active=group[0]
        bpy.ops.object.join();bpy.context.object.name=f'{ident}_{m.name}'
    bpy.ops.object.select_all(action='SELECT')
    path=ROOT/'public/models/expanded'/f'{ident}.glb'
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=False,export_yup=True)
    triangles=sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH')
    if not args.no_render:
        center=(low+high)*.5;size=max(high-low)
        ground=material('Studio background',(.065,.095,.077),.9)
        box('Pouze render / podlozka',(center.x,center.y,low.z-.09),(200,200,.12),ground)
        scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False
        scene.render.resolution_x=480;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.world.color=(.24,.24,.24)
        for pos,power,diam in [((2,-4,7),1700,6),((-4,-1,4),1000,5),((1,4,5),2100,4)]:
            bpy.ops.object.light_add(type='AREA',location=center+Vector(pos)*max(1,size/5))
            l=bpy.context.object;l.data.energy=power*max(1,size/5)**2;l.data.shape='DISK';l.data.size=diam
            l.rotation_euler=(center-l.location).to_track_quat('-Z','Y').to_euler()
        bpy.ops.object.camera_add(location=center+Vector((1.1,-1.5,.95))*size)
        cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.48;scene.camera=cam
        scene.view_settings.view_transform='AgX'
        scene.render.image_settings.file_format='PNG';scene.render.filepath=str(ROOT/'work/catalog-renders'/f'{ident}.png')
        bpy.ops.render.render(write_still=True)
    return {'id':ident,'name':title,'category':category,'description':desc,'model':f'models/expanded/{ident}.glb','thumbnail':f'images/options/{ident}.webp','priceCzk':None,'status':'concept','sizeBytes':path.stat().st_size,'dimensionsMeters':{'x':round(high.x-low.x,3),'y':round(high.z-low.z,3),'z':round(high.y-low.y,3)},'meshFaces':triangles}

for folder in ['public/models/expanded','work/catalog-renders','docs']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
results=[]
for item in CATALOG:
    if args.only and item[0]!=args.only:continue
    results.append(export_asset(item));print('ASSET_DONE',item[0],flush=True)
if not args.only:
    (ROOT/'docs/expanded-assets.json').write_text(json.dumps({'version':1,'units':'meters','upAxis':'Y','license':'Original procedural models created for this project.','items':results},ensure_ascii=False,indent=2))
