import torch
import torchaudio
import matplotlib.pyplot as plt

def main():
    # Load audio file and return as a tensor
    path = "./Datasets/Train/1001794_Phantom Sage - Holystone (UnluckyCroco) [At the Point of No Return]/audio.mp3"
    print(path)
    waveform, sample_rate = torchaudio.load(path)
    spectrogram = torchaudio.transforms.Spectrogram(n_fft=512)(waveform)

    # Display the spectrogram
    plt.figure()
    plt.imshow(spectrogram[0].log2(), aspect='auto', origin='lower')
    plt.title('Spectrogram')
    plt.xlabel('Frames')
    plt.ylabel('Frequency Bin')
    plt.colorbar(format="%+2.0f dB")
    plt.show()

if __name__ == "__main__":
    main()
