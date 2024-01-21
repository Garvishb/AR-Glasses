from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import assemblyai as aai



def transcribe_streaming_v2(
    project_id: str,
    # content
    audio_file: str,
) -> cloud_speech.StreamingRecognizeResponse:
    """Transcribes audio from audio file stream.

    Args:
        project_id: The GCP project ID.
        audio_file: The path to the audio file to transcribe.

    Returns:
        The response from the transcribe method.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()


    # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = len(content) // 5
    stream = [
        content[start : start + chunk_length]
        for start in range(0, len(content), chunk_length)
    ]
    audio_requests = (
        cloud_speech.StreamingRecognizeRequest(audio=audio) for audio in stream
    )

    recognition_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )
    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        streaming_config=streaming_config,
    )

    def requests(config: cloud_speech.RecognitionConfig, audio: list) -> list:
        yield config
        yield from audio

    # Transcribes the audio into text
    responses_iterator = client.streaming_recognize(
        requests=requests(config_request, audio_requests)
    )
    responses = []
    for response in responses_iterator:
        responses.append(response)
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

    return responses



# import sounddevice as sd
# import numpy as np
# import wave

# class mic_data():
#     def __init__(self):
#         self.sample_rate = 10000
#         self.channels = 2
#         self.duration = 1
#         self.audio_data = []

#     def callback(self, indata, frames, time, status):
#         if status:
#             print(status)
#         self.audio_data.append(indata.copy())

#     def record_audio(self):
#         with sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.sample_rate):
#             sd.sleep(int(self.duration * 1000))

#         audio_array = np.concatenate(self.audio_data, axis=0)

#         with wave.open('audio.wav', 'wb') as wf:
#             wf.setnchannels(self.channels)
#             wf.setsampwidth(2)  # Adjust based on your requirements
#             wf.setframerate(self.sample_rate)
#             wf.writeframes(audio_array.tobytes())
            

# if __name__ == "__main__":
#     mic = mic_data()
#     mic.record_audio()
#     transcribe_streaming_v2("speech-to-te-411900", "audio.wav")


# import os
# import time
# import playsound
# import speech_recognition as sr
# from gtts import gTTS


# def speak(text):
#     tts = gTTS(text=text, lang="en")
#     filename = "voice.mp3"
#     tts.save(filename)
#     playsound.playsound(filename)


# def get_audio():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         said = ""

#         try:
#             said = r.recognize_google(audio)
#             print(said)
#         except Exception as e:
#             print("Exception: " + str(e))

#     return said
#     # return audio

# # text = get_audio()


# # if "hello" in text:
# #     speak("hello, how are you?")
# # elif "what is your name" in text:
# #     speak("My name is Tim")

# if __name__ == "__main__":
#     audio = get_audio()
#     transcribe_streaming_v2("speech-to-te-411900", audio)