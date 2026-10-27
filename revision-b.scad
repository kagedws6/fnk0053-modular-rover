// FNK0053 revision B: measured kit packaging, experimental frame.
// Units mm; +X front, Y side, Z up. Full chassis fit/strength not verified.
// Run scripts/build_mechanics.py to regenerate the shared planar profiles.
include <generated/profiles-b.scad>
$fn=48;
part="assembly"; // assembly, frame, deck, bumper, audio_adapter, bracket_coupon
explode=0;
module rounded_plate(l,w,h,r=3){linear_extrude(h)hull()for(x=[-l/2+r,l/2-r],y=[-w/2+r,w/2-r])translate([x,y])circle(r);}
module frame(){
 difference(){
  union(){linear_extrude(4)frame_profile();for(p=board_posts)translate([p[0],p[1],4])difference(){cylinder(d=10,h=6.7);translate([0,0,-.01])cylinder(d=3.4,h=6.72);}}
  for(p=board_posts)translate([p[0],p[1],-.01])cylinder(d=6.4,h=2.42);
 }
}
module deck(){linear_extrude(4)deck_profile();}
module bumper(){difference(){union(){translate([8.5,0,0])rounded_plate(5,132,12,2);for(y=[-50,50])translate([0,y,4])rounded_plate(16,14,4,2);}for(y=[-50,50])translate([0,y,3.99])cylinder(d=3.4,h=4.02);}}
module audio_adapter(){difference(){cylinder(d=78,h=3);translate([0,0,-1])cylinder(d=48,h=5);for(a=[0:90:270])rotate([0,0,a])translate([33,0,-1])cylinder(d=3.4,h=5);}}
module bracket_coupon(){difference(){rounded_plate(26,20,2);for(x=[-4,4])translate([x,0,-1])cylinder(d=3.4,h=4);}}
module wheel(w){translate(w[0])rotate([90,0,0]){color("#363d43")cylinder(d=64.6,h=w[1],center=true);color("#cfb657")cylinder(d=44,h=w[1]+.3,center=true);}}
module assembly(){
 color("#2c879a")translate([0,0,43.3])frame();
 for(s=[-1,1])translate([s*116,0,43.3])if(s<0)mirror([1,0,0])color("#dea353")bumper();else color("#dea353")bumper();
 for(w=wheel_envelopes)wheel(w);
 for(m=motor_envelopes)color("#cfb657")translate(m[0])cube(m[1],center=true);
 for(pair=bracket_pairs){p=(pair[0]+pair[1])/2;color("#aaaa9f")translate([p[0],p[1],32.3])cube([14,5,22],center=true);}
 color("#35584d")translate([0,0,54+explode*.25])linear_extrude(1.6)board_profile();
 color("#424b55")translate([-81,0,55.6+explode*.25])rounded_plate(42,80,21);
 for(p=board_posts)color("#aaaa9f")translate([p[0],p[1],55.6+explode*.5])cylinder(d=5.4,h=28);
 color("#2c879a")translate([0,0,83.6+explode])deck();
 color("#dea353")translate([-6,-13,91.6+explode*1.5])audio_adapter();
 color("#776b97")translate([-6,-13,97.6+explode*2])cylinder(d=70,h=12);
 color("#aaaa9f")translate([-6,-13,109.6+explode*2])cylinder(d=70,h=1.5);
 color("#73926b")translate([-10,44,87.6+explode])rounded_plate(64,22,9);
 color("#424b55")translate([37,42,87.6+explode])rounded_plate(24,24,8);
 color("#424b55")translate([83.56,0,50.5+explode*.5])cube([32.8,12,30.2],center=true);
 for(y=[-18,18])color("#2c879a")translate([85,y,84+explode])cube([12,4,38],center=true);
 color("#424b55")translate([89,0,88+explode])cube([25,12,30],center=true);
 color("#424b55")translate([110,0,118.2+explode])cube([7,56,60],center=true);
 color("#152432")translate([113.7,0,127.7+explode])cube([.4,48,25],center=true);
 color("#35584d")translate(sensor_envelope[0])cube(sensor_envelope[1],center=true);
 for(p=sensor_posts)color("#aaaa9f")translate([p[0],p[1],15.3])cylinder(d=5.4,h=28);
}
if(part=="assembly")assembly();else if(part=="frame")frame();else if(part=="deck")deck();else if(part=="bumper")bumper();else if(part=="audio_adapter")audio_adapter();else if(part=="bracket_coupon")bracket_coupon();
