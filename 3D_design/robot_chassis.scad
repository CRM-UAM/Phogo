// This source file is part of the Phogo project
// https://github.com/CRM-UAM/Phogo
// Released under the GNU General Public License Version 3
// Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

// Increase the resolution of default shapes
$fa = 5; // Minimum angle for fragments [degrees]
$fs = 0.5; // Minimum fragment size [mm]

use <libs/MCAD/servos.scad>
use <libs/Servo-wheel.scad>

wheel_diameter = 42;

floor_Z = -wheel_diameter;

pen_diameter = 10;
pen_len = 110;
pen_holder_tolerance = 0.5;
pen_holder_thickness = 2;
pen_holder_height = 35;
pen_tip_posZ = floor_Z;

servo_separation = 75;

chassis_thickness = 3;
chassis_width = servo_separation+2*8;
chassis_len = 80+chassis_width/2;
chassis_corner_radius = 10;

chassis_thirdstand_diameter = 15;
chassis_thirdstand_height = -floor_Z-chassis_thirdstand_diameter/2;

screw_diam = 3.5; // diameter for tight fit
screw_tolerance = 0.5; // loose fit

ultrasound_posY = -chassis_width/2+25;
ultrasound_support_len = 8;
ultrasound_support_X = 10;
ultrasound_support_Y = 2.5;
ultrasound_support_tolerance = 0.5;
ultrasound_support_thickness = 2;

module pen() {
    color("lightblue") translate([0,0,pen_tip_posZ]) {
        translate([0,0,15]) cylinder(r=pen_diameter/2, h=pen_len-15);
        cylinder(r1=1,r2=pen_diameter/2+pen_holder_tolerance, h=15);
    }
}

module pen_support(holes=false) {
    if(holes)
        translate([0,0,pen_tip_posZ])
            cylinder(r=pen_diameter/2+pen_holder_tolerance, h=pen_len);
    else
        translate([0,0,-pen_holder_height])
            cylinder(r=pen_diameter/2+pen_holder_thickness, h=pen_holder_height+0.1);
}

module servo(holes=false,wheel=false) {
    if(holes) {
        // Agujeros para las bridas
        translate([-2.5,-15,0]) cube([2,5,chassis_thickness*3],center=true);
        translate([2.5,-15,0]) cube([2,5,chassis_thickness*3],center=true);
        translate([-2.5,50-15,0]) cube([2,5,chassis_thickness*3],center=true);
        translate([2.5,50-15,0]) cube([2,5,chassis_thickness*3],center=true);
    } else {
        color("gray") futabas3003([-28,30,-20], [0,-90,180]);
        if(wheel) translate([12,0,-10]) rotate([0,90,0]) {
            Servo_wheel_6_arm_horn();
            color("gray") horn6();
        }
    }
}

module two_servos(holes=false,wheels=false) {
    translate([-servo_separation/2,0,0])
        mirror([1,0,0]) servo(holes,wheels);
    translate([servo_separation/2,0,0])
        servo(holes,wheels);
}

// From: https://github.com/Obijuan/printbot_part_library/tree/master/sensors/ultrasound
module ultrasound() {
    color("darkgray")
    translate([0,ultrasound_posY,0])
        translate([0,-4.5,14]) rotate([90,0,0]) import("libs/BAT-ultrasonic.stl");
}

module ultrasound_support(holes=false) {
    translate([0,ultrasound_posY,0])
        if(holes)
            cube([ultrasound_support_X+2*ultrasound_support_tolerance,ultrasound_support_Y+2*ultrasound_support_tolerance,ultrasound_support_len*3],center=true);
        else
            translate([0,0,-ultrasound_support_len/2+0.1]) cube([ultrasound_support_X+2*ultrasound_support_thickness,ultrasound_support_Y+2*ultrasound_support_thickness,ultrasound_support_len],center=true);
}

// From: https://github.com/bq/zum/tree/master/zum-bt328/stl
module electronics() {
    color("lightgray")
    translate([0,35,0])
    translate([34.5,26.5,chassis_thickness+1.6]) rotate([0,0,180]) import("libs/zum_bt_328.stl");
}

module thirdstand() {
    translate([0,chassis_len-chassis_width/2-chassis_thirdstand_diameter/2,floor_Z+chassis_thirdstand_diameter/2]) union() {
            sphere(r=chassis_thirdstand_diameter/2);
            cylinder(r=chassis_thirdstand_diameter/2,h=chassis_thirdstand_height+0.1);
        }
}

module text_on_chassis() {
    translate([0,chassis_len-chassis_width/2-9,0])
    rotate([0,0,180]) scale([1.5,1,1]) translate([0,0,chassis_thickness-1.5]) linear_extrude(height=10) {
        text("PHOGO",size=10,font="Liberation Sans",halign="center",valign="center",$fn=16);
    }
}

module chassis() {
    difference() {
        union() {
            hull() {
                cylinder(r=chassis_width/2,h=chassis_thickness);
                translate([-chassis_width/2+chassis_corner_radius,chassis_len-chassis_width/2-chassis_corner_radius,0])
                    cylinder(r=chassis_corner_radius,h=chassis_thickness);
                translate([chassis_width/2-chassis_corner_radius,chassis_len-chassis_width/2-chassis_corner_radius,0])
                    cylinder(r=chassis_corner_radius,h=chassis_thickness);
            }
            pen_support();
            thirdstand();
            ultrasound_support();
        }
        pen_support(holes=true);
        two_servos(holes=true);
        ultrasound_support(holes=true);
        text_on_chassis();
    }
}

module non_3D_printed() {
    two_servos(wheels=true);
    pen();
    ultrasound();
    electronics();
}

chassis();
non_3D_printed();

