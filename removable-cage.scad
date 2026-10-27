// Optional removable exoskeleton for revision B. Prototype, not impact rated.
include <generated/cage-profiles.scad>
module cage_side_flat(){
 translate([0,-51.3,0])difference(){
  linear_extrude(8)cage_side_profile();
  for(x=[-100,100])translate([x,159,4])rotate([-90,0,0])cylinder(d=3.4,h=12);
 }
}
module cage_foot_flat(){difference(){union(){linear_extrude(4)cage_foot_profile();translate([-7,10,4])cube([14,5,16]);}translate([0,8,12])rotate([-90,0,0])cylinder(d=3.4,h=9);}}
module cage_roof_flat(){linear_extrude(6)cage_roof_profile();}
module cage_ready_frame(){
 difference(){union(){frame();linear_extrude(4)cage_pad_profile();}for(p=cage_mounts)translate([p[0],p[1],-.01])cylinder(d=3.4,h=4.02);}
}
module removable_cage(){
 for(s=[-1,1]){
  translate([0,s*79,51.3])multmatrix([[1,0,0,0],[0,0,s,0],[0,1,0,0],[0,0,0,1]])cage_side_flat();
  for(x=[-114,114])translate([x,s*64,47.3])rotate([0,0,s<0?180:0])cage_foot_flat();
 }
 for(x=[-100,100])translate([x,0,169])cage_roof_flat();
}
