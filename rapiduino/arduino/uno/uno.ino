
//Define the acknowledgement bytes

int versionMajor = 0;
int versionMinor = 1;
int versionPatch = 0;

#define ackBadCommand (byte)0
#define ackGoodCommand 1
#define ackData 2

int recvByte;

void setup(){
  Serial.begin(9600);

  //pinMode(beepPin,OUTPUT);
  //digitalWrite(beepPin,LOW);

}

void loop(){

  //Wait for information to become available
  while(!Serial.available());

  //Receive the Command Byte
  recvByte = Serial.read();

  //Polling
  if(recvByte==0){
    Serial.write(ackGoodCommand);
  }

  //Versioning
  else if(recvByte==1){
    Serial.write(ackGoodCommand);
    Serial.write(versionMajor);
    Serial.write(versionMinor);
    Serial.write(versionPatch);
  }
  //Arduino Version
  else if(recvByte==2){
    Serial.write(ackGoodCommand);
    Serial.write(11);
    Serial.print("Arduino Uno");
  }
  else{
    Serial.write(ackBadCommand);
  }

}
