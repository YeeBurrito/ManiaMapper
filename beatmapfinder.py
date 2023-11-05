import os

def find_beatmaps():
    file_location = "./Processed_Beatmaps/"
    extensions = {}
    #get a count of every file extension
    for folder in os.listdir(file_location):
        if os.path.isdir(os.path.join(file_location, folder)):
            for file in os.listdir(os.path.join(file_location, folder)):
                extension = file.split(".")[-1]
                if extension in extensions:
                    extensions[extension] += 1
                else:
                    extensions[extension] = 1
    #print the results
    for extension in extensions:
        print(extension + ": " + str(extensions[extension]))
                

def main():
    find_beatmaps()

if __name__ == '__main__':
    main()
# END: 3j4k5l6m7n8o
