import os
import torch
import torchaudio
from torch.utils.data import Dataset

#WIP

class ManiaMapperDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.samples = []
        for song_dir in os.listdir(root_dir):
            song_path = os.path.join(root_dir, song_dir)
            if not os.path.isdir(song_path):
                continue
            for file_name in os.listdir(song_path):
                if file_name.endswith('.osu'):
                    osu_path = os.path.join(song_path, file_name)
                    audio_path = os.path.join(song_path, file_name[:-4] + '.mp3')
                    if os.path.isfile(audio_path):
                        self.samples.append((osu_path, audio_path))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        osu_path, audio_path = self.samples[idx]
        osu_data = self._load_osu(osu_path)
        audio_data = self._load_audio(audio_path)
        return osu_data, audio_data

    def _load_osu(self, path):
        # Load .osu file and extract difficulty information
        with open(path, 'r') as f:
            lines = f.readlines()
            #The difficulty is in the last line of the file, should be Difficulty:x
            assert lines[-1].startswith('Difficulty:')
            difficulty = lines[-1].split(':')[1].strip()

    def _load_audio(self, path):
        # Load audio file and return as a tensor
        return torch.Tensor(torchaudio.load(path)[0][0])
