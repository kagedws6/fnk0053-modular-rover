"""Generate revision B preview from shared mechanical profiles and measured kit positions."""
import json, math
from mechanical_layout import D,FRAME_BLANK,BOARD,DECK_BLANK,RIBBON,BRACKET_HOLES,BOARD_POSTS,SENSOR_POSTS,ACCESSORY_HOLES,DECK_ACCESSORY,extrude
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIS = ROOT / 'preview'
parts = []

def add(name, category, level, faces, detail):
    parts.append(dict(name=name, category=category, level=level, faces=faces, detail=detail))

def box(cx,cy,cz,l,w,h):
    v=[[cx+sx*l/2,cy+sy*w/2,cz+sz*h/2] for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    return [[v[i] for i in f] for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]]

def outline(l,w,r):
    return [[cx+r*math.cos(a),cy+r*math.sin(a)] for cx,cy,a0 in [(l/2-r,w/2-r,0),(-l/2+r,w/2-r,90),(-l/2+r,-w/2+r,180),(l/2-r,-w/2+r,270)] for a in [math.radians(a0+j*90/6) for j in range(7)]]

def plate(cx,cy,z,l,w,h,r=5):
    p=outline(l,w,r); low=[[x+cx,y+cy,z] for x,y in p]; high=[[x+cx,y+cy,z+h] for x,y in p]
    return [low[::-1],high]+[[low[i],low[(i+1)%len(p)],high[(i+1)%len(p)],high[i]] for i in range(len(p))]

def cylinder(cx,cy,cz,r,h,axis='z',n=32):
    def v(a,t):
        u=r*math.cos(a);v=r*math.sin(a)
        return [cx+u,cy+v,cz+t] if axis=='z' else ([cx+u,cy+t,cz+v] if axis=='y' else [cx+t,cy+u,cz+v])
    low=[v(i*2*math.pi/n,-h/2) for i in range(n)]; high=[v(i*2*math.pi/n,h/2) for i in range(n)]
    return [low[::-1],high]+[[low[i],low[(i+1)%n],high[(i+1)%n],high[i]] for i in range(n)]

def ring(l,w,r,th,z,h):
    out=outline(l,w,r); inn=outline(l-2*th,w-2*th,max(2,r-th))
    f=[]
    for i in range(len(out)):
        j=(i+1)%len(out)
        o1,o2=out[i],out[j];i1,i2=inn[i],inn[j]
        for points in [ [(o1,z+h),(o2,z+h),(i2,z+h),(i1,z+h)],[(o2,z),(o1,z),(i1,z),(i2,z)],[(o1,z),(o2,z),(o2,z+h),(o1,z+h)],[(i2,z),(i1,z),(i1,z+h),(i2,z+h)] ]:
            f.append([[p[0],p[1],zz] for p,zz in points])
    return f

def planar_faces(p,h,z):
    return extrude(p,h,z).triangles.round(3).tolist()

add('Narrow-waist lower frame','frame',0,planar_faces(FRAME_BLANK,4,43.3),'Revision B: 244 x 132 mm maximum, 82 mm waist. Raised board leaves the motor loads on this carrier. Experimental; fit not verified.')
for x,y in BOARD_POSTS:
    add('PCB support boss','frame',0,cylinder(x,y,50.65,5,6.7),'New boss lifts the PCB bottom to 54 mm. Recessed underside screw head; fastener fit still needs checking.')
for b in D['brackets']:
    x=sum(p[0] for p in b['holes'])/2;y=sum(p[1] for p in b['holes'])/2
    add('Original metal motor bracket','metal',0,box(x,y,32.3,14,5,22),'14 x 22 x 5 mm bracket envelope. Its confirmed chassis screw centers are 8 mm apart.')
for x,sign in [(-116,-1),(116,1)]:
    f=plate(x+sign*8.5,0,43.3,5,132,12,2)
    for y in [-50,50]:f+=plate(x,y,47.3,16,14,4,2)
    add(('Rear' if sign<0 else 'Front')+' replaceable bumper','mount',0,f,'Separate bumper with two upper mounting flanges. The assembled frame/bumper length is 254 mm; joint hardware is not physically checked.')
for w in D['wheels']:
    x,y,z=w['center'];width=w['size'][1]
    add('Original wheel','wheel',0,cylinder(x,y,32.3,32.3,width,'y',40),'64.6 mm diameter and about 30 mm wide, positioned from the Freenove STEP. Total stock tire width is about 148.8 mm.')
    add('Wheel hub','hub',0,cylinder(x,y+(-1 if y<0 else 1)*(width/2+.15),32.3,22,.5,'y',28),'Simplified wheel hub; position follows the measured tire envelope.')
    f=[]
    for a in range(0,360,20):
        t=math.radians(a);dt=.03
        f.append([[x+32.4*math.cos(t+d),y+yy,32.3+32.4*math.sin(t+d)] for d,yy in [(-dt,-width/2),(dt,-width/2),(dt,width/2),(-dt,width/2)]])
    add('Tire tread','tread',0,f,'Illustrative tread on the measured wheel envelope.')
for m in D['motors']:
    add('Original gearmotor envelope','hub',0,box(*m['center'],*m['size']),'Measured conservative motor/shaft bounding box; its detailed shape is simplified in this preview.')
add('Freenove electronics shield','board',.25,planar_faces(BOARD,1.6,54),'233.31 x 120.34 x 1.6 mm envelope, raised 10.7 mm from stock. Wheel/servo cutouts are simplified packaging geometry, not the exact PCB perimeter.')
add('Open rear battery bay','stock',.25,plate(-81,0,55.6,42,80,21,3),'Rear battery access remains open. Holder envelope remains simplified.')
for x in [-91,-72]:
    add('Battery bay opening','screen',.25,box(x,0,76.8,14,67,.4),'Illustrative open battery slots; physical holder dimensions still require checking.')
for x,y in BOARD_POSTS:
    add('Original 28 mm deck standoff','metal',.5,cylinder(x,y,69.6,2.7,28),'Uses the stock deck hole pattern. Existing standoff height is retained above the raised PCB.')
add('Removable accessory deck','frame',1,planar_faces(DECK_BLANK.difference(RIBBON),4,83.6),'Proposed 110 x 120 x 4 mm deck. Four stock mounting positions plus a 12 mm accessory grid; rear battery bay stays open.')
def dots(points,z):
    return [[[x+1.7*math.cos(a*math.pi/6),y+1.7*math.sin(a*math.pi/6),z] for a in range(12)] for x,y in points]
add('Confirmed motor-bracket mounting pattern','hole',0,dots(BRACKET_HOLES,47.45),'Four measured pairs, each 8 mm center to center. Proposed printed clearance diameter is 3.4 mm.')
add('Lower accessory and sensor holes','hole',0,dots(ACCESSORY_HOLES+SENSOR_POSTS,47.45),'Accessory row is a proposed 12 mm interface. Sensor mounts retain the original underside elevation.')
add('Deck accessory grid','hole',1,dots(DECK_ACCESSORY+BOARD_POSTS,87.75),'Surface markers in preview; CAD/STLs contain true cut-through holes.')
add('Removable audio adapter','mount',1.5,cylinder(-6,-13,93.1,39,3),'Separate adapter envelope, not yet an exact audio-board mount.')
add('Waveshare audio stack','audio',2,cylinder(-6,-13,103.6,35,12),'Audio board diameter remains an unverified 70 mm envelope; microphone openings and connector geometry are pending.')
add('Audio top plate','metal',2,cylinder(-6,-13,110.35,35,1.5),'Simplified top plate of the existing voice assembly.')
add('Separate audio battery','battery',1,plate(-10,44,87.6,64,22,9,3),'Estimated battery envelope; not a verified cradle.')
add('Separate speaker','stock',1,plate(37,42,87.6,24,24,8,3),'Estimated speaker envelope; acoustic mount still needs design.')
add('Speaker cone','metal',1,cylinder(37,42,95.8,8,.4),'Illustrative speaker face.')
add('Existing pan servo','stock',.5,box(83.56,0,50.5,32.8,12,30.2),'Stock SG90 envelope, relocated with the raised PCB. Servo/board opening remains a fit-check item.')
for y in [-18,18]:
    add('Head support arm','frame',1,box(85,y,84,12,4,38),'Proposed replaceable head support; head sweep and ribbon routing have not been checked.')
add('Existing tilt servo','stock',1,box(89,0,88,25,12,30),'Simplified existing tilt stage; final adapter needs physical confirmation.')
add('Camera and expression head','stock',1,box(110,0,118.2,7,56,60),'Existing head simplified as a 56 x 60 mm face; its mounting and motion are not manufacturing geometry.')
add('Expression display','screen',1,box(113.7,0,127.7,.4,48,25),'Illustrative expression on the existing display.')
for y0 in [-12,12]:
    f=[]
    for dy,dz in [(-5,-1),(-2,2),(1,4),(4,2),(7,-1)]:f+=box(114.1,y0+dy,127.2+dz,.6,2.4,2.4)
    add('Expression pixels','mount',1,f,'Illustrative expression.')
add('Camera','screen',1,cylinder(114.3,0,102.2,6,1.5,'x',24),'Camera opening remains clear in the concept; physical head sweep is pending.')
sensor=D['sensor']
add('Line tracking module envelope','board',0,box(*sensor['center'],*sensor['size']),'Original measured sensor envelope and ground clearance retained. Carrier sits at the stock mounting elevation.')
for x,y in SENSOR_POSTS:
    add('Original sensor standoff','metal',0,cylinder(x,y,29.3,2.7,28),'28 mm stock sensor supports retained below the frame instead of the raised PCB.')

from cage_layout import assembly_meshes
for name,mesh in assembly_meshes():
    is_pad=name=='Cage mounting pads'
    add(name,'frame' if is_pad else 'cage',0 if is_pad else 2.5,mesh.triangles.round(3).tolist(),'Optional removable cage. Four dedicated base bolts release the complete assembly. Prototype; head sweep and impact resistance not verified.')
    parts[-1]['cage']=True

model=dict(revision='B+cage',units='mm',status='Measured kit packaging; experimental chassis; fit unverified',frame=[244,132],overall=[254,180,175],parts=parts)
raw=json.dumps(model,separators=(',',':'))
(ROOT/'concept-model.json').write_text(raw,encoding='utf-8',newline='\n')
template=(ROOT/'viewer-template.html').read_text(encoding='utf-8')
html=template.replace('/*MODEL_DATA*/',raw).replace('/*RENDERER*/',(ROOT/'scripts/preview-renderer.js').read_text(encoding='utf-8'))
VIS.mkdir(parents=True,exist_ok=True)
(VIS/'rover-chassis-concept.html').write_text(html,encoding='utf-8',newline='\n')
assert len(html.encode())<1000000
print(json.dumps(dict(revision='B',parts=len(parts),faces=sum(len(p['faces']) for p in parts),bytes=len(html.encode()))))
