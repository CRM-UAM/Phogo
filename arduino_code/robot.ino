// This source file is part of the Phogo project
// https://github.com/CRM-UAM/Phogo
// Released under the GNU General Public License Version 3
// Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

// Derived from: MPU-6050 Short Example Sketch by Arduino User JohnChi

//#include<Wire.h>
#include <SoftwareWire.h> // Using a virtual I2C port allows to plug the gyroscope module directly into the analog pins
// This is a hack that powers the gyroscope module with two digital pins, 1 (5V) and 0 (gnd)

SoftwareWire Wire(A3,A2);

const int MPU=0x68;  // I2C address of the MPU-6050

#define MPU6050_PWR_MGMT_1    0x6B
#define MPU6050_ACCEL_CONFIG  0x1C
#define MPU6050_GYRO_CONFIG   0x1B
#define MPU6050_SMPLRT_DIV    0x19
#define MPU6050_CONFIG        0x1A

void init_IMU() {
  for(int i=0; i<3; i++) { // Reset the IMU a few times
    IMUwriteReg(MPU6050_PWR_MGMT_1, bit(7) );  // DEVICE_RESET to 1 (D7=1)
    delay(100);
  }
  IMUwriteReg(MPU6050_PWR_MGMT_1, bit(0) | bit(1) ); // set clock source to Z Gyro (D0=D1=1, D2=0) and set SLEEP to zero (D6=0, wakes up the MPU-6050)
  IMUwriteReg(MPU6050_ACCEL_CONFIG, bit(3) | bit(4) ); // set sensitivity to +-16G (D3=1, D4=1) and disable high pass filter (D0,D1,D2=0)
  IMUwriteReg(MPU6050_GYRO_CONFIG, bit(3) | bit(4) ); // set sensitivity to +-2000deg/s (D3=1, D4=1)
  IMUwriteReg(MPU6050_SMPLRT_DIV, 0 ); // set sampling rate to 1khz (1khz / (1 + 0) = 1000 Hz)
  IMUwriteReg(MPU6050_CONFIG, bit(0) | bit(5) ); // disable digital low pass filter (D0=D1=D2=0) and EXT_SYNC to GYRO_ZOUT (D3=D4=0, D5=1)
}

int16_t AcY, GyZ;
int16_t GyZoffset;
float GyZ_integral;

unsigned long prev_ts;

void IMUwriteReg(byte reg, byte val) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission(true);
}

void setup() {
  pinMode(A0,OUTPUT);// Turn on the power for the Gyroscope module
  pinMode(A1,OUTPUT);
  digitalWrite(A1,LOW);
  digitalWrite(A0,HIGH);

  delay(400);

  Wire.begin();
  Wire.setTimeout(5);
  init_IMU();
  
  Serial.begin(115200);
  delay(1000);
  
  // Measure IMU sensor offsets (robot must remain still)
  AcYoffset = 0;
  GyZoffset = 0;
  for(int i=0; i<10; i++) {
    readIMU(&AcY, &GyZ);
    GyZoffset += GyZ;
  }
  GyZoffset /= 10;
  //Serial.println("Gyro offset:");
  //Serial.println(GyZoffset);
  
  prev_ts = millis();
  
  GyZ_integral = 0;
}

void readIMU(int16_t *AcY, int16_t *GyZ) {
  Wire.beginTransmission(MPU);
  Wire.write(0x3D);  // starting with register 0x3D (ACCEL_YOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,12,true);  // request a total of 12 registers
  *AcY = Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  for(int i=0; i<8; i++) Wire.read(); // Discard 0x3F-0x46
  *GyZ = Wire.read()<<8 | Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}


void loop() {
  readIMU(&AcY, &GyZ);
  unsigned long ts = micros();
  float dt = ((float)(ts-prev_ts))/1000000.;
  if(dt > 0) GyZ_integral += (GyZ-GyZoffset)*dt;
  
  float rotation = GyZ_integral*2000./32768.; // +-2000 deg/s sensitivity; +-2^15 full scale
  
  int rot_error = max(min(round(255.*rotation/90.),255),-255);
  int dist_error = max(min(round(255.*(40-1000*linear_motion)/300.),255),-255);
  
  if((iter % 10) == 0) {
    Serial.print(rotation);
    Serial.print("\t");
    Serial.println(linear_motion);
  }
  prev_ts = ts;
  iter++;
  delay(10);
}

