import os
import torch
import torchaudio
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
        self.ms_start = ms_start
        self.ms_timestep = ms_timestep
        self.difficulty = difficulty
    
    def __len__(self):
        return len(self.map_image)
    
    def __getitem__(self, idx):
        return self.map_image[idx], self.song_file[idx], self.ms_start[idx], self.ms_timestep[idx], self.difficulty[idx]
    

def prepare_dataset(train_path, start_ms, random_start, all_timesteps, timestep_ms):
    #ignore the random start for now
    if random_start:
        start_ms = -1
    #Get all the folders in the directory
    folders = os.listdir(train_path)
    #For each folder, get the osu file and the audio file
    for folder in folders:
        osu_file, audio_file = get_files(train_path + "/" + folder)
        #Get the map images and the start times for each map image
        if all_timesteps:
            map_images, start_times, difficulties = emi.get_all_timesteps(train_path + "/" + folder + "/" + osu_file, timestep_ms, start_ms)
        else:
            map_images = [emi.encode_map_to_image(train_path + "/" + folder + "/" + osu_file, timestep_ms, start_ms)]
            start_times = [start_ms]
            difficulties = [emi.get_map_difficulty(train_path + "/" + folder + "/" + osu_file)]
        #Get the audio file
        waveform, sample_rate = torchaudio.load(train_path + "/" + folder + "/" + audio_file)
        #Split the waveform into the correct time ranges
        audio_waveforms = []
        for i in range(len(map_images)):
            #Get the start time and end time of the audio file
            start_time = start_times[i] / 1000
            end_time = (start_times[i] + timestep_ms) / 1000
            #Get the time range of the audio file
            audio_file = waveform[:, int(start_time * sample_rate):int(end_time * sample_rate)]
            audio_waveforms.append(audio_file)
        #Get the difficulty of the maps
        #Create the dataset
        dataset = ManiaMapperDataset(map_images, audio_waveforms, start_times, timestep_ms)
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

if __name__ == "__main__":
    main()
