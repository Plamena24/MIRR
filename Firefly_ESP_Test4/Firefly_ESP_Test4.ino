/* 
 Modified by Plamena Milusheva from Firefly_Firmata by Andrew Payne and Jason Kelly Johnson
 Latest Update March 10th, 2017 
 
 This code allows you to control servos with a NodeMCU 1.0 board from Rhino/Grasshopper/Firefly using the Adafruit PWMServoDriver library.
 Updates, Questions, Suggestions visit: http://www.fireflyexperiments.com
 
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//define driver objects
//Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);

#define BAUDRATE 115200       // Set the Baud Rate to an appropriate speed


// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  160 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  560 // this is the 'maximum' pulse length count (out of 4096)
/*==============================================================================
 * GLOBAL VARIABLES
 *============================================================================*/



int servonum = 0;
int angle = 0;


void ReadSerial(){
  if (Serial.find("s")) {
    angle = Serial.parseInt();
    WriteToESP(angle);
  }
  
}

/*
* Send the incoming value to the appropriate pin using pre-defined logic (ie. digital, analog, or servo)
*/
void WriteToESP(double _value){                           
    //int pulselen = map(_value, 0, 180, SERVOMIN, SERVOMAX);
    double pulselen = _value;
    Serial.println(pulselen);
    for (int i = 0;i < 16; i++) {
     setServoPulse(i, pulselen);
    }
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000;
  pulse /= pulselength;
  Serial.println(pulse);
  pwm1.setPWM(n, 0, pulse);
}

/*==============================================================================
 * SETUP() This code runs once
 *============================================================================*/
void setup()
{ 
  Serial.begin(BAUDRATE);       // Start Serial communication

  //initialize driver objects
  //pwm0.begin();
  pwm1.begin();

  //pwm0.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  pwm1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

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











