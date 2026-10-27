 let hitBuffer=new Int16Array(0);
 const probe=document.createElement('canvas');probe.width=1;probe.height=1;
 const probeContext=probe.getContext('2d',{willReadFrequently:true});
 function draw(){
   colors();width=Math.round(canvas.clientWidth);height=Math.round(canvas.clientHeight);
   canvas.width=width;canvas.height=height;
   const rgba={};for(const key in palette){probeContext.clearRect(0,0,1,1);probeContext.fillStyle=palette[key];probeContext.fillRect(0,0,1,1);rgba[key]=probeContext.getImageData(0,0,1,1).data}
   const shown=model.parts.map((p,i)=>({p,i})).filter(({p})=>frameOnly?(p.level===0&&['frame','mount','hole'].includes(p.category)):(components||['frame','mount','hole'].includes(p.category)));
   let loU=Infinity,hiU=-Infinity,loV=Infinity,hiV=-Infinity;
   shown.forEach(({p})=>p.faces.forEach(f=>f.forEach(v=>{const q=project(v,p.level);loU=Math.min(loU,q.u);hiU=Math.max(hiU,q.u);loV=Math.min(loV,q.v);hiV=Math.max(hiV,q.v)})));
   const scale=Math.min((width-36)/(hiU-loU),(height-42)/(hiV-loV));
   const ox=width/2-(loU+hiU)*scale/2,oy=height/2+(loV+hiV)*scale/2;
   const output=ctx.createImageData(width,height),pixels=output.data,depths=new Float32Array(width*height);depths.fill(-Infinity);
   hitBuffer=new Int16Array(width*height);hitBuffer.fill(-1);
   for(const {p,i} of shown){
     for(const f of p.faces){
       const points=f.map(v=>{const q=project(v,p.level);return [ox+q.u*scale,oy-q.v*scale,q.depth]});
       const a=f[1].map((v,k)=>v-f[0][k]),b=f[2].map((v,k)=>v-f[0][k]);
       const n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],len=Math.hypot(...n)||1;
       const shade=.06+(1-Math.abs((n[0]*.25-n[1]*.4+n[2]*.88)/len))*.24;
       const base=rgba[p.category],background=rgba.shade;
       const color=[0,1,2].map(k=>Math.round(base[k]*(1-shade)+background[k]*shade));
       if(i===selected)for(let k=0;k<3;k++)color[k]=Math.round(color[k]*.65+rgba.highlight[k]*.35);
       for(let t=1;t<points.length-1;t++){
         const [a,b,c]=[points[0],points[t],points[t+1]];
         const denominator=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
         if(Math.abs(denominator)<.00001)continue;
         const minX=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),maxX=Math.min(width-1,Math.ceil(Math.max(a[0],b[0],c[0])));
         const minY=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),maxY=Math.min(height-1,Math.ceil(Math.max(a[1],b[1],c[1])));
         for(let y=minY;y<=maxY;y++)for(let x=minX;x<=maxX;x++){
           const u=((b[1]-c[1])*(x+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))/denominator;
           const v=((c[1]-a[1])*(x+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))/denominator;
           const w=1-u-v;if(u<0||v<0||w<0)continue;
           const depth=u*a[2]+v*b[2]+w*c[2],index=y*width+x;
           if(depth<=depths[index]+.00001)continue;
           depths[index]=depth;hitBuffer[index]=i;const offset=index*4;
           pixels[offset]=color[0];pixels[offset+1]=color[1];pixels[offset+2]=color[2];pixels[offset+3]=255;
         }
       }
     }
   }
   ctx.putImageData(output,0,0);
 }
