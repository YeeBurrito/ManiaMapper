import os
import pygame
from collections import deque
import encodemaptoimage as emi

#Globals
window_size = (1500, 900)
bottom_line_y = 0.95 * window_size[1]
note_speed = 1 #time in seconds for a note to travel from the top to the bottom of the screen

class Note:
    def __init__(self, timing, lane, type, length) -> None:
        self.timing = timing
        self.lane = lane
        self.type = type
        self.length = length
        self.y = -100 #start the note off screen
    
    def update(self, dt):
        self.y += note_speed * dt
    
    def draw(self, screen):
        note_color = (255, 255, 255) #white color
        if self.lane in [1, 2]: #if the note is in the middle 2 lanes
            note_color = (128, 128, 255) #blue color
        note_width = window_size[0] // 12
        if self.type == 0:
            note_height = 50
            pygame.draw.rect(screen, note_color, (((note_width * self.lane) + (window_size[0] // 3)), self.y, note_width, note_height))
            #check if the note has hit the bottom of the screen
            #if it has, remove it from the list of notes
            if self.y + 50 >= bottom_line_y:
                return True
        else:
            note_height = 50 + (note_speed * self.length)
            #draw the hold note
            #if the bottom of the hold note has hit the bottom of the screen, draw the tail end of the hold note
            if self.y + note_height >= bottom_line_y:
                pygame.draw.rect(screen, note_color, (((note_width * self.lane) + (window_size[0] // 3)), self.y, note_width, bottom_line_y - self.y))
                #if the tail end of the hold note has hit the bottom of the screen, remove the note from the list of notes
                if bottom_line_y - self.y <= 0:
                    return True
            else:
                pygame.draw.rect(screen, note_color, (((note_width * self.lane) + (window_size[0] // 3)), self.y, note_width, note_height))

        

def display_game(path):
    map_file, image_file, song_file = load_files(path)

    #get the notes from the map file, loaded as a numpy array
    #for now, just get the first 10 seconds of the song
    map_image = emi.encode_map_to_image(os.path.join(path, map_file), 10000, 0)

    notes = generate_notes(map_image)

    #initialize pygame and load the song, image, and set the window size
    pygame.init()
    music = pygame.mixer.Sound(os.path.join(path, song_file))
    pygame.mixer.Sound.set_volume(music, 0.2)
    window_size = (1500, 900)
    background = pygame.image.load(os.path.join(path, image_file))
    background = pygame.transform.scale(background, window_size)
    background.set_alpha(80)
    pygame.display.set_caption("beatmap visualizer")
    screen = pygame.display.set_mode(window_size)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #play the song
    pygame.mixer.Sound.play(music)

    running = True

    clock = pygame.time.Clock()

    print(bottom_line_y)
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        # draw lanes
        lane_width = window_size[0] // 12
        lane_height = window_size[1]
        lane_color = (50, 50, 50, 128)  # dark color
        line_color = (175, 175, 175)  # grey color
        line_width = 2  # thin line

        for i in range(4, 8):
            pygame.draw.rect(screen, lane_color, (i * lane_width, 0, lane_width, lane_height))
            pygame.draw.line(screen, line_color, (i * lane_width, 0), (i * lane_width, lane_height), line_width)

        # draw line to the right of the rightmost lane
        pygame.draw.line(screen, line_color, (8 * lane_width, 0), (8 * lane_width, lane_height), line_width)

        # draw horizontal line across all lanes near the bottom of the screen
        pygame.draw.line(screen, line_color, (4 * lane_width, bottom_line_y), (8 * lane_width, bottom_line_y), line_width)

        dt = clock.tick(60)  # get the elapsed time since the last frame

        #list of active notes
        active_notes = []

        # Spawn notes when their time has come
        while notes and notes[0].timing <= pygame.time.get_ticks():
            print(pygame.time.get_ticks())
            print("spawned note at time: ", notes[0].timing, "ms")
            active_notes.append(notes.popleft())
        
        # Update and draw notes
        for note in active_notes:
            if note.draw(screen):
                active_notes.remove(note)
        
        pygame.display.flip()


def load_files(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith(".osu"):
            map_file = file
            break
    
    print(map_file)

    with open(os.path.join(path, map_file), 'r') as f:
        lines = f.readlines()

    events_index = lines.index('[Events]\n')
    for i in range(events_index + 1, len(lines)):
        if lines[i].startswith('//Background and Video events'):
            image_line = lines[i + 1]
            image_file = image_line.split(',')[2].strip("\"")
            print(image_file)
            break

    song_index = lines.index('[General]\n')
    for i in range(song_index + 1, len(lines)):
        if lines[i].startswith('AudioFilename:'):
            song_file = lines[i].split(' ')[1].strip()
            print(song_file)
            break
    
    return map_file, image_file, song_file

def generate_notes(map_image):
    #create a copy of the map image
    #this will be used to remove notes from the map image as they are added to the list of notes
    map_image = map_image.copy()
    notes = deque()
    for timing, lane in enumerate(map_image):
        for pos, notetype in enumerate(lane):
            if notetype == 128:
                print(timing, pos, 0, -1)
                notes.append(Note(timing, pos, 0, -1))
            elif notetype == 255:
                #find the end of the hold note, or the next index where the note is not 255
                end = next((i for i, note in enumerate(map_image[timing:,pos]) if note != 255), None)
                if end is not None:
                    print(timing, pos, 1, end)
                    notes.append(Note(timing, pos, 1, end))
                    map_image[timing:end+timing, pos] = 0
                else:
                    print(timing, pos, 1, -1)
                    notes.append(Note(timing, pos, 1, -1))
                    map_image[timing:, pos] = 0
    
    return notes

def main():
    path = "./Nexta/"
    display_game(path)

if __name__ == "__main__":
    main()