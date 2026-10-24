// Fit-check tools, mm. These do not reproduce the Freenove bracket.
// Gauge range is a design choice, NOT a claim about actual bracket spacing.
$fn=96;
part="spacing"; // spacing or clearance
plate_thickness=2;
mark_height=0.4;
module rounded(l,w,r=3){linear_extrude(plate_thickness)hull()for(x=[-l/2+r,l/2-r],y=[-w/2+r,w/2-r])translate([x,y])circle(r);}
module label(t,x,y,size=3){translate([x,y,plate_thickness])linear_extrude(mark_height)text(t,size=size,halign="center",valign="center");}
module spacing(){
 difference(){
  rounded(64,28);
  translate([-22,0,-1])cylinder(d=3.6,h=plate_thickness+2);
  translate([0,0,-1])linear_extrude(plate_thickness+2)hull()for(x=[-14,14])translate([x,0])circle(d=3.6);
 }
 label("M3 FIT",0,8);
 label("0",-22,-10);
 for(d=[8:2:36])translate([-22+d-0.3,d%10==0?-6:-5,plate_thickness])cube([0.6,d%10==0?2.7:1.7,mark_height]);
 for(d=[10,20,30])label(str(d),-22+d,-10);
}
module clearance(){
 difference(){
  rounded(56,24);
  for(i=[0:2])translate([-17+17*i,2,-1])cylinder(d=3.2+i*0.2,h=plate_thickness+2);
 }
 for(i=[0:2])label(str(3.2+i*0.2),-17+17*i,-6);
}
if(part=="spacing")spacing();else clearance();
// STL generator uses a block font for tool-independent labels; SCAD text differs cosmetically.
