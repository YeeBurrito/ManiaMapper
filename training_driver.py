import DatasetLoader
import generator_main
import torch
from torch import cuda
import pandas as pd

def main():
    device = 'cuda' if cuda.is_available() else 'cpu'
    print(f"GPU available: {cuda.is_available()}")
    print(f"device: {device}")

    #Hyperparameters
    batch_size = 64
    num_epochs = 5
    learning_rate = 0.001
    optimizer = torch.optim.Adam
    start_ms = 0
    random_start = False
    all_timesteps = True
    timestep_ms = 10000

    #file paths
    train_path = "./Datasets/Train"
    dev_path = "./Datasets/Dev"

    #load the dataset
    train_dataset = DatasetLoader.prepare_dataset(train_path, start_ms, random_start, all_timesteps, timestep_ms)
    dev_dataset = DatasetLoader.prepare_dataset(dev_path, start_ms, random_start, all_timesteps, timestep_ms)

    #create the dataloaders
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    dev_loader = torch.utils.data.DataLoader(dev_dataset, batch_size=batch_size, shuffle=True)

    #create the model
    model = generator_main.ManiaMapperGenerator()


if __name__ == "__main__":
    main()
