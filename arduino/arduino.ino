/*
   RAPIDUINO

   For use with the Rapiduino Python Library
   https://github.com/samwedge/rapiduino

   Copyright (c) 2017 Samuel Wedge
*/

char versionMajor = 0;
char versionMinor = 1;
char versionMicro = 0;

char cmdByte;
char pinNum;
char dataByte;

void sendByte(char databyte) {
  Serial.write(databyte);
  return;
}

char recvByte() {
  while (!Serial.available());
  return Serial.read();
}

void setup() {
  Serial.begin(115200);
}

void loop() {

  // Receive the Command Byte
  cmdByte = recvByte();

  // poll
  if (cmdByte == 0) {
    sendByte(1);
  }

  // parrot
  if (cmdByte == 1) {
    char dataByte = recvByte();
    Serial.write(dataByte);
  }

  // version
  if (cmdByte == 2) {
    sendByte(versionMajor);
    sendByte(versionMinor);
    sendByte(versionMicro);
  }

  // pinMode
  if (cmdByte == 10) {
    pinNum = recvByte();
    dataByte = recvByte();
    if (dataByte == 0) {
      pinMode(pinNum, INPUT);
    }
    else if (dataByte == 1) {
      pinMode(pinNum, OUTPUT);
    }
    else if (dataByte == 2) {
      pinMode(pinNum, INPUT_PULLUP);
    }
  }

  // digitalRead
  if (cmdByte == 20) {
    pinNum = recvByte();
    dataByte = digitalRead(pinNum);
    if (dataByte == LOW) {
      Serial.write(0);
    }
    else if (dataByte == HIGH) {
      Serial.write(1);
    }
  }

  // digitalWrite
  if (cmdByte == 21) {
    pinNum = recvByte();
    dataByte = recvByte();
    if (dataByte == 0) {
      digitalWrite(pinNum, LOW);
    }
    else if (dataByte == 1) {
      digitalWrite(pinNum, HIGH);
    }
  }

  // analogRead
  if (cmdByte == 30) {
    pinNum = recvByte();
    dataByte = analogRead(pinNum);
    Serial.write(dataByte);
  }

  // analogWrite
  if (cmdByte == 31) {
    ;
    pinNum = recvByte();
    int value = recvByte();
    analogWrite(pinNum, value);
  }

}
