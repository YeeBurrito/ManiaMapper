import os
import re
import getData

def remove_files():
    #go through each folder in the Beatmaps folder and remove the .osu files that have a keycount that isn't 4k
    #this is defined in the CircleSize line of the .osu file, under the [Difficulty] section
    #Also delete any files that aren't of the mania gamemode, which is denoted by Mode: 3 in the [General] section
    file_location = "./Beatmaps/"
    for folder in os.listdir(file_location):
        if os.path.isdir(os.path.join(file_location, folder)):
            for file in os.listdir(os.path.join(file_location, folder)):
                if file.endswith(".osu"):
                    with open(os.path.join(file_location, folder, file), "r", errors='ignore') as f:
                        print("Checking " + os.path.join(file_location, folder, file))
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith("Mode"):
                                if line != "Mode: 3\n":
                                    print("Removing " + os.path.join(file_location, folder, file))
                                    f.close()
                                    os.remove(os.path.join(file_location, folder, file))
                                    break
                            if line.startswith("CircleSize"):
                                if line != "CircleSize:4\n":
                                    print("Removing " + os.path.join(file_location, folder, file))
                                    f.close()
                                    os.remove(os.path.join(file_location, folder, file))
                                    break

def get_song_difficulty():
    file_location = "./Processed_Beatmaps/"
    api = getData.get_client()
    for folder in os.listdir(file_location):
        if os.path.isdir(os.path.join(file_location, folder)):
            for file in os.listdir(os.path.join(file_location, folder)):
                if file.endswith(".osu"):
                    with open(os.path.join(file_location, folder, file), "r+", errors='ignore') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith("BeatmapID"):
                                map_id = int(line.split(":")[1].strip())
                                print("Getting difficulty for " + str(map_id))
                                #check if the difficulty is already on the last line of the file
                                if lines[-1].startswith("Difficulty"):
                                    print("Difficulty already exists")
                                    break
                                #get the difficulty, if it returns None, then the beatmap is not available, so remove it
                                difficulty = getData.get_beatmap_difficulty(api, map_id)
                                if difficulty == None:
                                    print("Removing " + os.path.join(file_location, folder, file))
                                    f.close()
                                    os.remove(os.path.join(file_location, folder, file))
                                    break
                                print("Difficulty: " + str(difficulty))
                                #add to the file
                                f.write("\nDifficulty:" + str(difficulty) + "\n")
                                break

def main():
    get_song_difficulty()

if __name__ == '__main__':
    main()