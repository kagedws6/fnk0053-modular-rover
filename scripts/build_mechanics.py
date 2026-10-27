"""Build revision B experimental frame/deck and the fixed 8 mm fit coupon."""
from pathlib import Path
import sys,json,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import trimesh
from mechanical_layout import *

OUT=ROOT/'experimental';OUT.mkdir(exist_ok=True)
GENERATED=ROOT/'generated';GENERATED.mkdir(exist_ok=True)
FIT=ROOT/'fit-checks'
def profile_scad(name,p):
 modules=[]
 for polygon in polygons(p):
  rings=[list(polygon.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in polygon.interiors]
  points=[];paths=[]
  for ring in rings:
   start=len(points);points += [[round(x,5),round(y,5)] for x,y in ring];paths.append(list(range(start,len(points))))
  modules.append('polygon(points='+json.dumps(points,separators=(',',':'))+',paths='+json.dumps(paths,separators=(',',':'))+');')
 return 'module '+name+'(){union(){'+''.join(modules)+'}}\n'
scad='// Generated from mechanical_layout.py; units mm. Do not hand edit.\n'
for name,p in [('frame_profile',FRAME),('deck_profile',DECK),('board_profile',BOARD)]:scad+=profile_scad(name,p)
scad+='bracket_holes='+json.dumps(BRACKET_HOLES)+';\nboard_posts='+json.dumps(BOARD_POSTS)+';\nsensor_posts='+json.dumps(SENSOR_POSTS)+';\n'
scad+='wheel_envelopes='+json.dumps([[w['center'],w['size'][1]] for w in D['wheels']])+';\n'
scad+='motor_envelopes='+json.dumps([[w['center'],w['size']] for w in D['motors']])+';\n'
scad+='bracket_pairs='+json.dumps([b['holes'] for b in D['brackets']])+';\n'
scad+='sensor_envelope='+json.dumps([D['sensor']['center'],D['sensor']['size']])+';\n'
(GENERATED/'profiles-b.scad').write_text(scad,encoding='utf-8',newline='\n')

frame=extrude(FRAME,4)
solids=[frame]+[extrude(p,6.7,4) for p in BOSSES]
frame=trimesh.boolean.union(solids,engine='manifold')
# Recess long board-support screw heads flush with the frame underside.
recess=extrude(holes(BOARD_POSTS,6.4),2.41,-.01)
frame=trimesh.boolean.difference([frame,recess],engine='manifold')
deck=extrude(DECK,4)
coupon=rounded(26,20,3).difference(holes([(-4,0),(4,0)],3.4))
coupon_mesh=extrude(coupon,2)
reports=[]
for path,mesh in [(OUT/'frame-b-experimental.stl',frame),(OUT/'deck-b-experimental.stl',deck),(FIT/'motor-bracket-8mm-fit.stl',coupon_mesh)]:
 mesh.merge_vertices();mesh.remove_unreferenced_vertices()
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and len(mesh.split())==1
 mesh.export(path);check=trimesh.load_mesh(path)
 assert check.is_watertight and check.is_winding_consistent and len(check.split())==1
 reports.append({'file':path.relative_to(ROOT).as_posix(),'watertight':True,'connected_components':1,'dimensions_mm':check.extents.round(4).tolist(),'volume_mm3':round(check.volume,2),'triangles':len(check.faces)})

# These are conservative tire bounding-box checks, not a full assembly collision analysis.
checks=[]
for i,w in enumerate(D['wheels']):
 tire=box(w['min'][0],w['min'][1],w['max'][0],w['max'][1])
 overlap=FRAME_BLANK.intersection(tire).area
 distance=FRAME_BLANK.distance(tire)
 assert overlap<1e-7 and distance>=D['clearance']-1e-5
 checks.append({'wheel':i,'frame_plan_clearance_mm':round(distance,4),'overlap_mm2':round(overlap,6)})
for b in D['brackets']:
 assert abs(math.dist(*b['holes'])-8)<.001
 for hole in b['holes']:assert FRAME_BLANK.contains(Point(*hole).buffer(3.2))
assert FRAME_BLANK.is_valid and len(polygons(FRAME_BLANK))==1
assert FRAME_BLANK.bounds[2]-FRAME_BLANK.bounds[0]<=244.001
assert len(BRACKET_HOLES)==8
servo_clearance=FRAME_BLANK.distance(PAN_SERVO)
assert servo_clearance>=1.999
report={'revision':'B','mesh_checks':reports,'tire_envelope_checks':checks,'pan_servo_plan_clearance_mm':round(servo_clearance,4),'bracket_spacing_mm':8,'physical_fit_verified':False,'limits':['No full assembly collision, head sweep, cable routing, strength or slicer validation.','Audio hardware dimensions remain estimates.','Experimental frame/deck require physical fit and fastener checks.']}
(OUT/'validation-b.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(report,indent=2))
