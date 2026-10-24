"""Generate lightweight concept mesh and preview fragment; no external packages."""
import json, math
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

add('Reinforced lower frame','frame',0,ring(238,132,13,12,46,8)+box(-10,0,50,8,108,8)+box(10,0,50,8,108,8),'Proposed 238 x 132 mm frame; open motor pockets. Board and bracket mounting details pending.')
for x in [-62,62]:
    for y in [-43,43]:
        add('Motor bracket support tab','frame',0,plate(x,y,46,24,22,8,3),'Provisional support position; original metal brackets retained. Mounting holes await dimensions.')
for x,label in [(-115,'Rear'),(115,'Front')]:
    add(label+' replaceable bumper','mount',0,plate(x,0,44,14,132,12,5),'Separate replaceable bumper concept; attachment joint still to be designed.')
for x in [-62,62]:
    for y in [-83,83]:
        add('Original wheel','wheel',0,cylinder(x,y,32.5,32.5,27,'y',40),'Estimated 65 mm diameter, 27 mm width; wheelbase assumed 124 mm.')
        add('Wheel hub','hub',0,cylinder(x,y+(-13.7 if y<0 else 13.7),32.5,22,1.0,'y',28),'Stock wheel envelope, simplified hub.')
        # Tread strips on outer circumference.
        f=[]
        for a in range(0,360,20):
            t=math.radians(a);dt=0.032
            f.append([[x+32.8*math.cos(t+d),y+yy,32.5+32.8*math.sin(t+d)] for d,yy in [(-dt,-12),(dt,-12),(dt,12),(-dt,12)]])
        add('Tire tread','tread',0,f,'Simplified stock tire tread.')
for x in [-49,49]:
    for y in [-47,47]:
        add('Original gearmotor','hub',0,box(x,y,32.5,58,22,20),'Motor housing envelope; shaft and bracket details unverified.')
add('Freenove electronics shield','board',0.25,plate(0,0,56,210,124,2,5),'Simplified 210 x 124 mm envelope; actual board outline and mounting holes remain unverified.')
add('Rear battery bay','stock',0.25,plate(-82,0,58,38,80,21,3),'Existing holder retained; rear area stays open for battery access.')
for y in [-23,0,23]:
    add('Battery bay opening','screen',0.25,box(-82,y,79.2,31,15,0.4),'Open rear battery access, schematic representation.')
for x in [-40,40]:
    for y in [-48,48]:
        add('Deck standoff','metal',0.5,cylinder(x,y,73,3,30),'Concept supports only; mounting points pending confirmation.')
add('Removable accessory deck','frame',1,plate(0,0,88,112,120,4,10),'112 x 120 x 4 mm proposed deck, with a 12 mm accessory grid and ribbon opening in CAD.')
# Surface hole markers in the visualization; CAD contains true cut-through holes.
f=[]
for x in range(-42,43,12):
    for y in range(-48,49,12):
        f.append([[x+1.7*math.cos(a*math.pi/6),y+1.7*math.sin(a*math.pi/6),92.15] for a in range(12)])
add('Deck accessory hole grid','hole',1,f,'Proposed M3 clearance holes on a 12 mm grid; shown as surface markers in this preview.')
f=[]
for x in range(-96,97,12):
    for y in [-60,60]:
        f.append([[x+1.7*math.cos(a*math.pi/6),y+1.7*math.sin(a*math.pi/6),54.15] for a in range(12)])
add('Side accessory mounting row','hole',0,f,'Proposed M3 clearance row for future adapter plates.')
add('Removable audio adapter','mount',1.5,cylinder(-6,-13,97.5,39,3),'Separate adapter; board-specific holes and microphone clearances pending.')
add('Waveshare audio stack','audio',2,cylinder(-6,-13,108,35,12),'ESP32-S3-AUDIO-Board assembly; 70 mm diameter is an unverified envelope.')
add('Audio top plate','metal',2,cylinder(-6,-13,114.75,35,1.5),'Simplified top plate from photos. Microphone and connector openings are not modeled.')
add('Separate audio battery','battery',1,plate(-10,44,92,64,22,9,3),'Provisional 64 x 22 x 9 mm envelope; final cradle needs measured battery dimensions.')
add('Separate speaker','stock',1,plate(37,42,92,24,24,8,3),'Existing small speaker retained; mount and acoustic openings pending.')
add('Speaker cone','metal',1,cylinder(37,42,100.2,8,0.4),'Speaker face, simplified.')
add('Existing pan and tilt servos','stock',0.5,plate(78,0,65,25,30,32,3),'Reuse existing head mechanism; motion sweep and cable clearance require checking.')
add('Replaceable head adapter','frame',1,plate(82,0,98,30,45,5,4),'Front adapter can be replaced when a future face is added.')
add('Camera and expression head','stock',1,box(98.5,0,120,7,56,60),'Existing camera/display head represented by a simplified 56 x 60 mm face.')
add('Expression display','screen',1,box(102.2,0,129.5,0.4,48,25),'Existing expression display; face appearance is illustrative.')
for y0 in [-12,12]:
    f=[]
    for dy,dz in [(-5,-1),(-2,2),(1,4),(4,2),(7,-1)]:
        f+=box(102.6,y0+dy,129+dz,0.6,2.4,2.4)
    add('Expression pixels','mount',1,f,'Illustrative friendly expression on existing display.')
add('Camera','screen',1,cylinder(102.8,0,104,6,1.5,'x',24),'Front camera remains unobstructed; final head geometry will follow the existing parts.')
add('Line tracking module','board',0,plate(100,0,16,28,62,4,3),'Existing underside sensor envelope; adjustable support still to be designed.')
for y in [-22,0,22]:
    add('Line tracking sensor','stock',0,box(102,y,14,7,7,4),'Sensor height must be preserved and checked on the assembled rover.')

model=dict(revision='A',units='mm',status='Concept only -- dimensions and fit unverified',frame=[238,132],overall=[244,193,150],parts=parts)
raw=json.dumps(model,separators=(',',':'))
(ROOT/'concept-model.json').write_text(raw,encoding='utf-8',newline='\n')
template=(ROOT/'viewer-template.html').read_text(encoding='utf-8')
html=template.replace('/*MODEL_DATA*/',raw)
VIS.mkdir(parents=True,exist_ok=True)
(VIS/'rover-chassis-concept.html').write_text(html,encoding='utf-8',newline='\n')
assert '/*MODEL_DATA*/' not in html
assert len(html.encode())<1000000
print(json.dumps(dict(parts=len(parts),faces=sum(len(p['faces']) for p in parts),bytes=len(html.encode()),preview=str(VIS/'rover-chassis-concept.html'))))
