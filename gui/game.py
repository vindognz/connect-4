# Imports
import pygame
from pygame import Vector2 as v2, Color as Colour

from button import Button

# some constst
WINDOW_SIZE = (768, 768)
WINDOW_SCALE = 1
TARGET_FPS = 60

# pygame inits
pygame.init()
display = pygame.display.set_mode(v2(WINDOW_SIZE)*WINDOW_SCALE)
clock = pygame.time.Clock()

# more variable inits
menu = "start"
tiles = []

# menu functions
def change_menu(targetMenu):
    global menu
    menu = targetMenu
    display.fill('black')

def start_game_func(*_):
    change_menu("game")

def settings_menu(*_):
    change_menu("settings")

def go_back(*_):
    change_menu("start")

# gets called when you click on a tile
def tile_press(tile):
    tile_id,x,y = tile.extra_data
    print(f"TILE {tile_id} at {x},{y} PRESSED")

# Main block
if __name__ == "__main__":
    # You're running the game, therefore running = True
    running = True

    # Button inits
    width = 280
    height = 75

    x = WINDOW_SIZE[0] / 2 - width / 2 # center of the screen horizontally
    y = (WINDOW_SIZE[1] / 2 - height / 2) # center of the screen vertically

    start_button = Button(x, y - 100, width, height, "Start Game", (0, 150, 0), (255, 0, 0), (255, 255, 255), start_game_func, "Baloo2-Bold.ttf", 50)
    settings_button = Button(x, y-100+height*2, width, height, "Settings", (0, 150, 0), (255, 0, 0), (255, 255, 255), settings_menu, "Baloo2-Bold.ttf", 50)
    go_back_button = Button(x, y, width, height, "Go back", (0, 150, 0), (255, 0, 0), (255, 255, 255), go_back, "Baloo2-Bold.ttf", 50)

    # Game loop
    while running:
        
        # handles user input
        for event in pygame.event.get():
            # Lets you actually close the game, or ESC out
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Handles all the inputs for the buttons
            if menu == "start":
                start_button.handle_event(event)
                settings_button.handle_event(event)
            elif menu == "settings":
                go_back_button.handle_event(event)
            elif menu == "game":
                for tile in tiles:
                    tile.handle_event(event)
            else:
                # very descriptive error message
                print("You broke smth idek what tbh")
                running = False
            
        # Display stuff!
        # so depending on what menu you're in, draw different stuff
        if menu == "start":
            start_button.draw(display)
            settings_button.draw(display)
        elif menu == "settings":
            go_back_button.draw(display)
        # basic connect-4 ahh grid
        elif menu == "game":
            COLS = 7
            ROWS = 6

            tiles = []

            for c in range(COLS):
                for r in range(ROWS):
                    tile = Button(50*c+50, 50*r+50, 30, 30, str(len(tiles)), (255, 255, 255), (150, 150, 150), (255, 0, 0), tile_press, None, 30, (len(tiles),c,r))
                    tiles.append(tile)
            
            for tile in tiles:
                tile.draw(display)
        else:
            # very descriptive error msg
            print("you broke smth.")
            running = False

        # flip the display and clock the tick so stuff actually updates
        pygame.display.flip()
        clock.tick(TARGET_FPS)
