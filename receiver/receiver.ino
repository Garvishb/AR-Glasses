/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-two-way-communication-esp32/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <esp_now.h>
#include <WiFi.h>


// REPLACE WITH THE MAC Address of your receiver 
uint8_t broadcastAddress[] = {0x34, 0x85, 0x18, 0xac, 0x08, 0x28};
//34:85:18:ac:08:28 is for the transmitter ESP

// Define variables to store incoming readings
char incomingChar;

//Structure example to send data
//Must match the receiver structure
typedef struct struct_message {
    char character;
} struct_message;


// Create a struct_message to hold incoming sensor readings
struct_message incomingCharacter;

esp_now_peer_info_t peerInfo;


// Callback when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&incomingCharacter, incomingData, sizeof(incomingCharacter));
  // Serial.print("Bytes received: ");
  // Serial.println(len);
  incomingChar = incomingCharacter.character;
  Serial.print("incoming char: ");
  Serial.println(incomingChar);
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(9600);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

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
}
 
void loop() {

   
}