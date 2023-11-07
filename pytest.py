import torch
import torchaudio
import os
from pygame import mixer
import time

def main():
    # Load audio file and return as a tensor
    path = "./Datasets/Train/1001794_Phantom Sage - Holystone (UnluckyCroco) [At the Point of No Return]/audio.mp3"
    print(path)
    waveform, sample_rate = torchaudio.load(path)
    spectrogram = torchaudio.transforms.Spectrogram(waveform,  sample_rate)
    print(spectrogram)

if __name__ == "__main__":
    main()
