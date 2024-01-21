import assemblyai as aai
import openai as OpenAI
import serial
import websocket, json
import pyaudio
from queue import Queue


aai.settings.api_key = "30ab78c6d7a64cf1b238372e4480b68f"
OpenAI.api_key = "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"

# ser = serial.Serial('COM4', 9600) # Change COM1 as needed
# def send_to_serial(data):
#     ser.write(data.encode())

transcript_queue = Queue()
language = "ko"

def google_translate(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    # print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    # print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result
    

def on_open(session_opened: aai.RealtimeSessionOpened):
  "This function is called when the connection has been established."

  #print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
  "This function is called when a new transcript has been received."

  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    transcript_queue.put(transcript.text + '')
    #print(transcript.text, end="\r\n")
    transcript_result = transcript_queue.get()
    google_translate("ko", transcript_result) 


  #else:
    #print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
  "This function is called when the connection has been closed."

  print("An error occured:", error)

def on_close():
  "This function is called when the connection has been closed."

  print("Closing Session")


transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=44_100,
  on_open=on_open, # optional
  on_close=on_close, # optional
)

# Start the connection
transcriber.connect()

# Open a microphone stream
microphone_stream = aai.extras.MicrophoneStream()


# Press CTRL+C to abort
transcriber.stream(microphone_stream)

transcriber.close()

# if __name__ == "__main__":
#    transcript_result = transcript_queue.get()
#    google_translate("fr", transcript_result) 