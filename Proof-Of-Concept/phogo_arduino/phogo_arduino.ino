
void setup() {
  Serial.begin(19200);
  pinMode(13, OUTPUT);
}

void loop() {
  if(Serial.available()) {
    char command = '\n';
    while(command == '\n' || command == '\r' || command == ' ') command = Serial.read();
    int param = Serial.parseInt();
    switch(command) {
      case 'l':
        if(param == 0 || param == 1)
          digitalWrite(13, param);
        break;
      case 'p':
        if(param > 0 && param < 10000)
          delay(param);
        break;
      default:
        break;
    }
  }
}

