import matplotlib.pyplot as plt
import encodemaptoimage as emi
import torchaudio
from torchaudio import transforms

def main():
    # Load audio file and return as a tensor
    osu_file = "./Nexta/LNexta.osu"
    audio_file = "./Nexta/audio.mp3"
    #Get the audio file
    waveform, sample_rate = torchaudio.load(audio_file)
    print(waveform.shape, sample_rate)

    #Cut the waveform to the first 20 seconds
    waveform = waveform[:, :sample_rate * 20]

    #Save to file as a .wav to test
    torchaudio.save("orig.wav", waveform, sample_rate)

    # Resample the waveform to the target sample rate
    target_sample_rate = 480000
    resampler = transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
    waveform = resampler(waveform)
    print(waveform.shape, target_sample_rate)

    #Save to file as a .wav to test
    torchaudio.save("resampledlarge.wav", waveform, target_sample_rate)


if __name__ == "__main__":
    main()
