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
            #AudioLeadIn is the milliseconds of silence added by the game before the song starts
            if line.startswith("AudioLeadIn:"):
                audio_lead_in = int(line.split("AudioLeadIn:")[1].strip())
                break
            else:
                audio_lead_in = 0
        for line in lines:
            #Find the [HitObjects] section
            if line.startswith("[HitObjects]"):
                break
        lines = lines[lines.index(line) + 1:]
        #Go through each line in the [HitObjects] section
        for line in lines:
            #Split the line into its components
            line_components = line.split(",")
            #Get the time of the hitobject
            time = int(line_components[2])
            #if there is an audio lead in, offset the time by the audio lead in
            time += audio_lead_in
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
                #if there is an audio lead in, offset the time by the audio lead in
                end_time += audio_lead_in
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
                    img[time - start_time:end_time - start_time][column] = 255
            #if the note has an endtime that is in the correct time range, but the start time is not add the tail end of the hold note
            elif (end_time >= start_time and end_time < start_time + timestep):
                img[0:end_time - start_time][column] = 255
            #if there is a hold note that starts before the time range and ends after the time range, add the entire hold note
            elif (time < start_time and end_time >= start_time + timestep):
                img[:,column] = 255
            if  time >= start_time + timestep:
                break
    return img

def main():
    image_test = encode_map_to_image("./Processed_Beatmaps/1924015/Kry.exe feat. Ice - Last Wish ([GB]ReMILia) [Unfulfilled Wish].osu", 30000, 0)
    plt.imshow(image_test)
    plt.show()

if __name__ == '__main__':
    main()
