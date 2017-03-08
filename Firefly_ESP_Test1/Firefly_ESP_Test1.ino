/* 
 Modified by Plamena Milusheva from Firefly_Firmata by Andrew Payne and Jason Kelly Johnson
 Latest Update March 10th, 2017 
 
 This code allows you to control servos with a NodeMCU 1.0 board from Rhino/Grasshopper/Firefly using the Adafruit PWMServoDriver library.
 Updates, Questions, Suggestions visit: http://www.fireflyexperiments.com
 
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//define driver objects
Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(0x40);
//Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);

#define BAUDRATE 115200       // Set the Baud Rate to an appropriate speed
#define BUFFSIZE 512          // buffer one command at a time

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  175 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  625 // this is the 'maximum' pulse length count (out of 4096)
/*==============================================================================
 * GLOBAL VARIABLES
 *============================================================================*/

char buffer[BUFFSIZE];        // declare buffer
uint8_t bufferidx = 0;        // a type of unsigned integer of length 8 bits
char *parseptr;
char buffidx;

int counter = 0;
int numcycles = 1000;
int servonum = 0;


void ReadSerial(){
  char c;    // holds one character from the serial port
  if (Serial.available()) {
    c = Serial.read();         // read one character
    buffer[bufferidx] = c;     // add to buffer
    if (c == '\n') {  
      buffer[bufferidx+1] = 0; // terminate it
      parseptr = buffer;       // offload the buffer into temp variable
      
      //parse all incoming values and assign them to the appropriate variable
      int val = parsedecimal(parseptr);          // parse the incoming number
      WriteToESP(val);      //send value out to pin on arduino board
           
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
void WriteToESP(int _value){                           
    int pulselen = map(_value, 0, 180, SERVOMIN, SERVOMAX);
    for (servonum; servonum < 16; servonum ++) {
      pwm0.setPWM(servonum, 0, pulselen);
    }
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
  Serial.begin(BAUDRATE);       // Start Serial communication

  //initialize driver objects
  pwm0.begin();
  //pwm1.begin();

  pwm0.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  //pwm1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  yield();
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











