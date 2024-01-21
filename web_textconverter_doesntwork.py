import assemblyai as aai
import openai as OpenAI
import serial
import websocket, json
import pyaudio
from queue import Queue


aai.settings.api_key = "30ab78c6d7a64cf1b238372e4480b68f"
OpenAI.api_key = "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"

#ser = serial.Serial('COM1', 9600) # Change COM1 as needed
#def send_to_serial(data):
    #ser.write(data.encode())

transcript_queue = Queue()
language = "french"

YOUR_API_KEY = "30ab78c6d7a64cf1b238372e4480b68f" 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

def on_message(ws, message):
    """
    is being called on every message
    """
    transcript = json.loads(message)
    text = transcript['text']

    if transcript["message_type"] == "PartialTranscript":
        print(f"Partial transcript received: {text}")
    elif transcript['message_type'] == 'FinalTranscript':
        print(f"Final transcript received: {text}")

def on_open(ws):
    """
    is being called on session begin
    """
    def send_data():
        while True:
            # read from the microphone
            data = stream.read(FRAMES_PER_BUFFER)

            # binary data can be sent directly
            ws.send(data)



def on_error(ws, error):
    """
    is being called in case of errors
    """
    print(error)


def on_close(ws):
    """
    is being called on session end
    """
    print("WebSocket closed")


def on_close():
  "This function is called when the connection has been closed."

  print("Closing Session")

websocket.enableTrace(False)

auth_header = {"Authorization": YOUR_API_KEY }

ws = websocket.WebSocketApp(
    f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}",
    header=auth_header,
    on_message=on_message,
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)


# Start the WebSocket connection
ws.run_forever()












def translate():
    transcript_result = transcript_queue.get() # Store live transcript
    response = OpenAI.chat.completions.create(
                model = 'gpt-3.5-turbo',
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
    #send_to_serial(translated_text) 

