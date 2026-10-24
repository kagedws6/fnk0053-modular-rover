"""Generate watertight fit gauges. Dependencies: shapely, trimesh, mapbox-earcut, manifold3d, networkx."""
from pathlib import Path
import json
import trimesh
from shapely.geometry import Point,LineString,box
from shapely import set_precision
from shapely.ops import unary_union

OUT=Path(__file__).resolve().parent
FONT={
 '0':['111','101','101','101','111'],
 '1':['010','110','010','010','111'],
 '2':['111','001','111','100','111'],
 '3':['111','001','111','001','111'],
 '4':['101','101','111','001','001'],
 '6':['111','100','111','101','111'],
 '8':['111','101','111','101','111'],
 '.':['0','0','0','0','1'],
 'M':['10001','11011','10101','10101','10101'],
 'F':['111','100','110','100','100'],
 'I':['111','010','010','010','111'],
 'T':['111','010','010','010','010'],
 ' ':['0','0','0','0','0']}
def text_shape(text,cx,cy,pixel=0.65):
 widths=[len(FONT[c][0]) for c in text]; width=(sum(widths)+len(text)-1)*pixel
 x=cx-width/2; cells=[]
 for c,w in zip(text,widths):
  for row,line in enumerate(FONT[c]):
   for col,ch in enumerate(line):
    if ch=='1': cells.append(box(x+col*pixel,cy+(1.5-row)*pixel,x+(col+1)*pixel,cy+(2.5-row)*pixel))
  x+=(w+1)*pixel
 return set_precision(unary_union([c.buffer(0.025,join_style=2) for c in cells]),0.0001).simplify(0.00001)
def rounded(l,w,r):
 return box(-l/2+r,-w/2+r,l/2-r,w/2-r).buffer(r,quad_segs=16)
def extrude(p,height,z=0):
 p=set_precision(p,0.00001).simplify(0.000001)
 m=trimesh.creation.extrude_polygon(p,height,engine='earcut');m.apply_translation([0,0,z]);return m
def export(name,base,markings):
 solids=[extrude(base,2)]
 for p in (markings.geoms if hasattr(markings,'geoms') else [markings]):
  if p.area>0:solids.append(extrude(p,0.5,1.9))
 
 mesh=trimesh.boolean.union(solids,engine='manifold')
 mesh.merge_vertices();mesh.remove_unreferenced_vertices()
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 assert len(mesh.split())==1
 path=OUT/(name+'.stl');mesh.export(path)
 loaded=trimesh.load_mesh(path)
 assert loaded.is_watertight and loaded.is_winding_consistent and len(loaded.split())==1
 return dict(file=path.name,dimensions_mm=loaded.extents.round(4).tolist(),triangles=len(loaded.faces),watertight=bool(loaded.is_watertight),volume_mm3=round(loaded.volume,2))

base=rounded(64,28,3).difference(Point(-22,0).buffer(1.8,quad_segs=24)).difference(LineString([(-14,0),(14,0)]).buffer(1.8,quad_segs=24))
marks=[text_shape('M3 FIT',0,8,0.65),text_shape('0',-22,-10,0.6)]
for distance in range(8,37,2):
 x=-22+distance
 marks.append(box(x-0.3,-6 if distance%10==0 else -5,x+0.3,-3.3))
for distance in [10,20,30]: marks.append(text_shape(str(distance),-22+distance,-10,0.6))
marks=unary_union(marks)
assert base.covers(marks)
report=[export('motor-bracket-spacing-gauge',base,marks)]
base=rounded(56,24,3)
marks=[]
for x,d,label in [(-17,3.2,'3.2'),(0,3.4,'3.4'),(17,3.6,'3.6')]:
 base=base.difference(Point(x,2).buffer(d/2,quad_segs=24));marks.append(text_shape(label,x,-6,0.65))
marks=unary_union(marks);assert base.covers(marks)
report.append(export('m3-clearance-sample',base,marks))
(OUT/'mesh-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(report,indent=2))
