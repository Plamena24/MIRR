#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>

#include <Wire.h>
#include "Adafruit_MCP23017.h"
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

/*#include <OSCBoards.h>
#include <OSCBundle.h>
#include <OSCData.h>
#include <OSCMatch.h>
#include <OSCMessage.h>
#include <OSCTiming.h>
*/
#define PIN 14

char ssid[] = "Balloon Network";          //  your network SSID (name) 
char pass[] = "balloons";   // your network password

//char ssid[] = "botcave";          //  your network SSID (name) 
//char pass[] = "12porcupines"; 

char* hostString = "buttonNode";
const unsigned int localPort = 5005;        // local port to listen for UDP packets (here's where we send the packets)

char messageBuffer[196]= {};  
bool buttonsPressed[98] = {};

unsigned long next_tx_ms = 0;
unsigned long next_rx_ms = 0;
int tx_interval_ms = 100;
int rx_interval_ms = 10;

Adafruit_MCP23017 MCPArray[7] = {};
Adafruit_NeoPixel strip = Adafruit_NeoPixel(88, PIN, NEO_RGBW + NEO_KHZ800);

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

//OSCErrorCode error;

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
    for (int j = 0; j < 16; j++){
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
    Serial.print(i);
    Serial.print(",");
    Serial.print(MCPArray[info.chipId].digitalRead(info.pinNumber));
    Serial.print(",");
    Serial.print((int)info.chipId);
    Serial.print(",");
    Serial.print((int)info.pinNumber);
    Serial.println();
    
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

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

void setup() {
  //return; 
  Serial.begin(115200);
  delay(100);

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
  }
  if (next_tx_ms <= millis()) {
    next_tx_ms = next_tx_ms + tx_interval_ms; // Time to TX a status message
    makeMessageBuffer();
    sendButtonState();
    clearButtons();
  }
  rainbow(20);
 // delay(1);
}

