// This source file is part of the Phogo project
// https://github.com/CRM-UAM/Phogo
// Released under the GNU General Public License Version 3
// Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain


//--------------------------
// **** begin GYROSCOPE ****
//--------------------------
// Gyroscope code derived from: MPU-6050 Short Example Sketch by Arduino User JohnChi

//#include<Wire.h>
#include <SoftwareWire.h> // Using a virtual I2C port and 5V power through two digital pins,
// allows to plug the gyroscope module directly into a row of pins, without the need for extra wires

SoftwareWire Wire(A3,A2); // A3 as SDA, A2 as SCL

const int MPU=0x68;  // I2C address of the MPU-6050

#define MPU6050_PWR_MGMT_1    0x6B
#define MPU6050_ACCEL_CONFIG  0x1C
#define MPU6050_GYRO_CONFIG   0x1B
#define MPU6050_SMPLRT_DIV    0x19
#define MPU6050_CONFIG        0x1A

void IMUwriteReg(byte reg, byte val) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission(true);
}

void init_IMU() {
  pinMode(A0,OUTPUT);// Turn on the power for the Gyroscope module
  pinMode(A1,OUTPUT);// using two arduino pins: A0 as 5V, and A1 as GND
  digitalWrite(A0,HIGH);
  digitalWrite(A1,LOW);
  
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


bool readIMU() {
  int16_t new_AcX, new_AcY, new_GyZ;
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3D (ACCEL_YOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 14, true); // request a total of 14 registers
  new_AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  new_AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  for (int i = 0; i < 8; i++) Wire.read(); // Discard 0x3F-0x46
  new_GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  bool updated = (AcX != new_AcX) || (AcY != new_AcY) || (GyZ != new_GyZ); // Check if value has changed

  AcX = new_AcX;
  AcY = new_AcY;
  GyZ = new_GyZ;
  return updated;
}

int16_t AcY, GyZ;
int16_t GyZoffset;
float GyZ_integral;
//--------------------------
// **** end GYROSCOPE ****
//--------------------------


unsigned long prev_ts;


//--------------------------
// ****    MAIN         ****
//--------------------------
void setup() {

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

