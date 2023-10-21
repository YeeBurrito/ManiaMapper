import os
import zipfile

def unzip_files():
    file_location = "./Beatmaps/"
    for file in os.listdir(file_location):
        if file.endswith(".osz"):
            #rename the file to a zip file
            os.rename(os.path.join(file_location, file), os.path.join(file_location, file.replace(".osz", ".zip")))
            file = file.replace(".osz", ".zip")
            #unzip the file and delete the zip file
            with zipfile.ZipFile(os.path.join(file_location, file), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(file_location, file.replace(".zip", "")))

def main():
    unzip_files()

if __name__ == '__main__':
    main()