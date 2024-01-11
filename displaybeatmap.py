import os
import pygame
import time
import threading
import encodemaptoimage

def main():
    path = ".\\Datasets\\Train\\1001794_Phantom Sage - Holystone (UnluckyCroco) [At the Point of No Return]"
    osu_file, audio_file = get_files(path)
    last_note = get_map_length(path, osu_file)
    if last_note == 0:
        print("No notes in beatmap")
        return
    map_image = encodemaptoimage.encode_map_to_image(os.path.join(path, osu_file), last_note, 0)
    game_thread = threading.Thread(target=play_game, args=(path, map_image))
    music_thread = threading.Thread(target=play_audio, args=(os.path.join(path, audio_file),))
    input_thread = threading.Thread(target=wait_for_input)
    game_thread.start()
    music_thread.start()
    input_thread.start()

def get_files(path):
    files = os.listdir(path)
    osu_file = next((file for file in files if file.endswith(".osu")), None)
    audio_file = next((file for file in files if file.endswith(".mp3")), None)
    return osu_file, audio_file

def play_audio(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def play_game(path, map_image):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # adjust size as needed
    clock = pygame.time.Clock()

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Define lane positions
    LANE_WIDTH = 200
    LANE_HEIGHT = 600
    LANE_POSITIONS = [(i * LANE_WIDTH, 0) for i in range(4)]

    # Define note speed
    NOTE_SPEED = 2  # adjust as needed

    # Initialize notes
    notes = [(timing, notetype, pos) for timing, lane in enumerate(map_image) for pos, notetype in enumerate(lane) if notetype > 0]

    print(len(notes))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Clear screen
        screen.fill(BLACK)

        # Draw lanes
        for pos in LANE_POSITIONS:
            pygame.draw.rect(screen, WHITE, (*pos, LANE_WIDTH, LANE_HEIGHT), 1)

        # Update and draw notes
        for i in range(len(notes)):
            timing, notetype, pos = notes[i]
            if timing <= pygame.time.get_ticks():
                color = RED if notetype == 128 else WHITE  # use different colors for different note types
                pygame.draw.circle(screen, color, (LANE_POSITIONS[pos][0] + LANE_WIDTH // 2, LANE_HEIGHT - (pygame.time.get_ticks() - timing) * NOTE_SPEED), 10)
                if LANE_HEIGHT - (pygame.time.get_ticks() - timing) * NOTE_SPEED < 0:
                    notes.pop(i)

        pygame.display.flip()
        clock.tick(60)  # limit to 60 FPS

def get_map_length(path, osu_file):
    #last note is the last line that starts with a number
    with open(os.path.join(path, osu_file), 'r') as f:
        lines = f.readlines()
        last_note = next((line for line in reversed(lines) if line[0].isdigit()), None)
        if last_note is not None:
            last_note = last_note.split(",")
            last_note = int(last_note[2])
        else:
            last_note = 0
    return last_note

def wait_for_input():
    input()
    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()