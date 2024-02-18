import os
import encodemaptoimage as emi

list_of_english_characters =    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                                "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H",
                                "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
                                "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", "!", "\"", "#", "$", "%",
                                "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@",
                                "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "\n", "\r", "\t"]

def main():
    path = "./Datasets/Train"
    print(path)
    for i, folder in enumerate(os.listdir(path)):
        print(folder)
        osu_file = emi.get_map_file(path + "/" + folder)
        print(osu_file)
        #remove every character in the file that gives an encoding error
        with open(path + "/" + folder + "/" + osu_file, "r", encoding='utf-8') as f:
            #read each line of the file
            while True:
                try:
                    lines = f.readlines()
                    #remove every character that is not in the list of english characters
                    for j, line in enumerate(lines):
                        new_line = ""
                        for character in line:
                            if character in list_of_english_characters:
                                new_line += character
                        lines[j] = new_line
                        #replace the line in the file with the new line
                except UnicodeDecodeError:
                    print("UnicodeDecodeError")
                    break
                except StopIteration:
                    break
        if i > 0:
            break

if __name__ == "__main__":
    main()