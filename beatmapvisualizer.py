import os
import pygame

#Globals
window_size = (1500, 900)
bottom_line_y = 0.95 * window_size[1]

class Note:
    def __init__(self, lane, speed):
        self.lane = lane
        self.speed = speed
        self.y = -300

    def update(self, dt):
        self.y += self.speed * dt

    def has_hit_bottom(self, bottom_line_y):
        return self.y + 50 >= bottom_line_y

    def draw(self, screen):
        note_color = (255, 255, 255)  # white color
        if self.lane in [1, 2]:  # if the note is in the middle 2 lanes
            note_color = (128, 128, 255)  # blue color
        note_width = window_size[0] // 12
        note_height = 50  # 50 pixels in height
        pygame.draw.rect(screen, note_color, (((note_width * self.lane) + (window_size[0] // 3)), self.y, note_width, note_height))

def main():
    path = "./Nexta/"
    display_beatmap_lanes(path)

def display_beatmap_lanes(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith(".osu"):
            mapfile = file
            break

    with open(os.path.join(path, mapfile), 'r') as f:
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

    pygame.init()
    music = pygame.mixer.Sound(os.path.join(path, song_file))
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
    notes = [Note(2, 1.5), Note(3, 1.5), Note(0, 0.3)]
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

        for note in notes:
            note.update(dt)  # update the note's position
            note.draw(screen)  # draw the note

        notes = [note for note in notes if not note.has_hit_bottom(bottom_line_y)]  # remove the notes that have hit the bottom line

        pygame.display.flip()

if __name__ == "__main__":
    main()