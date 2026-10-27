"""Removable cage geometry; nominal mm, prototype only, no impact rating."""
import math
import numpy as np
import trimesh
from shapely.geometry import LineString,Point,box
from shapely.ops import unary_union
from mechanical_layout import D,FRAME_BLANK,FRAME,BOARD_POSTS,rounded,holes,extrude

MOUNTS=[(x,y) for x in [-114,114] for y in [-64,64]]
PAD_BLANK=unary_union([Point(*p).buffer(7,quad_segs=12) for p in MOUNTS])
PAD_PROFILE=PAD_BLANK.difference(holes(MOUNTS))
CAGE_FRAME_BLANK=FRAME_BLANK.union(PAD_BLANK)
CAGE_FRAME=FRAME.union(PAD_PROFILE).difference(holes(MOUNTS))
SIDE_Y=83.0
SIDE_THICKNESS=8.0
BASE=51.3
SIDE_PATH=[(-114,59.3),(-120,85),(-120,153),(-108,165),(108,165),(120,153),(120,85),(114,59.3)]
SIDE_BLANK=LineString(SIDE_PATH).buffer(4,quad_segs=8,join_style=1)
SIDE_BLANK=SIDE_BLANK.union(unary_union([box(x-7,BASE,x+7,67.3) for x in [-114,114]]))
SIDE_PROFILE=SIDE_BLANK.difference(holes([(-114,59.3),(114,59.3)]))
FOOT_PROFILE=LineString([(0,0),(0,19)]).buffer(7,quad_segs=8).difference(holes([(0,0)]))
ROOF_PROFILE=rounded(12,180,3).difference(holes([(0,-83),(0,83)]))

def cylinder_between(start,end,radius=1.7,sections=24):
 start=np.asarray(start);end=np.asarray(end)
 return trimesh.creation.cylinder(radius=radius,segment=[start,end],sections=sections)

def side_flat():
 # Flat print coordinates: X=vehicle X, Y=height above base, Z=panel thickness.
 mesh=extrude(SIDE_PROFILE,8)
 cutters=[cylinder_between([x,159,-0+4],[x,171,4]) for x in [-100,100]]
 mesh=trimesh.boolean.difference([mesh]+cutters,engine='manifold')
 mesh.apply_translation([0,-BASE,0]);return mesh

def foot_flat():
 plate=extrude(FOOT_PROFILE,4)
 ear=trimesh.creation.box(extents=[14,5,16]);ear.apply_translation([0,12.5,12])
 foot=trimesh.boolean.union([plate,ear],engine='manifold')
 return trimesh.boolean.difference([foot,cylinder_between([0,8,12],[0,17,12])],engine='manifold')

def roof_flat():return extrude(ROOF_PROFILE,6)

def side_world(mesh,side):
 m=mesh.copy()
 # Transform the flat panel into the XZ plane at either side of the rover.
 transform=np.array([[1,0,0,0],[0,0,side,side*(SIDE_Y-4)],[0,1,0,BASE],[0,0,0,1]],dtype=float)
 m.apply_transform(transform);return m

def foot_world(mesh,x,side):
 m=mesh.copy()
 if side<0:m.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[0,0,1]))
 m.apply_translation([x,side*64,47.3]);return m

def assembly_meshes():
 side=side_flat();foot=foot_flat();roof=roof_flat()
 result=[('Left side hoop',side_world(side,-1)),('Right side hoop',side_world(side,1))]
 for x in [-114,114]:
  for s in [-1,1]:result.append(('Removable cage foot',foot_world(foot,x,s)))
 for x in [-100,100]:
  m=roof.copy();m.apply_translation([x,0,169]);result.append(('Upper crossbar',m))
 result.append(('Cage mounting pads',extrude(PAD_PROFILE,4,43.3)))
 return result
