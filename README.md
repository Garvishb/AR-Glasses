# AR-Glasses

- textconverter files trancribe realtime speech to text and we use different APIs to translate it to different language:
  - textconverter_openai uses ChatGPT API for translation
  - textconverter_google_translate uses Google Cloud API for translation
- The reciever and transmitter folders contain the code for ESP32 S3 microcontrollers to transmit speech data from a mic to the AR Glasses
