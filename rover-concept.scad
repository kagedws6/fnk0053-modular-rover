// FNK0053 modular rover -- CONCEPT ONLY, revision A.
// Units: mm. All component dimensions and hole positions are UNVERIFIED.
// Not a fit-checked or print-ready chassis. Use fit coupons before fabrication.
// +X = front, Y = left/right, Z = up. Ground = Z0.
$fn = 48;
part = "assembly"; // assembly, frame, deck, audio_adapter, bumper
explode = 0;
frame_length = 238;
frame_width = 132;
rail_width = 12;
wheelbase = 124;
wheel_diameter = 65;
wheel_width = 27;
wheel_center_y = 83;
accessory_pitch = 12; // proposed design choice, not a Freenove standard
accessory_hole = 3.4; // nominal M3 clearance, print compensation unverified

module rounded_plate(l,w,h,r=8) {
    linear_extrude(h) hull()
        for(x=[-l/2+r,l/2-r],y=[-w/2+r,w/2-r])
            translate([x,y]) circle(r);
}
module bumper() {
    difference() {
        rounded_plate(14,132,12,5);
        for(y=[-48,48]) translate([0,y,-1]) cylinder(d=accessory_hole,h=14);
    }
}
module frame() {
    difference() {
        union() {
            difference() {
                rounded_plate(frame_length,frame_width,8,13);
                translate([0,0,-1]) rounded_plate(frame_length-2*rail_width,frame_width-2*rail_width,10,8);
            }
            // Transverse supports at the board center; motor pockets remain open.
            for(x=[-10,10]) translate([x-4,-54,0]) cube([8,108,8]);
            // Provisional motor-bracket tabs: geometry pending measurements.
            for(x=[-62,62],y=[-43,43])
                translate([x,y,0]) rounded_plate(24,22,8,3);
        }
        // Side accessory row. Actual kit mounting holes deliberately omitted.
        for(x=[-96:accessory_pitch:96],y=[-60,60])
            translate([x,y,-1]) cylinder(d=accessory_hole,h=10);
    }
}
module deck() {
    difference() {
        rounded_plate(112,120,4,10);
        for(x=[-42:accessory_pitch:42],y=[-48:accessory_pitch:48])
            translate([x,y,-1]) cylinder(d=accessory_hole,h=6);
        for(x=[-40,40],y=[-48,48])
            translate([x,y,-1]) cylinder(d=3.4,h=6);
        // Ribbon/wiring opening, provisional.
        translate([39,0,-1]) rounded_plate(18,30,6,3);
    }
}
module audio_adapter() {
    difference() {
        cylinder(d=78,h=3);
        translate([0,0,-1]) cylinder(d=48,h=5);
        // Deck interface only; audio-board-specific holes await confirmation.
        for(a=[0:90:270]) rotate([0,0,a]) translate([33,0,-1]) cylinder(d=3.4,h=5);
    }
}
module wheel() {
    rotate([90,0,0]) {
        color("#292d33") cylinder(d=wheel_diameter,h=wheel_width,center=true);
        color("#d7b653") cylinder(d=wheel_diameter*0.68,h=wheel_width+0.4,center=true);
    }
}
module assembly() {
    color("#2c7784") translate([0,0,46]) frame();
    for(x=[-115,115]) color("#db9b4c") translate([x,0,44]) bumper();
    for(x=[-wheelbase/2,wheelbase/2],y=[-wheel_center_y,wheel_center_y])
        translate([x,y,wheel_diameter/2]) wheel();
    for(x=[-49,49],y=[-47,47]) color("#d7b653")
        translate([x-29,y-11,22.5]) cube([58,22,20]);
    // Main shield envelope, including integrated rear battery-holder envelope.
    color("#334246") translate([0,0,56+explode*0.25]) rounded_plate(210,124,2,5);
    color("#40454d") translate([-82,0,58+explode*0.25]) rounded_plate(38,80,21,3);
    for(x=[-40,40],y=[-48,48]) color("#b7a46e")
        translate([x,y,58+explode*0.5]) cylinder(d=6,h=30);
    color("#2c7784") translate([0,0,88+explode]) deck();
    color("#db9b4c") translate([-6,-13,96+explode*1.5]) audio_adapter();
    // Approximate existing Waveshare round audio stack; not manufacturing data.
    color("#465b63") translate([-6,-13,102+explode*2]) cylinder(d=70,h=12);
    color("#bda884") translate([-6,-13,114+explode*2]) cylinder(d=70,h=1.5);
    color("#788d77") translate([-10,44,92+explode]) rounded_plate(64,22,9,3);
    color("#40454d") translate([37,42,92+explode]) rounded_plate(24,24,8,3);
    // Existing pan/tilt head and camera/display envelope.
    color("#40454d") translate([78,0,65+explode*0.5]) rounded_plate(25,30,32,3);
    color("#2c7784") translate([82,0,98+explode]) rounded_plate(30,45,5,4);
    color("#40454d") translate([95,-28,90+explode]) cube([7,56,60]);
    color("#111d25") translate([102,-24,117+explode]) cube([1,48,25]);
    color("#40454d") translate([100,0,16]) rounded_plate(28,62,4,3);
}
if(part == "assembly") assembly();
else if(part == "frame") frame();
else if(part == "deck") deck();
else if(part == "audio_adapter") audio_adapter();
else if(part == "bumper") bumper();
