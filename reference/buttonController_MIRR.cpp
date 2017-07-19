#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>

#include <Wire.h>
#include "Adafruit_MCP23017.h"
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#include <OSCBoards.h>
#include <OSCBundle.h>
#include <OSCData.h>
#include <OSCMatch.h>
#include <OSCMessage.h>
#include <OSCTiming.h>

#define PIN 14

char ssid[] = "Balloon Network";          //  your network SSID (name) 
char pass[] = "balloons";   // your network password

//char ssid[] = "botcave";          //  your network SSID (name) 
//char pass[] = "12porcupines"; 

char* hostString = "buttonNode";
const unsigned int localPort = 5005;        // local port to listen for UDP packets (here's where we send the packets)

char messageBuffer[196]= {};  
bool buttonsPressed[98] = {};

unsigned long lightTimers_ms[98] = {};

unsigned long next_tx_ms = 0;
unsigned long next_rx_ms = 0;
int tx_interval_ms = 100;
int rx_interval_ms = 90;
int lightChange_interval_ms = 5000;


Adafruit_MCP23017 MCPArray[7] = {};
Adafruit_NeoPixel strip = Adafruit_NeoPixel(98, PIN, NEO_RGBW + NEO_KHZ800);

typedef struct
{
  char chipId;
  char pinNumber;
} pinInfo;

pinInfo buttonMapping[98] = {};


WiFiClient client;
WiFiUDP Udp;
IPAddress broadcastIP;
int destPort = 6001;

OSCErrorCode error;

void connectWiFi() {

  Serial.println("Attempting to connect to WPA network...");
  Serial.print("SSID: ");
  Serial.println(ssid);
  Serial.print("hostString: ");
  Serial.println(hostString);

  WiFi.hostname(hostString);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  broadcastIP = WiFi.localIP();
  broadcastIP[3] = 255;  // Works for networks with netmask 255.255.255.0

}

void startMDNS() {
  if (!MDNS.begin(hostString)) {
    Serial.println("Error setting up MDNS responder!");
  }
  Serial.println("mDNS responder started");
}

void populateButtonMapping() {
  int buttonPosition = 0;
  for (int i = 0; i < 6; i++){
    for (int j = 0; j < 15; j++){
      buttonMapping[buttonPosition].chipId = i;
      buttonMapping[buttonPosition].pinNumber = j;
      buttonPosition = buttonPosition + 1;
    }
  }
 
  for (int j = 0; j < 8; j++){
    if (buttonPosition == 98)
    {
      break;
    }
    buttonMapping[buttonPosition].chipId = 6;
    buttonMapping[buttonPosition].pinNumber = j;
    buttonPosition = buttonPosition + 1;
    }
}

void readButtons(){
  //mcp stuff goes in here
  for (int i = 0; i < 98; i++){
    pinInfo info = buttonMapping[i];
    buttonsPressed[i] = buttonsPressed[i] || MCPArray[info.chipId].digitalRead(info.pinNumber); 
    // Serial.print(i);
    // Serial.print(",");
    // Serial.print(MCPArray[info.chipId].digitalRead(info.pinNumber));
    // Serial.print(",");
    // Serial.print((int)info.chipId);
    // Serial.print(",");
    // Serial.print((int)info.pinNumber);
    // Serial.println();
    
  }
 // digitalWrite(LED_BUILTIN, MCPArray[buttonMapping.chipId].digitalRead(buttonMapping.pinNumber));
  
}

void clearButtons(){
  for (int i = 0; i < 98; i++){
    buttonsPressed[i] = false;
  }
}

void makeMessageBuffer() {
  int bufferPosition = 0;
  for (int i = 0; i < 98; i++){
    char theCharacter = '0';
    if (buttonsPressed[i] == true)
    {
      theCharacter = '1';       
    }
    messageBuffer[bufferPosition] = theCharacter;
    bufferPosition = bufferPosition + 1;
    messageBuffer[bufferPosition] = ',';
    bufferPosition = bufferPosition + 1;
  }
  messageBuffer[bufferPosition - 1] = 0;
}

int sendButtonState() {

  Udp.beginPacket(broadcastIP, destPort);
  Udp.write(messageBuffer);
  Udp.endPacket();

  //Serial.println(buttonBuffer);
}

void populateLightTimers() {
  int lightPosition = 0;
  for (int i = 0; i < 98; i++){
    if (buttonsPressed[i] == true ){
      lightTimers_ms[i] = millis() + lightChange_interval_ms;
    }else if (buttonsPressed[i] == false && lightTimers_ms[i] > millis()){
      lightTimers_ms[i] = lightTimers_ms[i];
    }else{
      lightTimers_ms[i] = millis();
    }
    lightPosition = lightPosition + 1;   
  }
}

void setLightColor() {
  for (int i=0; i<strip.numPixels(); i++){
    if (lightTimers_ms[i] > millis()){
      strip.setPixelColor(i, 0, 0, 0, 255);
    }else if (lightTimers_ms[86] > millis()
            &&lightTimers_ms[78] > millis()
            &&lightTimers_ms[70] > millis()
            &&lightTimers_ms[62] > millis()
            &&lightTimers_ms[54] > millis()
            &&lightTimers_ms[46] > millis()
            &&lightTimers_ms[39] > millis()
            &&lightTimers_ms[32] > millis()
            &&lightTimers_ms[25] > millis()
            &&lightTimers_ms[18] > millis()
            &&lightTimers_ms[11] > millis()
            &&lightTimers_ms[19] > millis()
            &&lightTimers_ms[27] > millis()
            &&lightTimers_ms[35] > millis()
            &&lightTimers_ms[43] > millis()
            &&lightTimers_ms[51] > millis()
            &&lightTimers_ms[58] > millis()
            &&lightTimers_ms[65] > millis()
            &&lightTimers_ms[72] > millis()
            &&lightTimers_ms[79] > millis()){
      theaterChase(strip.Color(0, 0, 0, 255));
      theaterChase(strip.Color(127, 0, 127, 0));
      theaterChase(strip.Color(0, 127, 127, 0));
    }else {  
      strip.setPixelColor(i, Wheel((i*2) & 255));
    }
  }
  strip.show();
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

void theaterChase(uint32_t c) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

void setup() {
  //return; 
  Serial.begin(115200); 
  //delay(100);

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("LED_BUILTIN enabled");
  digitalWrite(LED_BUILTIN, LOW);

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  populateButtonMapping();

  for (int i = 0; i < 7; i++){
    MCPArray[i].begin(i);
    for (int j = 0; j < 16; j++){
      MCPArray[i].pinMode(j, INPUT);
      MCPArray[i].pullUp(j, HIGH);
    }
    
  }
  
  connectWiFi();
  startMDNS();

  next_tx_ms = millis();
  next_rx_ms = millis();
}


void loop() {
  //return;  //debug
  if (next_rx_ms <= millis()) {
    next_rx_ms = next_rx_ms + rx_interval_ms; // Time to RX a status message
    readButtons();
    populateLightTimers();
    setLightColor();
  }
  if (next_tx_ms <= millis()) {
    next_tx_ms = next_tx_ms + tx_interval_ms; // Time to TX a status message
    makeMessageBuffer();
    sendButtonState();
    clearButtons();
  }
 
  delay(1);
}