import numpy as np
import os
import matplotlib.pyplot as plt

def encode_map_to_image(filename, timestep, start_time):
    #Create an image with a numpy array of size (ms, 4)
    #Each row represents a millisecond
    #Each column represents a lane in the map
    #The value of each pixel represents the type of hitobject that is present in that lane at that time
    img = np.zeros((timestep, 4), dtype=np.uint8)
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            #Find the [HitObjects] section
            if line.startswith("[HitObjects]"):
                break
        lines = lines[lines.index(line) + 1:]
        #if the start_time is -1, then the start time will be a random time in the map,
        #from 0ms to the end minus the timestep
        #So if the map was 60 seconds long and the timestep was 10 seconds, the start time would be between 0 and 50 seconds
        if start_time == -1:
            #Find the last note in the map
            last_note = get_last_note(f)
            #Set the start time to a random time in the map
            start_time = np.random.randint(0, last_note - timestep)

        #Go through each line in the [HitObjects] section
        for line in lines:
            #make sure the line is a hitobject
            if line.startswith("\n"):
                break
            #Split the line into its components
            line_components = line.split(",")
            #Get the time of the hitobject
            time = int(line_components[2])
            #Get the type of the hitobject
            type = int(line_components[3])
            #Get the column of the hitobject
            column = int(line_components[0])
            #Convert the column into a number between 0 and 3, 0=64, 1=192, 2=320, 3=448
            column = (column - 64) // 128
            #Get the end time of the hitobject if it is a hold note
            if type & 128 == 128:
                end_time = line_components[5]
                #remove everything after the colon
                end_time = end_time.split(":")[0]
                end_time = int(end_time)
            else:
                end_time = -1
            # print(line_components)
            #Make sure the hitobject is in the correct time range
            if (time >= start_time and time < start_time + timestep):
                #Set the pixel at the time and column to the type of the hitobject
                #Check the type of the hitobject
                #1 is a normal note
                #128 is a hold note
                if type & 1 == 1:
                    img[time - start_time][column] = 128
                if type & 128 == 128:
                    img[time - start_time:end_time - start_time, column] = 255
            #if the note has an endtime that is in the correct time range, but the start time is not add the tail end of the hold note
            elif (end_time >= start_time and end_time < start_time + timestep):
                img[0:end_time - start_time, column] = 255
            #if there is a hold note that starts before the time range and ends after the time range, add the entire hold note
            elif (time < start_time and end_time >= start_time + timestep):
                img[:,column] = 255
            if  time >= start_time + timestep:
                break
    return img

def get_last_note(osu_file):
    lines = osu_file.readlines()
    last_note = lines[-3].split(",")[2]
    last_note = int(last_note)
    return last_note

def get_all_timesteps(osu_file_path, timestep, start_time):
    with open(osu_file_path, "r") as f:
        last_note = get_last_note(f)
    map_images = []
    start_times = []
    difficulties = []
    #The last map image cannot be longer than the last note
    for i in range(start_time, last_note - timestep, timestep):
        map_images.append(encode_map_to_image(osu_file_path, timestep, i))
        start_times.append(i)
        difficulties.append(get_map_difficulty(osu_file_path))
    return map_images, start_times, difficulties

def get_song_file(osu_file_path):
    with open(osu_file_path, "r") as f:
        lines = f.readlines()
    song_index = lines.index('[General]\n')
    for i in range(song_index + 1, len(lines)):
        if lines[i].startswith('AudioFilename:'):
            #remove the AudioFilename: part of the line without splitting the line
            song_file = lines[i].replace('AudioFilename: ', '').strip()
            return song_file

def get_map_file(osu_file_path):
    for file in os.listdir(osu_file_path):
        if file.endswith(".osu"):
            return file
        
def get_map_difficulty(osu_file_path):
    with open(osu_file_path, "r") as f:
        lines = f.readlines()
    return lines[-1].split(":")[1].strip()

def main():
    image_test = encode_map_to_image("./Processed_Beatmaps/1924015/Kry.exe feat. Ice - Last Wish ([GB]ReMILia) [Unfulfilled Wish].osu", 30000, -1)
    plt.imshow(image_test)
    plt.show()

if __name__ == '__main__':
    main()
