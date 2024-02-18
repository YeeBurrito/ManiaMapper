import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, length):
        super(Generator, self).__init__()
        self.length = length
        
        # Define layers for generating data
        self.audio_conv = nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.audio_pool = nn.MaxPool1d(kernel_size=2, stride=2)
        self.audio_fc1 = nn.Linear(64 * (self.length // 2), 128)  # Adjust the input size accordingly
        self.audio_fc2 = nn.Linear(128, 64)  # Output size of this layer can be adjusted
        self.difficulty_fc1 = nn.Linear(1, 32)
        self.difficulty_fc2 = nn.Linear(32, 16)
        self.fc1 = nn.Linear(64 + 16, 256)  # Adjust input size accordingly
        self.fc2 = nn.Linear(256, 512)
        self.fc3 = nn.Linear(512, 1024)
        self.fc4 = nn.Linear(1024, self.length * 4)  # Adjust output size to match data shape
        
        # Define activation functions
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        
    def forward(self, audio_input, difficulty, noise):
        # Process audio waveform
        audio_output = self.audio_conv(audio_input)
        audio_output = self.relu(audio_output)
        audio_output = self.audio_pool(audio_output)
        audio_output = audio_output.view(audio_output.size(0), -1)
        audio_output = self.audio_fc1(audio_output)
        audio_output = self.relu(audio_output)
        audio_output = self.audio_fc2(audio_output)
        audio_output = self.relu(audio_output)
        
        # Process difficulty input
        difficulty_output = self.difficulty_fc1(difficulty)
        difficulty_output = self.relu(difficulty_output)
        difficulty_output = self.difficulty_fc2(difficulty_output)
        difficulty_output = self.relu(difficulty_output)
        
        # Concatenate audio, difficulty, and noise inputs
        combined_input = torch.cat((audio_output, difficulty_output, noise), dim=1)
        
        # Generate synthetic data
        x = self.fc1(combined_input)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        output = self.tanh(x)  # Output in the range [-1, 1]
        return output.view(-1, self.length, 4)


class Discriminator(nn.Module):
    def __init__(self, length):
        super(Discriminator, self).__init__()
        self.length = length
        
        # Define layers for discriminating real and fake data
        self.fc1 = nn.Linear(self.length * 4, 1024)  # Adjust input size to match data shape
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, 1)
        
        # Define activation functions
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, input_data):
        x = input_data.view(-1, self.length * 4)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        output = self.sigmoid(x)  # Output probability of being real
        return output