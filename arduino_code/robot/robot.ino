// This source file is part of the Phogo project
// https://github.com/CRM-UAM/Phogo
// Released under the GNU General Public License Version 3
// Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

//--------------------------
// **** begin MISC *********
//--------------------------
// map() implementation modified for floating point operation
float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

//--------------------------
// **** begin LED **********
//--------------------------
#define LED_PIN 13
#define ON 1
#define OFF 0

void init_led() {
	pinMode(LED_PIN, OUTPUT);
}

void led(bool state) {
	digitalWrite(LED_PIN, state);
}

//--------------------------
// **** begin SERVO PEN ****
//--------------------------
#include <Servo.h>

Servo pen_servo;
#define PEN_SERVO_PIN 10
#define UP 180 // degrees
#define DOWN 140 // degrees

void pen_move(int deg) {
	pen_servo.attach(PEN_SERVO_PIN);
	pen_servo.write(deg);
	delay(500);
	pen_servo.detach(); // power down the servo after the target position has been reached
}

//--------------------------
// **** begin ULTRASOUND ***
//--------------------------
// Based on code by Robi.Wang
#define ULTRASOUND_TRIGGER_PIN 7
#define ULTRASOUND_ECHO_PIN 6

void init_ultrasound() {
	pinMode(ULTRASOUND_TRIGGER_PIN, OUTPUT);
	pinMode(ULTRASOUND_ECHO_PIN, INPUT);
	digitalWrite(ULTRASOUND_TRIGGER_PIN, LOW);
}

float measure_distance_cm() {
	digitalWrite(ULTRASOUND_TRIGGER_PIN, HIGH);
	delayMicroseconds(10);
	digitalWrite(ULTRASOUND_TRIGGER_PIN, LOW);
	long microseconds = pulseIn(ULTRASOUND_ECHO_PIN, HIGH, 20000); // Measures the duration of the input pulse (it is proportional to the time it takes for the sound to bounce back)
	return microseconds / 29. / 2.;
}

int measure_distance_cm_filtered(int nsamples) {
	float res = 0;
	int n = nsamples;
	while (n > 0) {
		float dist = measure_distance_cm();
		if (dist > 0) {
			res += dist;
			n--;
		}
		delay(10);
	}
	return res / nsamples;
}

//--------------------------
// **** begin IMU **********
//--------------------------
// Gyroscope/Accelerometer code derived from: MPU-6050 Short Example Sketch by Arduino User JohnChi
#define MPU6050_VCC_PIN A0
#define MPU6050_GND_PIN A1
#define MPU6050_SDA_PIN A3
#define MPU6050_SCL_PIN A2

#include <SoftwareWire.h> // Using a virtual I2C port and 5V power through two digital pins,
// allows to plug the gyroscope module directly into a row of pins, without the need for extra wires

SoftwareWire Wire(MPU6050_SDA_PIN, MPU6050_SCL_PIN);

const int MPU = 0x68; // I2C address of the MPU-6050

#define MPU6050_PWR_MGMT_1    0x6B
#define MPU6050_ACCEL_CONFIG  0x1C
#define MPU6050_GYRO_CONFIG   0x1B
#define MPU6050_SMPLRT_DIV    0x19
#define MPU6050_CONFIG        0x1A

int16_t AcX, AcY, GyZ;
int16_t AcX_raw, AcY_raw, GyZ_raw;
int16_t AcXoffset, AcYoffset, GyZoffset;
float GyZ_integral, rotation;
unsigned long IMU_last_ts = 0;

void IMUwriteReg(byte reg, byte val) {
	Wire.beginTransmission(MPU);
	Wire.write(reg);
	Wire.write(val);
	Wire.endTransmission(true);
}

void init_IMU() {
	pinMode(MPU6050_VCC_PIN, OUTPUT); // Turn on the power for the Gyroscope module, using two arduino pins
	pinMode(MPU6050_GND_PIN, OUTPUT); // This is possible since the MPU6050 IMU can work with very little power
	digitalWrite(MPU6050_VCC_PIN, HIGH);
	digitalWrite(MPU6050_GND_PIN, LOW);

	Wire.begin(); // Initialise the I2C port
	Wire.setTimeout(5);

	for (int i = 0; i < 3; i++) { // Reset the IMU a few times
		IMUwriteReg(MPU6050_PWR_MGMT_1, bit(7));   // DEVICE_RESET to 1 (D7=1)
		delay(100);
	}
	IMUwriteReg(MPU6050_PWR_MGMT_1, bit(0) | bit(1));  // set clock source to Z Gyro (D0=D1=1, D2=0) and set SLEEP to zero (D6=0, wakes up the MPU-6050)
	IMUwriteReg(MPU6050_ACCEL_CONFIG, bit(3) | bit(4));  // set sensitivity to +-16G (D3=1, D4=1) and disable high pass filter (D0,D1,D2=0)
	IMUwriteReg(MPU6050_GYRO_CONFIG, bit(3) | bit(4));  // set sensitivity to +-2000deg/s (D3=1, D4=1)
	IMUwriteReg(MPU6050_SMPLRT_DIV, 0);  // set sampling rate to 1khz (1khz / (1 + 0) = 1000 Hz)
	IMUwriteReg(MPU6050_CONFIG, bit(0) | bit(5));  // disable digital low pass filter (D0=D1=D2=0) and EXT_SYNC to GYRO_ZOUT (D3=D4=0, D5=1)
}

bool read_IMU() {
	int16_t new_AcX, new_AcY, new_GyZ;
	Wire.beginTransmission(MPU);
	Wire.write(0x3B);  // starting with register 0x3D (ACCEL_YOUT_H)
	Wire.endTransmission(false);
	Wire.requestFrom(MPU, 14, true); // request a total of 14 registers

	// Receive and decode the response
	new_AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
	new_AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
	for (int i = 0; i < 8; i++) Wire.read(); // Discard 0x3F-0x46
	new_GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

	bool updated = (AcX_raw != new_AcX) || (AcY_raw != new_AcY) || (GyZ_raw != new_GyZ); // Check if value has changed

	AcX_raw = new_AcX;
	AcY_raw = new_AcY;
	GyZ_raw = new_GyZ;
	AcX = AcX_raw - AcXoffset;
	AcY = AcY_raw - AcYoffset;
	GyZ = GyZ_raw - GyZoffset;
	return updated;
}

void calibrate_IMU() {
	// Measure IMU sensor offsets (the robot must remain still)
	AcXoffset = 0;
	AcYoffset = 0;
	GyZoffset = 0;
	for (int i = 0; i < 10; i++) {
		while (read_IMU() == false) delay(10);
		AcXoffset += AcX_raw;
		AcYoffset += AcY_raw;
		GyZoffset += GyZ_raw;
	}
	AcXoffset /= 10;
	AcYoffset /= 10;
	GyZoffset /= 10;
	GyZ_integral = 0;
}

void integrate_IMU() {
	while (!read_IMU());
	unsigned long ts = micros();
	float dt = ((float)(ts - IMU_last_ts)) / 1000000.; // seconds
	if (dt > 0) {
		if (dt < 0.5) GyZ_integral += GyZ * dt;
		IMU_last_ts = ts;
		rotation = GyZ_integral * 2000. / 32768.; // +-2000 deg/s sensitivity; +-2^15 full scale
	}
}

void offset_IMU(float deg) {
	GyZ_integral += deg * 32768. / 2000.;
}

void zero_IMU() {
	GyZ_integral = 0;
}

//--------------------------
// **** begin MOTORS *******
//--------------------------
Servo L_servo, R_servo;
#define L_SERVO_MOTOR_PIN 8
#define R_SERVO_MOTOR_PIN 9
unsigned long motors_last_ts = 0;

int limit_angle(int deg) {
	return min(max(deg, 0), 180);
}

void actuate_motors(float distanceGoal, float targetAngleDeg) {
	L_servo.attach(L_SERVO_MOTOR_PIN);
	R_servo.attach(R_SERVO_MOTOR_PIN);

	float velocity = 10 * (distanceGoal > 0) - 8 * (distanceGoal < 0);
	float distance_integral = 0;

	offset_IMU(-targetAngleDeg);
	while (1) {
		integrate_IMU();
		unsigned long ts = micros();
		float dt = ((float)(ts - motors_last_ts)) / 1000000.; // seconds
		if (dt > 0) {
			if (dt < 0.5) distance_integral += 48 * dt;
			motors_last_ts = ts;
		}
		L_servo.write(limit_angle(90 - velocity - 0.5 * rotation));
		R_servo.write(limit_angle(90 + velocity - 0.5 * rotation));
		if (distanceGoal == 0) {
			if (abs(rotation) < 10) break;
		} else {
			if (distance_integral >= abs(distanceGoal)) break;
		}
	}

	L_servo.detach();
	R_servo.detach();
}


//--------------------------
// ****    MAIN         ****
//--------------------------

void setup() {
	delay(400);
	Serial.begin(19200);
	led(ON);
	init_IMU();
	pen_move(UP);
	init_ultrasound();
	calibrate_IMU();
	led(OFF);
	Serial.println("READY");
}


void loop() {
	if (Serial.available()) {
		led(ON);
		bool sendOK = false;
		char cmd[3];
		cmd[0] = Serial.read();
		cmd[1] = Serial.read();
		cmd[2] = '\0';
		if (strcmp(cmd, "PD") == 0) {
			pen_move(DOWN);
			Serial.println("OK");

		} else if (strcmp(cmd, "PU") == 0) {
			pen_move(UP);
			Serial.println("OK");

		} else if (strcmp(cmd, "FD") == 0) {
			actuate_motors(Serial.parseInt(), 0);
			Serial.println("OK");

		} else if (strcmp(cmd, "BK") == 0) {
			actuate_motors(-Serial.parseInt(), 0);
			Serial.println("OK");

		} else if (strcmp(cmd, "RT") == 0) {
			actuate_motors(0, -Serial.parseInt());
			Serial.println("OK");

		} else if (strcmp(cmd, "LT") == 0) {
			actuate_motors(0, Serial.parseInt());
			Serial.println("OK");

		} else if (strcmp(cmd, "OE") == 0) {
			int dist = measure_distance_cm_filtered(10);
			Serial.println(dist);
		}
		led(OFF);
	}
	integrate_IMU();
}

