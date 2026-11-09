"""Deterministic, headless Blender architectural asset pipeline.
Coordinates supplied as x/y(up)/z, in metres. glTF export preserves this space.
Run: blender --background --python scripts/generate_assets.py
"""
import bpy, math, random, os
from mathutils import Vector
random.seed(42)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'public','models'); os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def linear(v): return ((v+0.055)/1.055)**2.4 if v>0.04045 else v/12.92
def mat(name,hex,rough=.6,metal=0,emission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    rgb=tuple(linear(int(hex[i:i+2],16)/255) for i in (0,2,4)); p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    if emission:
        key='Emission Color' if 'Emission Color' in p.inputs else 'Emission'
        p.inputs[key].default_value=(*rgb,1)
        if 'Emission Strength' in p.inputs: p.inputs['Emission Strength'].default_value=emission
    return m
wood=mat('Modřín – přírodní dřevo','B99768'); wood2=mat('Dřevo – tmavší lamely','8E7049'); cedar=mat('Červený cedr','A56B49')
bark=mat('Kůra ovocných stromů','67513A'); grass=mat('Travní sad','7E9760'); dirt=mat('Hrana půdního profilu','655746'); gravel=mat('Štěrkový příjezd','C9C5B6')
metal=mat('Antracitový falcovaný plech','293A37',.42,.7); glass=mat('Panoramatické zasklení','7BABA1',.13,.55); rubber=mat('Pneumatiky podvozku','232925'); steel=mat('Pozinkovaný podvozek','9FA6A1',.35,.8)
corten=mat('Corten #9A4624','9A4624',.75,.3); soil=mat('Zahradní substrát','403328'); solar=mat('Monokrystalické fotovoltaické články','243B4C',.25,.65)
warm=mat('Teplá světla oken a festonů','FFD195',.4,0,2); red=mat('Jablka','C66C42'); green=[mat('Listí %d'%i,h) for i,h in enumerate(['486644','648450','789658','8B9E64','57734B'])]

def pos(v): return (v[0],-v[2],v[1])
def cube(name,p,d,m,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos(p)); o=bpy.context.object; o.name=name; o.dimensions=(d[0],d[2],d[1]); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Jemně zaoblené hrany','BEVEL'); mod.width=bevel; mod.segments=2
        o.modifiers.new('Vážené normály','WEIGHTED_NORMAL')
    return o

def cyl(name,p,r,depth,m,vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=pos(p)); o=bpy.context.object; o.name=name; o.data.materials.append(m); return o

def beam(name,a,b,r,m):
    av,bv=Vector(pos(a)),Vector(pos(b)); delta=bv-av
    o=cyl(name,((a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2),r,delta.length,m)
    o.rotation_euler=delta.to_track_quat('Z','Y').to_euler(); return o

def ico(name,p,s,m,sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=pos(p)); o=bpy.context.object; o.name=name; o.scale=(s[0],s[2],s[1]); o.data.materials.append(m)
    for f in o.data.polygons: f.use_smooth=True
    return o

def export(name,fn):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); fn()
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,name+'.glb'),export_format='GLB',export_apply=True,export_yup=True)
    print('EXPORTED',name)

def plot():
    cube('300 m² — 15 × 20 m',(0,-.42,0),(15,.8,20),dirt,.28); cube('Travnatá parcela',(0,0,0),(15,.12,20),grass,.18)
    cube('Štěrkové parkovací stání',(4.7,.09,7.3),(4,.08,4.8),gravel,.12)
    cube('Pěšina ze šlapáků',(-1,.09,5.6),(1.1,.09,5),gravel,.05)
    for side in [-1,1]:
        for z in range(-10,11,2): cyl('Akátový sloupek',(side*7.35,.72,z),.065,1.5,wood2)
        for h in [.32,.7,1.1,1.4]: beam('Lesnické pletivo',(side*7.35,h,-10),(side*7.35,h,10),.012,metal)
        for x in range(-7,8,2): cyl('Akátový sloupek',(x,.72,side*9.85),.065,1.5,wood2)
    for h in [.32,.7,1.1,1.4]:
        beam('Zadní pletivo',(-7.35,h,-9.85),(7.35,h,-9.85),.012,metal)
        beam('Přední pletivo',(-7.35,h,9.85),(2.4,h,9.85),.012,metal)
    for x in [2.4,7.25]: cube('Sloup GSM brány',(x,.85,9.85),(.15,1.7,.15),metal)
    for x in [2.6+i*.18 for i in range(25)]: cube('Lamela posuvné brány',(x,.8,9.85),(.08,1.25,.06),wood2)
    cube('GSM klávesnice',(2.4,1.3,9.72),(.13,.2,.07),steel,.015)
    cyl('Poklop vodoměrné šachty',(6,.09,5.7),.38,.08,metal,24)
    for i in range(220):
        x=random.uniform(-7.1,7.1); z=random.uniform(-9.7,9.7)
        if x>2.5 and z>4.8: continue
        ico('Drobný porost',(x,.09,z),(.035,.1,.035),random.choice(green))

def tree(x,z,mature=False,idx=0):
    h=2.8 if mature else 1.9; radius=1.05 if mature else .7
    cyl('Kmen jabloně',(x,h*.42,z),.12 if mature else .065,h*.85,bark)
    for k in range(5 if mature else 3):
        angle=k*2.4; bx=x+math.sin(angle)*.55; bz=z+math.cos(angle)*.55
        beam('Větve',(x,h*.55,z),(bx,h*.9,bz),.04,bark)
        ico('Organická koruna',(bx,h+random.uniform(-.2,.35),bz),(radius*.9,radius*.9,radius*.85),green[(idx+k)%5],2)
    if mature:
        for k in range(6):
            a=k*1.6; ico('Zralé jablko',(x+math.sin(a)*1.05,h+random.uniform(-.5,.1),z+math.cos(a)*1.05),(.07,.075,.07),red,1)
    cyl('Mulčovací kruh',(x,.09,z),.65,.04,dirt,24)

def orchard(mature):
    points=[(3,-6),(5,-2),(3,2),(-5,5)]
    if mature: points += [(5,5),(-5,-7),(-6.2,0),(0,7)]
    for i,(x,z) in enumerate(points): tree(x,z,mature,i)
    if mature:
        for z in [-7,-5,-3,0,2]: ico('Jedlé keře',(6.5,.5,z),(.5,.6,.55),green[2],2)

def house(kind):
    width=6.5 if kind!='anna' else 7.2; depth=3.1 if kind=='liberte' else 3.5; height=2.7
    cube('Vlemmix pozinkovaný rám',(0,.45,0),(width+.25,.22,depth),steel,.03)
    for x in [-1.1,.1]:
        for z in [-depth/2,depth/2]:
            o=cyl('Kolo homologovaného přívěsu',(x,.38,z),.4,.2,rubber,24); o.rotation_euler[0]=math.pi/2
            o=cyl('Hliníkový disk',(x,.38,z*1.01),.21,.22,steel,16); o.rotation_euler[0]=math.pi/2
    beam('Oj Vlemmix',(width/2,.42,-1),(width/2+1.5,.42,0),.085,steel); beam('Oj Vlemmix',(width/2,.42,1),(width/2+1.5,.42,0),.085,steel)
    cube('Držák registrační značky',(-width/2-.13,.48,0),(.05,.2,.5),metal)
    for x in [-width/2+.3,width/2-.3]:
        for z in [-depth/2+.2,depth/2-.2]: cyl('Stabilizační podpěra',(x,.24,z),.045,.45,steel)
    body=cedar if kind=='baluchon' else wood
    cube('Izolovaný plášť',(0,1.98,0),(width,2.8,depth),body,.025)
    # Fine, individually modelled vertical cladding.
    for x in [-width/2+.06+i*.145 for i in range(int(width/.145))]:
        for z in [-depth/2-.025,depth/2+.025]: cube('Svislé modřínové palubky',(x,1.99,z),(.126,2.78,.065),body if int(x*100)%3 else wood2,.008)
    for z in [-depth/2+i*.14 for i in range(int(depth/.14))]:
        for x in [-width/2-.015,width/2+.015]: cube('Boční obklad',(x,1.98,z),(.06,2.78,.12),body,.006)
    if kind=='anna':
        cube('Posuvný prosklený plášť',(0,1.92,depth/2+.075),(width-.2,2.55,.06),glass)
        for x in [-width/2+i*.45 for i in range(int(width/.45)+1)]:
            cube('Biofilní žebro',(x,1.95,depth/2+.16),(.07,2.85,.12),wood2)
        cube('Dubová podlaha',(0,.65,0),(width,.12,depth),wood)
    else:
        glazing=4 if kind=='millhome' else 2.65
        cube('Francouzská panoramatická okna',(-.7,1.95,depth/2+.075),(glazing,2.35,.08),metal,.02)
        cube('Dvojsklo',(-.7,1.95,depth/2+.13),(glazing-.14,2.2,.045),glass)
        for x in [-.7-glazing/2,-.7,-.7+glazing/2]: cube('Rám francouzských dveří',(x,1.95,depth/2+.17),(.065,2.35,.07),metal)
        cube('Interiérové teplé světlo',(-.7,2.9,depth/2+.17),(glazing-.2,.035,.04),warm)
        if kind=='millhome':
            cube('Rohové panoramatické okno',(-width/2-.07,1.95,.7),(.08,2.35,1.8),glass)
            cube('Spací loft',(-width/2-.1,2.7,.7),(.1,.1,1.8),wood)
        cube('Boční koupelnové okno',(width/2+.07,2.35,0),(.08,.65,1.1),glass)
    roof=cube('Asymetrická střecha' if kind=='millhome' else 'Falcovaná střecha',(0,3.48,0),(width+.3,.17,depth+.3),metal,.025)
    if kind=='millhome': roof.rotation_euler[0]=.12
    for x in [-width/2+i*.32 for i in range(int(width/.32)+1)]: cube('Stojatá drážka',(x,3.59,0),(.02,.04,depth+.2),metal)
    # Integrated small solar starter array; off-grid upgrade is separate.
    for x in [-1.5,0,1.5]:
        cube('Solární modul',(x,3.64,-.15),(1.35,.055,2),solar,.02)
        for k in range(4): cube('Sběrnice panelu',(x-.5+k*.33,3.675,-.15),(.012,.005,1.95),steel)
    if kind=='baluchon': cyl('Komín krbových kamen',(2.1,3.88,-.65),.11,1.1,metal,20)

def terrace():
    for x in [-5,-2,1]:
        for z in [-1,2]: cyl('Zemní vrut',(x,.2,z),.055,.6,steel)
    for i in range(40): cube('Modřínové terasové prkno',(-2.7,.36,-.5+i*.125),(6,.14,.115),wood if i%4 else wood2,.012)
    cube('Schod terasy',(-2.7,.15,4.8),(2,.2,.5),wood,.02)
    for x in [-4.4,-3.3]:
        cube('Zahradní křeslo',(x,.8,2.9),(.72,.14,.7),wood2,.04); cube('Opěradlo',(x,1.15,2.65),(.72,.6,.1),wood2,.03)
        for xx in [-.27,.27]:
            for zz in [-.25,.25]: cube('Noha křesla',(x+xx,.57,2.9+zz),(.055,.5,.055),metal)
    cyl('Venkovní stolek',(-3.85,.8,3.9),.35,.08,wood,24); cyl('Podnož stolku',(-3.85,.5,3.9),.05,.6,metal)

def beds():
    for z in [0,2.2]:
        for x in [3.5,5.4]:
            cube('Corten vyvýšený záhon',(x,.4,z),(1.45,.65,1.7),corten,.035); cube('Substrát',(x,.74,z),(1.33,.06,1.58),soil)
            for k in range(8): ico('Zelenina',(x+random.uniform(-.5,.5),.87,z+random.uniform(-.6,.6)),(.15,.18,.14),random.choice(green))

def pergola():
    for x in [-5,-1]:
        for z in [4.2,7.5]: cube('Sloup pergoly',(x,1.4,z),(.14,2.8,.14),wood2)
    for z in [4.2,7.5]: cube('Nosník pergoly',(-3,2.82,z),(4.35,.2,.16),wood2)
    for x in [-5+i*.4 for i in range(11)]: cube('Stínicí lamely pergoly',(x,2.98,5.85),(.08,.18,3.7),wood)
    for k in range(12):
        x=-5+k*4/11; h=2.7-.4*math.sin(k/11*math.pi)
        ico('Emisivní žárovka festonu',(x,h,5.8),(.055,.08,.055),warm,2)
        if k: beam('Kabel festonu',(x-4/11,2.7-.4*math.sin((k-1)/11*math.pi),5.8),(x,h,5.8),.012,metal)
    cyl('Kruhové ohniště',(-3,.32,5.8),.65,.35,corten,32); cyl('Uhlíky',(-3,.51,5.8),.53,.05,soil,24)
    for z in [4.7,7]: cube('Dřevěné posezení',(-3,.55,z),(2.5,.18,.4),wood,.03)

def tech(solar_enabled=True,water_enabled=True):
    if solar_enabled: cube('Victron Energy bateriový kabinet',(-5.7,.8,-4),(.7,1.5,.65),metal,.06)
    if solar_enabled: cube('Victron modrý regulátor',(-5.7,1.06,-3.66),(.45,.5,.04),solar,.025)
    if water_enabled: cyl('Retenční nádrž – servisní poklop',(5,.09,7),.45,.12,metal,32)
    for x in ([-4.2,-2.7,-1.2] if solar_enabled else []): cube('Off-grid panel 3 kWp',(x,3.83,-4.4),(1.4,.055,2.6),solar,.02)

def all_addons(): terrace(); beds(); pergola(); tech()
export('solar_tech',lambda:tech(True,False))
export('water_tech',lambda:tech(False,True))
export('plot_base',plot)
export('orchard_standard',lambda:orchard(False)); export('orchard_trees',lambda:orchard(True))
for kind in ['liberte','millhome','baluchon','anna']: export('tiny_'+kind,lambda k=kind:house(k))
for name,fn in [('terrace',terrace),('corten_beds',beds),('firepit_pergola',pergola),('offgrid_tech',tech),('addons',all_addons)]: export(name,fn)
print('All assets generated in',OUT)
