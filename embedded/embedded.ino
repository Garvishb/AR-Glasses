#define NUM_ROWS_MAX 5
#define CHAR_WIDTH 6
#define CHAR_HEIGHT 8
#define WHITESPACE_PERCENTAGE 0.2
int numCharsPerRow = (128 / CHAR_WIDTH) * 0.5;
//  * (1 - 3 * WHITESPACE_PERCENTAGE);

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#include <esp_now.h>
#include <WiFi.h>

#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;


//--------FOR ESP NOW
// REPLACE WITH THE MAC Address of your receiver 
uint8_t broadcastAddress[] = {0x34, 0x85, 0x18, 0xac, 0x08, 0x28};
//34:85:18:ac:08:28 is for the transmitter ESP

// Define variables to store incoming readings
String incomingChar;

//Structure example to send data
//Must match the receiver structure
typedef struct struct_message {
    String character;
} struct_message;

// Create a struct_message to hold incoming sensor readings
struct_message incomingCharacter;

esp_now_peer_info_t peerInfo;


// Callback when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len);
 
///---end of ESP NOW


const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

float beatsPerMinute;
int beatAvg = 80;

bool isWiredConnection = false;

/* Uncomment the initialize the I2C address , uncomment only one, If you get a totally blank screen try the other*/
#define i2c_Address 0x3c //initialize with the I2C addr 0x3C Typically eBay OLED's
//#define i2c_Address 0x3d //initialize with the I2C addr 0x3D Typically Adafruit OLED's

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1   //   QT-PY / XIAO

Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


void setup()   {
  Wire.begin(D4, D5); //6,7 for c3
  Serial.begin(9600);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  delay(250); // wait for the OLED to power up
  display.begin(i2c_Address, true); // Address 0x3C default
  //display.setContrast (0); // dim display

  // Clear the buffer.
  display.clearDisplay();

  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);


  
  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Register for a callback function that will be called when data is received
  esp_now_register_recv_cb(OnDataRecv);



  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
}

String printBuffer;

int lastDeletedTime = millis();

void loop() {

  // text display tests
  // display.setTextSize(1);
  // display.setTextColor(SH110X_WHITE);
  // display.setCursor(0, 0);
  // display.setTextColor(SH110X_BLACK, SH110X_WHITE); // 'inverted' text
  // display.println(3.141592);

  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true)
  {

    //We sensed a beat!
    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 150 && beatsPerMinute > 50)
    {

      rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
      rateSpot %= RATE_SIZE; //Wrap variable

      //Take average of readings
      // beatAvg = 80;
      for (byte x = 0 ; x < RATE_SIZE ; x++)
      beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
      
    }
  }  
  
  display.clearDisplay();

  ////if (irValue < 50000)k
    ////Serial.print(" No finger?");
  if(irValue > 50000){
    // display.setCursor(90, 54);
    display.setCursor(10, 54);
    display.print(String(beatAvg) + "BPM");
  }


  while(Serial.available() > 0){
    char incomingChar = Serial.read();
    
    // Serial.print("X: ");
    // Serial.print(display.getCursorY());
    // Serial.print(", Y: ");
    // if(incomingChar != '\n'){
      printBuffer.concat(incomingChar);
    // }
    // Serial.println(display.getCursorX());
    // Serial.print(printBuffer);
    isWiredConnection = true;
    lastDeletedTime = millis();
  }


  
  // if(isWiredConnection){
  //   display.print("Wired");
  // }
  // else{
  //   display.print("Wireless");
  // }

  // Serial.println(isWiredConnection);
  

  if (printBuffer.length() > NUM_ROWS_MAX * numCharsPerRow || millis() - lastDeletedTime > 3000){
    //go until min length 
    //(printBuffer.length() - NUM_ROWS_MAX * numCharsPerRow); //if a longer than 13 char string comes in, I might need to remove more than 1 row. 
    printBuffer = printBuffer.substring(numCharsPerRow);
    lastDeletedTime = millis();
  }

  
  for(int i = 0; i < printBuffer.length() ; i++){
    int x = (i % numCharsPerRow) * CHAR_WIDTH + 10;
    int y = (i / numCharsPerRow) * CHAR_HEIGHT + CHAR_HEIGHT;
    display.setCursor(x, y);
    display.write(printBuffer[i]);
  } 
  display.display();
 
  //each row displays 21 characters -> say we leave a 20% buffer on each side. we start the cursor at 25 pixels, then we know we printed a whole row when we print 13 characters.

  // display.clearDisplay();

  // miniature bitmap display
  // display.drawBitmap(30, 16,  logo16_glcd_bmp, 16, 16, 1);
  // display.display();
  // delay(1);

  // invert the display
  // display.invertDisplay(true);
  // delay(1000);
  // display.invertDisplay(false);
  // delay(1000);
  // display.clearDisplay();
}

// void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
//   memcpy(&incomingCharacter, incomingData, sizeof(incomingCharacter));
//   // Serial.print("Bytes received: ");
//   // Serial.println(len);
//   // callback when data is recv from Master

//   incomingChar = incomingCharacter.character;
//   //// Serial.print("incoming char: ");
//   Serial.println(incomingChar);
  
    
//   ////Serial.print("X: ");
//   ////Serial.print(display.getCursorY());
//   ////Serial.print(", Y: ");
//   // if(incomingChar != '\n'){
//   printBuffer.concat(incomingChar);
//   // }
//   ////Serial.println(display.getCursorX());
//   Serial.println(printBuffer);
//   isWiredConnection = false;
//   lastDeletedTime = millis();
// }

void OnDataRecv(const uint8_t *mac_addr, const uint8_t *data, int data_len) {
   char* buff = (char*) data;
  String buffStr = String(buff);
  Serial.println(buffStr);

  printBuffer.concat(buffStr + "   ");
  // }
  ////Serial.println(display.getCursorX());
  Serial.println(printBuffer);
  isWiredConnection = false;
  lastDeletedTime = millis();
}