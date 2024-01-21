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
language = "french"


def translate():
    transcript_result = transcript_queue.get() # Store live transcript
    response = OpenAI.chat.completions.create(
                model = 'gpt-4',
                messages = [
                    {"role": "system", "content": f'Translate the word or text into {language}'},
                    {"role": "user", "content": transcript_result}
                ]
            )
    
    reply = str(response)
    reply_str = reply.split("'")
    reply_done = reply_str[5].split('"')
    translated_text = reply_done[0]
    print(translated_text)

    # Send text to COM as needed
    # send_to_serial(translated_text) 
    

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
    translate()


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