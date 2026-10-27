"""Revision B planar profiles shared by CAD export, preview and clearance checks."""
from pathlib import Path
import json
from shapely.geometry import box,Point,LineString
from shapely.ops import unary_union
from shapely.affinity import translate

ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'data'/'kit-dimensions.json').read_text())
def rounded(l,w,r=3,cx=0,cy=0):
 return translate(box(-l/2+r,-w/2+r,l/2-r,w/2-r).buffer(r,quad_segs=12),cx,cy)
def holes(points,d=3.4):return unary_union([Point(x,y).buffer(d/2,quad_segs=16) for x,y in points])
def cutouts(clearance=2):
 return unary_union([box(w['min'][0]-clearance,w['min'][1]-clearance,w['max'][0]+clearance,w['max'][1]+clearance) for w in D['wheels']])

BRACKET_HOLES=[q for p in D['brackets'] for q in p['holes']]
BOARD_POSTS=D['board_posts'];SENSOR_POSTS=D['sensor_posts']
BUMPER_HOLES=[(x,y) for x in [-116,116] for y in [-50,50]]
ACCESSORY_HOLES=[(x,y) for x in range(-96,97,12) for y in [-35,35] if all(Point(x,y).distance(Point(*h))>6 for h in BRACKET_HOLES+BOARD_POSTS+SENSOR_POSTS)]

members=[rounded(244,12,3,cy=y) for y in [-35,35]]
members += [rounded(14,132,3,cx=x) for x in [-115,0,115]]
for b in D['brackets']:
 x=sum(q[0] for q in b['holes'])/2
 members.append(rounded(20,82,3,cx=x))
# Sensor carrier retains the original underside attachment elevation.
members.append(rounded(14,82,3,cx=sum(q[0] for q in SENSOR_POSTS)/2))
for x,y in BOARD_POSTS:
 nearest=min([sum(q[0] for q in b['holes'])/2 for b in D['brackets']]+[0],key=lambda t:abs(t-x))
 members.append(LineString([(nearest,y),(x,y)]).buffer(6,quad_segs=12))
PAN_SERVO=box(83.56-16.4,-6,83.56+16.4,6)
SERVO_OPENING=rounded(36.8,16,2,cx=83.56)
FRAME_BLANK=unary_union(members).difference(cutouts()).difference(SERVO_OPENING).buffer(0)
FRAME_HOLES=BRACKET_HOLES+BOARD_POSTS+SENSOR_POSTS+BUMPER_HOLES+ACCESSORY_HOLES
FRAME=FRAME_BLANK.difference(holes(FRAME_HOLES))
BOSSES=[Point(x,y).buffer(5,quad_segs=20).difference(holes([(x,y)])) for x,y in BOARD_POSTS]
DECK_BLANK=rounded(110,120,8,cx=2.72179)
RIBBON=rounded(12,24,3,cx=46,cy=0)
DECK_ACCESSORY=[(2.72179+x,y) for x in range(-42,43,12) for y in range(-48,49,12) if all(Point(2.72179+x,y).distance(Point(*p))>5 for p in BOARD_POSTS) and not RIBBON.buffer(3).covers(Point(2.72179+x,y))]
DECK=DECK_BLANK.difference(holes(DECK_ACCESSORY+BOARD_POSTS)).difference(RIBBON)
BOARD=rounded(D['board_size'][0],D['board_size'][1],3).difference(cutouts())
BOARD=BOARD.difference(rounded(34,16,2,cx=83.56)) # simplified servo opening, not an extracted PCB outline

def polygons(p):return list(p.geoms) if hasattr(p,'geoms') else [p]
def extrude(p,h,z=0):
 import trimesh
 meshes=[]
 for poly in polygons(p):
  m=trimesh.creation.extrude_polygon(poly.simplify(1e-7),h,engine='earcut');m.apply_translation([0,0,z]);meshes.append(m)
 return trimesh.util.concatenate(meshes)
