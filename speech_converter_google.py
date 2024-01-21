from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import assemblyai as aai



def transcribe_streaming_v2(
    project_id: str,
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


if __name__ == "__main__":
    transcribe_streaming_v2("speech-to-te-411900")