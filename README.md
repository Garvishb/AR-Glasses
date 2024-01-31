# MediLens
## Inspiration
We were inspired by one of our close friends, who suffers from moderate autism spectrum disorder, as well as many others on the autism spectrum. Oftentimes, he would struggle with visual and audio sensory overload, where he feels overwhelmed by the sheer amount of sensory input coming from the outside world. This motivated us to create a gadget that would make a change in his life and the world. 

## What it does
Hence, we created an AR goggle device that caters towards as many people with ASD as possible, by limiting the amount of visual and audio sensory overload. We created an AR goggle on top of sunglasses and noise cancelling earbuds, which transcribes conversations into a caption, which the user can read instead. This creates a relative safe space for the user, within which the person is able to separate themselves as much as they want from the external world, while still maintaining contact and holding conversations. Additionally, the goggles can provide real-time translation of these captions, which increases accessibility for the spectrum of users. Further, it has a heart rate sensor, which is directly displayed at all times on the AR glasses. This provides crucial information for some people on the spectrum, as research has linked autism with a greater likelihood of having cardiovascular issues. 

## How we built it
The AR goggles were created using an SH1106 1.3" OLED screen with a mirror to project the screen onto the surface of the sunglasses. To fine tune the angle and the distances perfectly for a clear image, we used Fusion 360 and a 3D printer.  

The screen is driven by a XIAO ESP32 S3, which is the brain of the operation. It consolidates sensory data from the heart rate sensor and displays it onto the screen.

For real-time transcribing of speech, we used a microphone connected to the Assembly AI API, which handles the speech-to-text translation. The text is then sent to the GPT-4 API for translation into virtually any language. Afterwards, the text is communicated wirelessly to the goggles through a WiFi protocol called ESP-NOW to be displayed on the screen. 


## Challenges we ran into
- Getting a clear image from the AR goggles was an incredibly difficult task, due to the complex nature of the optics and clearance issues with the mirror and the screen touching the user's face. This was solved by iteratively creating 10+ prototypes with the 3D printer. We also experimented with various mirror sizes and a magnifying lens on the surface of the sunglasses. Ultimately, we ended up with a design with no magnifying lens as that provided a clearer and brighter picture.

- The ESP-NOW wireless communication protocol was a big challenge to work with. It was difficult to ensure a low latency and highly reliable link. We were able to solve this issue by troubleshooting, upon which we discovered that the issue was due to the ESP-NOW packets being overloaded by the constant bombardment of separate characters. Instead of sending the packets character by character, we grouped them into sentences to achieve a near instantaneous response time.

-  None of the Speech-to-text APIs we found trancribed speech from languages except english even though some claimed to do so. Some APIs only work on Mac or Linux so we had to test them by dual booting into a ubuntu os. Some of the models were not optimized thus causes our laptops to crash and no good results.

## Accomplishments that we're proud of
- We are proud to have created a device that could truly make a difference in one's life. Although the prototype is not the highest fidelity, we believe that with more iterations and resources, we can flesh out a truly unique experience that would encompass many of those on the autism spectrum.

- We are proud to have created a fully functioning end-to-end solution, since there are many complex components involved, each with their unique set of challenges.

## What we learned
- We researched and learned a lot about Autism Spectrum Disorder, and their unique experiences. Additionally, we learned the challenges of creating such a compact and tightly integrated system, using AI models and programming embedded systems.

## What's next for MediLens
- We wish to further improve this by adding an onboard camera to detect and inform users about the emotions of people around them. Many with ASD have challenges detecting and sensing emotions of others and themselves. Hence, this would benefit them greatly. 
-We also wish to move the microphone onto the ESP32 S3 directly, and not have to rely on a separate computer to interface with the AI APIs. If everything is tightly integrated with a cellular connection to the cloud, this would be a truly portable solution.

## Details about the code
- textconverter files trancribe realtime speech to text and we use different APIs to translate it to different language:
  - textconverter_openai uses ChatGPT API for translation
  - textconverter_google_translate uses Google Cloud API for translation
- The reciever and transmitter folders contain the code for ESP32 S3 microcontrollers to transmit speech data from a mic to the AR Glasses
