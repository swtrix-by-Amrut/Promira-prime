/*
  SCP1000 sensor attached to pins 6, 7, 10 - 13:
  DRDY: pin 6
  CSB: pin 7
  MOSI: pin 11
  MISO: pin 12
  SCK: pin 13
*/
#include <SPI.h>

byte dataToSend;
unsigned long int result;
byte inByte;

const int chipSelectPin = 10;

bool echoFlag = false;

int SPI_CLK_Pin = 13;

int a, index0 = 0;
char inp_char = '8';
char serial_inp_string[] = "1912i1o122";
char command_str[] = "r 12";
char command_str2[] = "w 12 34";
bool readwrtie_flag = false, valid_data = false;
int regH = 0, regL = 0, i = 0;

int hexA, hexB, hexAB;
byte hex_val, hex_val2;

void setup() {
  Serial.begin(115200);
  SPI.begin();


  index0 = 0;




  while (Serial.available() == 0) { ; }
  inp_char = Serial.read();
  if (inp_char != '~' && inp_char != '^') {
    while (1) {
      Serial.println("..... Invalid access .....");
      delay(500);
    }
  }
  if (inp_char == '^') {
    echoFlag = true;
  }
  if (echoFlag) { Serial.println("UART is now active!!"); }
  else      { Serial.println("K"); }
}

void loop() {
  // int tempData = readRegister(0x21, 2);


  //=====================================================
  if (Serial.available() > 0) {
    inp_char = Serial.read();
    if (inp_char == 10 or index0 > 8) {
      serial_inp_string[index0] = '\0';
      index0 = -1;
      //Serial.print (serial_inp_string);
    } else {
      serial_inp_string[index0] = inp_char;
      index0 += 1;
    }
  }  // end serial-if
  //=====================================================
  if (index0 == -1) {
    if (echoFlag) { Serial.println(serial_inp_string); }
    index0 = 0;
    valid_data = true;
    if (serial_inp_string[0] == 'w') {
      readwrtie_flag = false;
      copy_str(command_str2, serial_inp_string);
      for (i = 2; i < 6; i++) {
        if ((command_str2[i] <= 57 && command_str2[i] >= 48) || (command_str2[i] <= 70 && command_str2[i] >= 65)) {
          //valid_data =  valid_data && true;
          regH = command_str2[i] - '0';
        } else {
          valid_data = false;
        }
      }
    } else if (serial_inp_string[0] == 'r') {
      readwrtie_flag = true;
      copy_str(command_str, serial_inp_string);
      for (i = 2; i < 4; i++) {
        if ((command_str[i] <= 57 && command_str[i] >= 48) || (command_str[i] <= 70 && command_str[i] >= 65)) {
          regH = command_str[i] - '0';
        } else {
          valid_data = false;
        }
      }
    } else {
      valid_data = false;
    }
    if (valid_data == true) {
      if (echoFlag) { Serial.print("You entered: "); }
      if (readwrtie_flag) {
        if (echoFlag) { Serial.println(command_str); }
        int tempData = readRegister();
        Serial.println(tempData, HEX);
      } else {
        if (echoFlag) {
          Serial.println(command_str2);
          //get_hxnum(command_str2[2], command_str2[3]);
          //Serial.print(hexAB, HEX);
          Serial.println("writing...");
        }
        writeRegister();
      }
    } else {
      if (echoFlag) { Serial.println("invalid cmd"); }
    }

  }  // end if 2
  //=====================================================
}
unsigned int readRegister() {
  result = 0;
  dataToSend = 0x90;
  get_hxnum(command_str[2], command_str[3]);
  hex_val = hexAB;

  //Serial.println (hex_val, HEX);

  SPI.beginTransaction(SPISettings(125000, MSBFIRST, SPI_MODE3));
  digitalWrite(chipSelectPin, LOW);
  delay(200);
  SPI.transfer(dataToSend);
  SPI.transfer(hex_val);
  result = SPI.transfer(0x00);
  digitalWrite(chipSelectPin, HIGH);
  SPI.endTransaction();
  return (result);
}
void writeRegister() {
  dataToSend = 0x10;
  get_hxnum(command_str2[2], command_str2[3]);
  hex_val2 = hexAB;
  get_hxnum(command_str2[4], command_str2[5]);
  hex_val = hexAB;

  /*
  SPI.beginTransaction(SPISettings(125000, MSBFIRST, SPI_MODE3));
  digitalWrite(chipSelectPin, LOW);
  delay(100);
  SPI.transfer(dataToSend);
  SPI.transfer(hex_val2);
  SPI.transfer(hex_val);
  digitalWrite(chipSelectPin, HIGH);
  SPI.endTransaction();
  */




  //Serial.println (hex_val2, HEX);
  //Serial.println (hex_val, HEX);
  SPI.beginTransaction(SPISettings(125000, MSBFIRST, SPI_MODE3));
  digitalWrite(chipSelectPin, LOW);
  delay(200);
  SPI.transfer(dataToSend);
  SPI.transfer(hex_val2);
  SPI.transfer(hex_val);
  digitalWrite(chipSelectPin, HIGH);
  SPI.endTransaction();
}
void copy_str(char s1[], char s2[]) {
  bool loopflag = true;
  for (int i = 0; i < 20; i++) {
    if (s2[i] == '\0') {
      loopflag = false;
    }
    if (s1[i] == '\0') {
      break;
    }
    if (loopflag) {
      s1[i] = s2[i];
    } else {
      s1[i] = ' ';
    }
  }
}
void get_hxnum(char a, char b) {
  hexA = -1;
  hexB = -1;
  hexAB = 0;
  if (a <= 57 && a >= 48) {
    hexA = a - '0';
  } else if (a <= 70 && a >= 65) {
    hexA = a - 55;
  }
  if (b <= 57 && b >= 48) {
    hexB = b - '0';
  } else if (b <= 70 && b >= 65) {
    hexB = b - 55;
  }
  hexAB = hexA * 16 + hexB;
}
