#include "SPI.h"
const int SSPin = 7;
const int CEPin = 8;
const int IRQPin = 6;
const int PKTLEN = 14;
const int VMAJ = 1;
const int VMIN = 1;

char command;
byte channel;
byte address[5];
byte buft[PKTLEN+1];

void setup() {
  Serial.begin(9600);
  pinMode (SSPin, OUTPUT);
  digitalWrite(SSPin,HIGH); 
  pinMode (CEPin, OUTPUT);
  digitalWrite(CEPin,LOW); 
  pinMode (IRQPin, INPUT);
  // initialize SPI:
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV128);
  SPI.setDataMode(SPI_MODE0);
  SPI.setBitOrder(MSBFIRST);
}

void loop() {
  int i;
  if (Serial.available()) {
    command = Serial.read();
    switch (command) {
    case '.':
      break;
    case 't':
      transmit();
      if(readStatus()&32) {
        Serial.println("ok");
      } else {
        delay(2);
        if(readStatus()&32) {
          Serial.println("ok");
        } else {
          Serial.println("fail");
          flushTx();
        }
      }
      clearIrqs();
      break;
    case 'b':
      for (i=0; i<PKTLEN; i++) {
        buft[i] = (byte)Serial.parseInt();
      }
      Serial.println("ok");
      break;
    case 'a':
      for (i=0; i<5; i++) {
        address[i] = (byte)Serial.parseInt();
      }
      writeAddresses();
      Serial.println("ok");
      break;
    case 'c':
      channel = (byte)Serial.parseInt();
      writeChannel();
      Serial.println("ok");      
    case 'h':
      Serial.print(VMAJ);
      Serial.print(".");
      Serial.print(VMIN);
      if (readStatus() == 14) {
        Serial.println("ok");
      } else {
        Serial.println("fail");
      }
      break;
    case 's':
      Serial.println(readStatus(),HEX);
      break;
    case 'q':
      clearIrqs();
      Serial.println("ok");
      break;
    case 'f':
      flushTx();
      flushRx();
      Serial.println("ok");
      break;
    case 'r':
      Serial.println(readRegByte((byte)Serial.parseInt()),HEX);
      break;
    default:
      Serial.print("unknown: ");
      Serial.println(command);
    }
  }
}

byte readStatus() {
  return singleCommand(255);
}

void flushTx() {
  singleCommand(225);
}

void flushRx() {
  singleCommand(226);
}

byte singleCommand(byte cmd) {
  byte ret;
  digitalWrite(SSPin,LOW);
  ret = SPI.transfer(cmd);
  digitalWrite(SSPin,HIGH); 
  return ret;  
}

void writeConf(byte conf) {
  writeRegByte(0, conf);
}

void writeChannel() {
  writeRegByte(5, channel);
}

void clearIrqs() {
  writeRegByte(7, 112);
}


void transmit() {
  writeConf(10);
  writePayload();
  digitalWrite(CEPin,HIGH); 
  delayMicroseconds(50);
  digitalWrite(CEPin,LOW);   
}


byte readRegByte(byte addr) {
  byte ret;
  digitalWrite(SSPin,LOW);
  SPI.transfer(addr&31);
  ret = SPI.transfer(0);
  digitalWrite(SSPin,HIGH); 
  return ret;
}

void writeRegByte(byte addr, byte value) {
  digitalWrite(SSPin,LOW);
  SPI.transfer((addr&31)|32);
  SPI.transfer(value);
  digitalWrite(SSPin,HIGH); 
}

void writePayload() {
  digitalWrite(SSPin,LOW);
  SPI.transfer(160);
  for (int i=0; i<PKTLEN; i++) {
    SPI.transfer(buft[i]);
  }
  digitalWrite(SSPin,HIGH); 
}

void writeAddresses() {
  digitalWrite(SSPin,LOW);
  SPI.transfer(48);
  for (int i=0; i<5; i++) {
    SPI.transfer(address[i]);
  }
  digitalWrite(SSPin,HIGH); 
  digitalWrite(SSPin,LOW);
  SPI.transfer(42);
  for (int i=0; i<5; i++) {
    SPI.transfer(address[i]);
  }
  digitalWrite(SSPin,HIGH); 
}

