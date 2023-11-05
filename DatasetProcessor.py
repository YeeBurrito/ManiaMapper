import os
import random
import shutil

def sort_files():
    """
    Sorts files into the dev, train, and test datasets.
    """
    file_location = "./Processed_Beatmaps/"
    train_dataset_location = "./Datasets/Train/"
    dev_dataset_location = "./Datasets/Dev/"
    test_dataset_location = "./Datasets/Test/"
    split_rates = [0.8, 0.1, 0.1]
    #get each .osu map file from the processed beatmaps folder
    for folder in os.listdir(file_location):
        if os.path.isdir(os.path.join(file_location, folder)):
            for file in os.listdir(os.path.join(file_location, folder)):
                if file.endswith(".osu"):
                    #find the associated audio file in the same folder
                    audio_file_name = ""
                    with open(os.path.join(file_location, folder, file), "r", errors='ignore') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith("AudioFilename: "):
                                audio_file_name = line.split("AudioFilename: ")[1].strip()
                                break
                    #check if the audio file exists
                    if audio_file_name == "":
                        print("Audio file not found for " + os.path.join(file_location, folder, file))
                        continue
                    #check if the audio file is in the same folder
                    if not os.path.exists(os.path.join(file_location, folder, audio_file_name)):
                        print("Audio file not found for " + os.path.join(file_location, folder, file))
                        continue
                    # randomly assign the map to dev, train, or test dataset
                    dataset = random.choices(['train', 'dev', 'test'], weights=split_rates, k=1)[0]
                    # create folder for the map and its respective song inside the respective dataset folder
                    map_folder = os.path.join(eval(dataset + '_dataset_location'), folder + '_' + file[:-4])
                    os.makedirs(map_folder, exist_ok=True)
                    shutil.copy2(os.path.join(file_location, folder, file), map_folder)
                    shutil.copy2(os.path.join(file_location, folder, audio_file_name), map_folder)

def main():
    sort_files()

if __name__ == '__main__':
    main()

