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
pen_holder_thickness = 3;
pen_holder_height = 30;
pen_tip_posZ = floor_Z;

servo_separation = 75;

chassis_thickness = 4;
chassis_width = servo_separation+2*8;
chassis_len = 80+chassis_width/2;
chassis_corner_radius = 10;

chassis_thirdstand_diameter = 15;
chassis_thirdstand_height = -floor_Z-chassis_thirdstand_diameter/2;

screw_diam = 3.5; // diameter for tight fit
screw_tolerance = 0.5; // loose fit

module pen() {
    color("lightblue") translate([0,0,pen_tip_posZ]) {
        translate([0,0,15]) cylinder(r=pen_diameter/2+pen_holder_tolerance, h=pen_len);
        cylinder(r1=1,r2=pen_diameter/2+pen_holder_tolerance, h=15);
    }
}

module pen_support(holes=false) {
    if(holes)
        pen();
    else
        cylinder(r=pen_diameter/2+pen_holder_thickness, h=chassis_thickness+pen_holder_height);
}

module servo(holes=false,wheel=false) {
    if(holes) {
        
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

module chassis_thirdstand(holes=false) {
    if(holes) {
        translate([0,chassis_len-chassis_width/2-chassis_thirdstand_diameter/2,floor_Z+chassis_thirdstand_diameter/2])
            cylinder(r=screw_diam/2+screw_tolerance,h=chassis_thirdstand_height*2);
    } else {
        translate([0,chassis_len-chassis_width/2-chassis_thirdstand_diameter/2,floor_Z+chassis_thirdstand_diameter/2]) union() {
            sphere(r=chassis_thirdstand_diameter/2);
            difference() {
                cylinder(r=chassis_thirdstand_diameter/2,h=chassis_thirdstand_height);
                cylinder(r=screw_diam/2,h=chassis_thirdstand_height+1);
            }
        }
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
        }
        pen_support(holes=true);
        two_servos(holes=true);
        chassis_thirdstand(holes=true);
    }
}

module non_3D_printed() {
    two_servos(wheels=true);
    pen();
}

chassis();
chassis_thirdstand();
non_3D_printed();

