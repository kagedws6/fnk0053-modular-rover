"""Render a static concept image from the generated mesh; requires Pillow."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
model=json.loads((ROOT/'concept-model.json').read_text())
colors={'cage':'#dea353','frame':'#2c879a','mount':'#dea353','wheel':'#454b54','tread':'#6c737b','hub':'#d7b653','board':'#35584d','stock':'#424b55','screen':'#152432','hole':'#152432','metal':'#aaa99f','audio':'#776b97','battery':'#73926b'}
W,H=1280,920;im=Image.new('RGB',(W,H),'#f3f5f7');draw=ImageDraw.Draw(im)
yaw=-.85;elevation=.52
def project(v):
 x,y,z=v;a=math.cos(yaw);b=math.sin(yaw);c=math.cos(elevation);d=math.sin(elevation)
 return (-b*x+a*y,-d*a*x-d*b*y+c*(z-65),c*a*x+c*b*y+d*z)
pts=[project(v) for p in model['parts'] for f in p['faces'] for v in f]
lo=[min(p[i] for p in pts) for i in range(2)];hi=[max(p[i] for p in pts) for i in range(2)]
scale=min((W-100)/(hi[0]-lo[0]),(H-230)/(hi[1]-lo[1]));ox=W/2-(lo[0]+hi[0])*scale/2;oy=H/2+30+(lo[1]+hi[1])*scale/2
faces=[]
for p in model['parts']:
 for f in p['faces']:
  q=[project(v) for v in f]
  a=[f[1][i]-f[0][i] for i in range(3)];b=[f[2][i]-f[0][i] for i in range(3)]
  n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];length=math.sqrt(sum(x*x for x in n)) or 1
  light=abs((n[0]*.25-n[1]*.4+n[2]*.88)/length);factor=.74+.26*light
  color=colors[p['category']];rgb=tuple(int(int(color[i:i+2],16)*factor) for i in [1,3,5])
  faces.append(([(ox+v[0]*scale,oy-v[1]*scale,v[2]) for v in q],rgb))
pixels=np.asarray(im).copy();depths=np.full((H,W),-np.inf)
for face,color in faces:
 for i in range(1,len(face)-1):
  a,b,c=np.array([face[0],face[i],face[i+1]])
  denominator=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(denominator)<1e-8:continue
  x0=max(0,int(min(a[0],b[0],c[0])));x1=min(W-1,int(max(a[0],b[0],c[0]))+1)
  y0=max(0,int(min(a[1],b[1],c[1])));y1=min(H-1,int(max(a[1],b[1],c[1]))+1)
  if x1<x0 or y1<y0:continue
  xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
  u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/denominator
  v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/denominator;w=1-u-v
  zz=u*a[2]+v*b[2]+w*c[2];region=depths[y0:y1+1,x0:x1+1]
  mask=(u>=0)&(v>=0)&(w>=0)&(zz>region+1e-6)
  region[mask]=zz[mask];pixels[y0:y1+1,x0:x1+1][mask]=color
im=Image.fromarray(pixels);draw=ImageDraw.Draw(im)
def font(size):
 for name in ['arial.ttf','DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf']:
  try:return ImageFont.truetype(name,size)
  except OSError:pass
 return ImageFont.load_default()
draw.text((45,25),'FNK0053 MODULAR ROVER',font=font(34),fill='#202d39')
draw.text((45,75),'Removable cage | four independent base bolts',font=font(23),fill='#506174')
draw.text((45,H-70),'Optional cage: 248 x 180 x 175 mm | prototype fit and strength unverified',font=font(22),fill='#506174')
draw.text((45,H-38),'Blue: frame/deck   Orange: adapters/bumpers   Other parts: existing hardware envelopes',font=font(18),fill='#506174')
dest=ROOT/'docs'/'images'/'removable-cage.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);print(dest)
