import os
from pydub import AudioSegment
import shutil

def removeOggMaps():
    datasets_location = "./Datasets/"
    for dataset_folder in os.listdir(datasets_location):
        if os.path.isdir(os.path.join(datasets_location, dataset_folder)):
            for map_folder in os.listdir(os.path.join(datasets_location, dataset_folder)):
                if os.path.isdir(os.path.join(datasets_location, dataset_folder, map_folder)):
                    for file in os.listdir(os.path.join(datasets_location, dataset_folder, map_folder)):
                        if file.endswith(".ogg"):
                            #remove the folder if it exists
                            print("Removing " + os.path.join(datasets_location, dataset_folder, map_folder))
                            if os.path.exists(os.path.join(datasets_location, dataset_folder, map_folder)):
                                shutil.rmtree(os.path.join(datasets_location, dataset_folder, map_folder))


def main():
    removeOggMaps()

if __name__ == "__main__":
    main()