import io
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import mmap
import numpy
import soundfile
import torchaudio
import torch

from collections import defaultdict
from IPython.display import Audio, display
from pathlib import Path
from pydub import AudioSegment

from seamless_communication.inference import Translator
from seamless_communication.streaming.dataloaders.s2tt import SileroVADSilenceRemover


# Initialize a Translator object with a multitask model, vocoder on the GPU.

model_name = "seamlessM4T_v2_large"
vocoder_name = "vocoder_v2" if model_name == "seamlessM4T_v2_large" else "vocoder_36langs"

translator = Translator(
    model_name,
    vocoder_name,
    device=torch.device("cuda:0"),
    dtype=torch.float16,
)

print("English audio:")
in_file = "english.wav"
display(Audio(in_file, rate=16000, autoplay=False, normalize=True))

tgt_langs = ("spa", "fra", "deu", "ita", "hin", "cmn")

for tgt_lang in tgt_langs:
  text_output, speech_output = translator.predict(
      input=in_file,
      task_str="s2st",
      tgt_lang=tgt_lang,
  )

  print(f"Translated text in {tgt_lang}: {text_output[0]}")
  print()

  out_file = f"translated_english_{tgt_lang}.wav"

  torchaudio.save(out_file, speech_output.audio_wavs[0][0].to(torch.float32).cpu(), speech_output.sample_rate)

  print(f"Translated audio in {tgt_lang}:")
  audio_play = Audio(out_file, rate=speech_output.sample_rate, autoplay=False, normalize=True)
  display(audio_play)
  print()