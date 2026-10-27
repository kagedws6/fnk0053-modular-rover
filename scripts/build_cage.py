"""Generate removable cage prototypes, the matching carrier, and selected checks."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import trimesh
import numpy as np
from mechanical_layout import *
from cage_layout import *

OUT=ROOT/'experimental'/'cage';OUT.mkdir(parents=True,exist_ok=True)
frame=trimesh.boolean.union([extrude(CAGE_FRAME,4)]+[extrude(p,6.7,4) for p in BOSSES],engine='manifold')
frame=trimesh.boolean.difference([frame,extrude(holes(BOARD_POSTS,6.4),2.41,-.01)],engine='manifold')
meshes={'side-hoop-print-two.stl':side_flat(),'foot-print-four.stl':foot_flat(),'roof-crossbar-print-two.stl':roof_flat(),'frame-with-cage-mounts.stl':frame}
reports=[]
for name,mesh in meshes.items():
 mesh.merge_vertices();mesh.remove_unreferenced_vertices()
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and len(mesh.split())==1
 mesh.export(OUT/name);check=trimesh.load_mesh(OUT/name)
 assert check.is_watertight and check.is_winding_consistent and len(check.split())==1
 assert max(check.extents[:2])<=248.001
 reports.append({'file':name,'dimensions_mm':check.extents.round(4).tolist(),'watertight':True,'connected_components':1,'volume_mm3':round(check.volume,2)})

# Static bounding-envelope checks against the current preview's stock hardware.
parts=json.loads((ROOT/'concept-model.json').read_text())['parts']
envelopes=[]
for p in parts:
 if p['category'] in ['wheel','hub','board','stock','screen','audio','battery']:
  points=np.array([v for face in p['faces'] for v in face]);lo=points.min(axis=0);hi=points.max(axis=0)
  if np.prod(hi-lo)<.01:continue
  mesh=trimesh.creation.box(extents=hi-lo);mesh.apply_translation((lo+hi)/2);envelopes.append((p['name'],mesh))
cage=assembly_meshes();overlaps=[]
for name,mesh in cage:
 for other,obstacle in envelopes:
  if np.any(mesh.bounds[1]<=obstacle.bounds[0]+1e-5) or np.any(obstacle.bounds[1]<=mesh.bounds[0]+1e-5):continue
  intersect=trimesh.boolean.intersection([mesh,obstacle],engine='manifold')
  if intersect.is_empty:continue
  volume=abs(float(intersect.volume))
  assert np.isfinite(volume),(name,other,'nonfinite intersection')
  if volume>.01:overlaps.append({'cage_part':name,'component':other,'volume_mm3':round(volume,3)})
assert not overlaps,overlaps
for w in D['wheels']:
 tire=box(w['min'][0],w['min'][1],w['max'][0],w['max'][1]);assert CAGE_FRAME_BLANK.distance(tire)>3
assert CAGE_FRAME_BLANK.bounds[3]-CAGE_FRAME_BLANK.bounds[1]<=142.001

def module_profile(name,p):
 polygons=[p] if p.geom_type=='Polygon' else list(p.geoms);out='module '+name+'(){union(){'
 for poly in polygons:
  rings=[list(poly.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in poly.interiors];points=[];paths=[]
  for ring in rings:
   start=len(points);points += [[round(x,5),round(y,5)] for x,y in ring];paths.append(list(range(start,len(points))))
  out+='polygon(points='+json.dumps(points,separators=(',',':'))+',paths='+json.dumps(paths,separators=(',',':'))+');'
 return out+'}}\n'
scad='// Generated cage profiles, mm. Prototype only.\ncage_mounts='+json.dumps(MOUNTS)+';\n'
for name,p in [('cage_side_profile',SIDE_PROFILE),('cage_foot_profile',FOOT_PROFILE),('cage_roof_profile',ROOF_PROFILE),('cage_pad_profile',PAD_PROFILE)]:scad+=module_profile(name,p)
(ROOT/'generated'/'cage-profiles.scad').write_text(scad,encoding='utf-8',newline='\n')
report={'mesh_checks':reports,'static_hardware_envelope_overlaps':overlaps,'roof_crossbar_bottom_mm':169,'head_envelope_top_mm':148.2,'side_panel_inner_y_mm':79,'nominal_cage_envelope_mm':[248,180,175],'complete_cage_removal_fasteners':4,'physical_fit_verified':False,'limits':['No dynamic head sweep, microphone/acoustic or camera field-of-view analysis.','No impact, rollover, drop or structural load test.','Screw lengths and retaining nuts require physical fit checks.']}
(OUT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(report,indent=2))
