# Imports
import pygame
from pygame import Vector2 as v2, Color as Colour

from button import Button

# some pygame constst
WINDOW_SIZE = (768, 768)
TARGET_FPS = 60

# pygame inits
pygame.init()
display = pygame.display.set_mode(v2(WINDOW_SIZE))
clock = pygame.time.Clock()

# more variable inits
menu = ""
tiles = []
COLS = 7
ROWS = 6

# menu functions
def change_menu(targetMenu):
    global menu
    menu = targetMenu
    display.fill(bg_color)

def start_game_func(*_):
    change_menu("game")
    create_tiles()

def settings_menu(*_):
    change_menu("settings")

def go_back(*_):
    change_menu("start")

def create_tiles():
    global tiles
    tiles = []
    for c in range(COLS):
        for r in range(ROWS):
            tile = Button(
                        50*c+50, 50*r+50, 30, 30, str(len(tiles)), 
                        tile_color, tile_hover, tile_text, tile_press, None, 30, (len(tiles),c,r),
                        rounding=5
                    )
            tiles.append(tile)

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

    # === Color Variables ===
    primary_color = (70, 130, 180)    # button background
    hover_color   = (100, 149, 237)   # button hover
    text_color    = (245, 245, 245)   # button text
    tile_color    = (200, 200, 200)   # tile main
    tile_hover    = (170, 170, 170)   # tile hover
    tile_text     = (50, 50, 50)      # tile text
    bg_color      = (30, 30, 40)      # main background

    start_button = Button(x, y - 100, width, height, "Start Game", primary_color, hover_color, text_color, start_game_func, "Baloo2-Bold.ttf", 50, rounding=8)
    settings_button = Button(x, y-100+height*2, width, height, "Settings", primary_color, hover_color, text_color, settings_menu, "Baloo2-Bold.ttf", 50, rounding=8)
    go_back_button = Button(x, y, width, height, "Go back", primary_color, hover_color, text_color, go_back, "Baloo2-Bold.ttf", 50, rounding=8)

    change_menu("start")

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
            for tile in tiles:
                tile.draw(display)
        else:
            # very descriptive error msg
            print("you broke smth.")
            running = False

        # flip the display and clock the tick so stuff actually updates
        pygame.display.flip()
        clock.tick(TARGET_FPS)
