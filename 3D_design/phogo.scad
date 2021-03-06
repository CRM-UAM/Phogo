// This source file is part of the Phogo project
// https://github.com/CRM-UAM/Phogo
// Released under the GNU General Public License Version 3
// Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain



// Increase the resolution of default shapes
$fa = 5; // Minimum angle for fragments [degrees]
$fs = 0.5; // Minimum fragment size [mm]

use <libs/MCAD/servos.scad>
use <libs/Servo-wheel.scad>
use <libs/build_plate.scad>

wheel_diameter = 42;

floor_Z = -wheel_diameter;

pen_diameter = 17;
pen_len = 120;
pen_holder_tolerance = 0.5;
pen_holder_thickness = 2;
pen_holder_height = 35;
pen_tip_posZ = floor_Z;
pen_holder_Xoffset = 1;

servo_separation = 75+7;

chassis_thirdstand_diameter = 15;
chassis_thirdstand_height = -floor_Z-chassis_thirdstand_diameter/2;

chassis_thickness = 3;
chassis_width = servo_separation+2*8;
chassis_len = 70+chassis_width/2;
chassis_corner_radius = chassis_thirdstand_diameter/2;

screw_diam = 4; // diameter for tight fit

ultrasound_posY = -chassis_width/2+21;
ultrasound_support_len = 8;
ultrasound_support_X = 10;
ultrasound_support_Y = 2.5;
ultrasound_support_tolerance = 0.8;
ultrasound_support_thickness = 2;

module pen_support_vitamins() {
    color("lightblue") translate([0,0,pen_tip_posZ]) {
        translate([0,0,25]) cylinder(r=pen_diameter/2, h=pen_len-25);
        cylinder(r1=1.5,r2=pen_diameter/2+pen_holder_tolerance, h=25);
    }
    translate([-3+pen_holder_Xoffset,-8-pen_diameter/2,chassis_thickness])
        color("gray") alignds420([-18,0,17], [-90,0,-90]); // mini-servo para el rotulador
}

module pen_support(holes=false) {
    if(holes) {
        translate([0,0,pen_tip_posZ])
            cylinder(r=pen_diameter/2+pen_holder_tolerance, h=pen_len);
        cylinder(r1=pen_diameter/2+pen_holder_tolerance, r2=pen_diameter/2+2*pen_holder_tolerance, h=chassis_thickness+0.1);
        // Agujeros para sujetar el mini-servo
        translate([-3+pen_holder_Xoffset,-9-pen_diameter/2,0]) cube([3,14,chassis_thickness*3],center=true);
        translate([-11+pen_holder_Xoffset,-pen_diameter/2-2,0]) cube([6,3,chassis_thickness*3],center=true);
        translate([-11+pen_holder_Xoffset,-pen_diameter/2-16,0]) cube([6,3,chassis_thickness*3],center=true);
        // Agujero para el cable del mini-servo
        translate([-26+pen_holder_Xoffset,-9-pen_diameter/2,0]) cube([4,11,chassis_thickness*3],center=true);
        // Agujeros para los cables de la electronica
        translate([0,pen_diameter/2+pen_holder_thickness+6/2,0]) cube([15,6,chassis_thickness*3],center=true);
        translate([0,chassis_len-chassis_width/2-5,0]) cube([15,6,chassis_thickness*3],center=true);
    } else
        translate([0,0,-pen_holder_height])
            cylinder(r=pen_diameter/2+pen_holder_thickness, h=pen_holder_height+0.1);
}

module pen_holder() {
    translate([0,0,40])
        difference() {
            union() {
                cylinder(r=15+pen_diameter/2, h=1);
                difference() {
                    for(i=[-1,1]) rotate([90,0,45*i]) cylinder(r=14+pen_diameter/2, h=4, center=true);
                    rotate([180,0,0]) cylinder(r=15+pen_diameter/2, h=100);
                }
            }
            translate([0,0,-1]) cylinder(r1=pen_diameter/2+pen_holder_tolerance,r2=pen_diameter/2-4*pen_holder_tolerance, h=15+pen_diameter/2+2);
        }
    }

module continuous_rotation_servo(holes=false,wheel=false) {
    if(holes) {
        // Agujeros para las bridas
        translate([-2.5,-15,0]) cube([2.5,6,chassis_thickness*3],center=true);
        translate([2.5,-15,0]) cube([2.5,6,chassis_thickness*3],center=true);
        translate([-2.5,50-15,0]) cube([2.5,6,chassis_thickness*3],center=true);
        translate([2.5,50-15,0]) cube([2.5,6,chassis_thickness*3],center=true);
    } else {
        color("gray") futabas3003([-28,30,-20], [0,-90,180]);
        if(wheel) translate([12,0,-10]) rotate([0,90,0]) {
            Servo_wheel_6_arm_horn(); // Ruedas impresas
            color("gray") horn6(); // Soporte servo 6 brazos
        }
    }
}

module main_motors(holes=false,wheels=false) {
    translate([-servo_separation/2,0,0])
        mirror([1,0,0]) continuous_rotation_servo(holes,wheels);
    translate([servo_separation/2,0,0])
        continuous_rotation_servo(holes,wheels);
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

module battery(holes=false) {
    translate([0,50,0])
    if(holes) {
        translate([-15,14,0]) cube([5,2,chassis_thickness*3],center=true);
        translate([-15,-14,0]) cube([5,2,chassis_thickness*3],center=true);
        translate([15,14,0]) cube([5,2,chassis_thickness*3],center=true);
        translate([15,-14,0]) cube([5,2,chassis_thickness*3],center=true);
    } else {
        color("pink") translate([0,0,-15/2]) cube([52,25,15],center=true);
    }
}

// From: https://github.com/bq/zum/tree/master/zum-bt328/stl
module arduino(holes=false) {
    translate([0,43,2])
    if(holes) {
        translate([19.25,-24.25,0]) cylinder(r=screw_diam/2, h=chassis_thickness*5, center=true);
        translate([20.5,24,0]) cylinder(r=screw_diam/2, h=chassis_thickness*5, center=true);
        translate([-31.5,19,0]) cylinder(r=screw_diam/2, h=chassis_thickness*5, center=true);
        translate([-31.5,-9,0]) cylinder(r=screw_diam/2, h=chassis_thickness*5, center=true);
        for(i=[-1,1]) for(j=[-1,1]) translate([10*i,10*j,0]) cylinder(r=screw_diam/2, h=chassis_thickness*5, center=true);
    } else color("lightgray") translate([34.5,26.5,chassis_thickness+1.6]) rotate([0,0,180]) import("libs/zum_bt_328.stl");
}

module thirdstand() {
    for(i=[-1,1]) translate([i*(chassis_width/2-chassis_thirdstand_diameter/2),chassis_len-chassis_width/2-chassis_thirdstand_diameter/2,floor_Z+chassis_thirdstand_diameter/2]) union() {
            sphere(r=chassis_thirdstand_diameter/2);
            cylinder(r=chassis_thirdstand_diameter/2,h=chassis_thirdstand_height+0.1);
        }
}

module text_on_chassis() {
    translate([0,chassis_len-chassis_width/2-7,0])
    *rotate([0,0,180]) scale([1.5,1,1]) translate([0,0,chassis_thickness-1.5]) linear_extrude(height=10) {
        text("PHOGO",size=10,font="Liberation Sans",halign="center",valign="center",$fn=16);
    }
    translate([0,2,0])
    rotate([0,0,180]) translate([0,0,chassis_thickness-1.5]) linear_extrude(height=10) {
        text("CRM      UAM",size=10,font="Liberation Sans :style=Bold",halign="center",valign="center",$fn=16);
    }
    translate([0,-chassis_width/4-4,0])
    rotate([0,0,180]) translate([0,0,chassis_thickness-1.5]) linear_extrude(height=10) {
        text("L              R",size=10,font="Liberation Sans :style=Bold",halign="center",valign="center",$fn=16);
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
        main_motors(holes=true);
        ultrasound_support(holes=true);
        text_on_chassis();
        arduino(holes=true);
        battery(holes=true);
    }
}

module non_3D_printed() {
    main_motors(wheels=true);
    pen_support_vitamins();
    ultrasound();
    arduino();
    battery();
}

pen_holder();
chassis();
non_3D_printed();

//for display only, doesn't contribute to final object
translate([0,0,floor_Z]) build_plate(3,200,200);
