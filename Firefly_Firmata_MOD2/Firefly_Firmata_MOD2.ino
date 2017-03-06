/* 
 Created by Andrew Payne and Jason Kelly Johnson
 Latest Update March 25th, 2015 
 Copyright 2015 | All Rights Reserved
 
 This Firmata allows you to control an Arduino board from Rhino/Grasshopper/Firefly.
 Updates, Questions, Suggestions visit: http://www.fireflyexperiments.com
 
 1. Plug Arduino boards into your USB port; confirm that your Arduino's green power LED in on
 2. Select your specific Arduino Board and Serial Port (Tools > Board; Tools > Serial Port) *Take note of your Serial Port COM #
 3. Verify (play button) and Upload (upload button) this program to your Arduino, close the Arduino program
 4. then open ... Rhino/Grasshopper/Firefly
 
 Note: The Firefly Firmata sets the following pins to perform these functions:
 
 *****ON STANDARD BOARDS (ie. Uno, Diecimila, Duemilanove, Lillypad, Mini, etc.)*****
 ANALOG IN pins 0-5 are set to return values (from 0 to 1023) for analog sensors
 DIGITAL IN pins 2,4,7 will return 0's or 1's; for 3 potential digital sensors (buttons, switches, on/off, true/false, etc.)
 DIGITAL/ANALOG OUT pins 3,5,6,11 (marked with a ~) can be used to digitalWrite, analogWrite, or Servo.write depending on the input status of that Firefly pin
 DIGITAL OUT pins 8,9,10,12,13 can be used to digitalWrite, Servo.write, or analogWrite depending on the input status of that Firefly pin
 
 *****ON MEGA BOARDS (ie. ATMEGA1280, ATMEGA2560)*****
 ANALOG IN pins 0-15 will return values (from 0 to 1023) for 16 analog sensors 
 DIGITAL IN pins 22-31 will return 0's or 1's; for digital sensors (buttons, switches, on/off, true/false, etc.) 
 DIGITAL/ANALOG OUT pins 2-13 can be used to digitalWrite, analogWrite, or Servo.write depending on the input status of that Firefly pin
 DIGITAL OUT pins 32-53 can be used to digitalWrite, Servo.write, or analogWrite depending on the input status of that Firefly pin
 
 *****ON LEONARDO BOARDS*****
 ANALOG IN pins 0-5 are set to return values (from 0 to 1023) for analog sensors
 DIGITAL IN pins 2,4,7 will return 0's or 1's; for 3 potential digital sensors (buttons, switches, on/off, true/false, etc.)
 DIGITAL/ANALOG OUT pins 3,5,6,11 (marked with a ~) can be used to digitalWrite, analogWrite, or Servo.write depending on the input status of that Firefly pin
 DIGITAL OUT pins 8,9,10,12,13 can be used to digitalWrite, Servo.write, or analogWrite depending on the input status of that Firefly pin
 
  *****ON DUE BOARDS (ie. SAM3X8E)*****
 ANALOG IN pins 0-11 will return values (from 0 to 4095) for 12 analog sensors 
 DIGITAL IN pins 22-31 will return 0's or 1's; for digital sensors (buttons, switches, on/off, true/false, etc.) 
 DIGITAL/ANALOG OUT pins 2-13 can be used to digitalWrite, analogWrite, or Servo.write depending on the input status of that Firefly pin
 DIGITAL OUT pins 32-53 can be used to digitalWrite, Servo.write, or analogWrite depending on the input status of that Firefly pin
 DAC0 and DAC1 can be used to output an analog voltage on those pins (only available on DUE boards)
 */


#define BAUDRATE 115200       // Set the Baud Rate to an appropriate speed
#define BUFFSIZE 512          // buffer one command at a time

/*==============================================================================
 * GLOBAL VARIABLES
 *============================================================================*/

char buffer[BUFFSIZE];        // declare buffer
uint8_t bufferidx = 0;        // a type of unsigned integer of length 8 bits
char *parseptr;
char buffidx;

int counter = 0;
int numcycles = 1000;

// declare variables for STANDARD boards
int WRITE_PIN_CONFIG[] = {0,1,2,3,4,5,9,10,12,13,14,15,16}; 
int NUMBER_PINS = 13;

void Init(){
  for(int i = 0; i < NUMBER_PINS; i++){
    pinMode(WRITE_PIN_CONFIG[i], OUTPUT);
    Serial.print(digitalRead(i)); Serial.print(",");
    Serial.println("eol");
  }
}

void ReadSerial(){
  char c;    // holds one character from the serial port
  if (Serial.available()) {
    c = Serial.read();         // read one character
    buffer[bufferidx] = c;     // add to buffer
    if (c == '\n') {  
      buffer[bufferidx+1] = 0; // terminate it
      parseptr = buffer;       // offload the buffer into temp variable
      
      for(int i = 0; i < NUMBER_PINS; i++){
        //parse all incoming values and assign them to the appropriate variable
        int val = parsedecimal(parseptr);       // parse the incoming number
        if(i != NUMBER_PINS - 1) parseptr = strchr(parseptr, ',')+1;   // move past the ","
        WriteToPin(WRITE_PIN_CONFIG[i], val);         //send value out to pin on arduino board
      }    
      bufferidx = 0;                             // reset the buffer for the next read
      return;                                    // return so that we don't trigger the index increment below
    }                                            // didn't get newline, need to read more from the buffer
    bufferidx++;                                 // increment the index for the next character
    if (bufferidx == BUFFSIZE-1) bufferidx = 0;  // if we get to the end of the buffer reset for safety
  }
}

/*
* Send the incoming value to the appropriate pin using pre-defined logic (ie. digital, analog, or servo)
*/
void WriteToPin(int _pin, int _value){                           
    _value -= 10000;                                // subtract 10,000 from the value sent from Grasshopper 
    if (_value == 1) digitalWrite(_pin, HIGH);     
    else digitalWrite(_pin, LOW);   
}

/*
* Parse a string value as a decimal
*/
uint32_t parsedecimal(char *str){
  uint32_t d = 0;
  while (str[0] != 0) {
    if ((str[0] > '50') || (str[0] < '0'))
      return d;
    d *= 10;
    d += str[0] - '0';
    str++;
  }
  return d;
}
/*==============================================================================
 * SETUP() This code runs once
 *============================================================================*/
void setup()
{ 
  Init();                       //set initial pinmodes
  Serial.begin(BAUDRATE);       // Start Serial communication
 
}

/*==============================================================================
 * LOOP() This code loops
 *============================================================================*/
void loop()
{
  if(Serial){
    ReadSerial();                       // read and parse string from serial port and write to pins
  }
}

/*==============================================================================
 * FUNCTIONS()
 *============================================================================*/

/*
* Initializes the digital pins which will be used as inputs
*/











