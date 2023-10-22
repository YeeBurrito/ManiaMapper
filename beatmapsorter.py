import os

def get_files():
    file_location = "./Beatmaps/"
    new_file_location = "./Processed_Beatmaps/"
    i = 0
    for folder in os.listdir(file_location):
        print("Processing " + folder)
        new_folder_name = folder.split(" ")[0]
        if not os.path.exists(os.path.join(new_file_location, new_folder_name)):
            os.mkdir(os.path.join(new_file_location, new_folder_name))
        for file in os.listdir(os.path.join(file_location, folder)):
            if file.endswith(".osu"):
                with open(os.path.join(file_location, folder, file), "r", errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("AudioFilename: "):
                            audio_file_name = line.split("AudioFilename: ")[1].strip()
                            if not os.path.exists(os.path.join(new_file_location, new_folder_name, audio_file_name)):
                                os.rename(os.path.join(file_location, folder, audio_file_name), os.path.join(new_file_location, new_folder_name, audio_file_name))
                            break
                os.rename(os.path.join(file_location, folder, file), os.path.join(new_file_location, new_folder_name, file))

def main():
    get_files()

if __name__ == '__main__':
    main()