import os
import torch
import torchaudio
from torchaudio import transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np
import encodemaptoimage as emi

#WIP
#The features of the dataset are the difficulty which is just a float
#and the certain ms range of the song file
#The label is ms range of the map image

#for example, one feature could be seconds 10-20 of the song file
#and the label could be the map image of the song file at that time

class ManiaMapperDataset(Dataset):
    def __init__(self, map_image, song_file, ms_start=0, ms_timestep=10000, difficulty=0.0):
        self.map_image = map_image
        self.song_file = song_file
        self.difficulty = difficulty
        self.ms_start = ms_start
        self.ms_timestep = ms_timestep
        self.difficulty = difficulty
    
    def __len__(self):
        return len(self.map_image)
    
    def __getitem__(self, idx):
        return self.map_image[idx], self.song_file[idx], self.ms_start[idx], self.ms_timestep, self.difficulty[idx]
    

def prepare_dataset(train_path, start_ms, random_start, all_timesteps, timestep_ms, batch_size=64, target_sample_rate=44100):
    #Make sure to use the gpu if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    map_images = []
    start_times = []
    difficulties = []
    audio_waveforms = []
    #ignore the random start for now
    if random_start:
        start_ms = -1
    #Get all the folders in the directory
    folders = os.listdir(train_path)
    #For each folder, get the osu file and the audio file
    for i, folder in enumerate(folders):
        osu_file, audio_file = get_files(train_path + "/" + folder)
        #Get the map images and the start times for each map image
        if all_timesteps:
            map_image, start_time, difficulty = emi.get_all_timesteps(train_path + "/" + folder + "/" + osu_file, timestep_ms, start_ms)
            map_images.extend(map_image)
            start_times.extend(start_time)
            difficulties.extend(difficulty)
        else:
            map_images.append(emi.encode_map_to_image(train_path + "/" + folder + "/" + osu_file, timestep_ms, start_ms))
            start_times.append(start_ms)
            difficulties.append(emi.get_map_difficulty(train_path + "/" + folder + "/" + osu_file))
        #Get the audio file
        waveform, sample_rate = torchaudio.load(train_path + "/" + folder + "/" + audio_file)
        # Resample the waveform to the target sample rate
        resampler = transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
        waveform = resampler(waveform)
        #Split the waveform into the correct time ranges
        for i in range(len(map_images)):
            #Get the start time and end time of the audio file
            start_time = start_times[i] / 1000
            end_time = (start_times[i] + timestep_ms) / 1000
            #Get the time range of the audio file
            audio_file = waveform[:, int(start_time * target_sample_rate):int(end_time * target_sample_rate)]
            audio_waveforms.append(audio_file)
        #if the batch_size is -1, then get all the files
        if batch_size >= 0 and i >= batch_size:
            break
    #Create the dataset
    dataset = ManiaMapperDataset(map_images, audio_waveforms, start_times, timestep_ms, difficulties)
    return dataset

def get_files(path):
    files = os.listdir(path)
    osu_file = next((file for file in files if file.endswith(".osu")), None)
    audio_file = next((file for file in files if file.endswith(".mp3")), None)
    return osu_file, audio_file

def main():
    #For testing purposes
    path = "./Datasets/Train"
    folders = os.listdir(path)
    test_dataset = prepare_dataset(path, 0, False, False, 10000, 1000)

if __name__ == "__main__":
    main()
