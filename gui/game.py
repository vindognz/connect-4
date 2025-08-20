# imports
import pygame
from button import Button
from menu_manager import MenuManager

# consts
WINDOW_SIZE = (768, 768)
TARGET_FPS = 60
COLS, ROWS = 7, 6
TILE_SIZE, TILE_SPACING = 50, 20

GRID_WIDTH = COLS * TILE_SIZE + (COLS - 1) * TILE_SPACING
GRID_HEIGHT = ROWS * TILE_SIZE + (ROWS - 1) * TILE_SPACING

# init the pygame
pygame.init()
font = pygame.font.Font("Baloo2-Bold.ttf", 40)
display = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# variables
tiles = []
menu_manager = MenuManager(display, (30, 30, 40))  # background color

# colorss
primary_color = (70, 130, 180)    # button background
hover_color   = (51, 102, 145)    # button hover
text_color    = (245, 245, 245)   # button text
tile_color    = (200, 200, 200)   # tile main
tile_hover    = (170, 170, 170)   # tile hover
tile_text     = (50, 50, 50)      # tile text
bg_color      = (30, 30, 40)      # main background

# menu functions
def start_game_func(*_):
    create_tiles()
    menu_manager.change_menu("game")

def settings_menu(*_):
    menu_manager.change_menu("settings")

def go_back(*_):
    menu_manager.change_menu("start")

# tile stuff
def create_tiles():
    global tiles
    tiles = []
    
    start_x = (WINDOW_SIZE[0] - GRID_WIDTH) // 2
    start_y = (WINDOW_SIZE[1] - GRID_HEIGHT) // 2

    for c in range(COLS):
        for r in range(ROWS):
            x = start_x + c * (TILE_SIZE + TILE_SPACING)
            y = start_y + r * (TILE_SIZE + TILE_SPACING)

            tile = Button(
                x, y, TILE_SIZE, TILE_SIZE, str(len(tiles)),
                tile_color, tile_hover, tile_text, tile_press, None, 30, (len(tiles), c, r),
                rounding=5
            )
            tiles.append(tile)

def tile_press(tile):
    tile_id, x, y = tile.extra_data
    print(f"TILE {tile_id} at {x},{y} PRESSED")


# button stuff
width, height = 280, 75
x = WINDOW_SIZE[0] / 2 - width / 2
y = WINDOW_SIZE[1] / 2 - height / 2

start_button = Button(x, y - 100, width, height, "Start Game",
                      primary_color, hover_color, text_color,
                      start_game_func, "Baloo2-Bold.ttf", 50, rounding=8)

settings_button = Button(x, y - 100 + height * 2, width, height, "Settings",
                         primary_color, hover_color, text_color,
                         settings_menu, "Baloo2-Bold.ttf", 50, rounding=8)

go_back_button = Button(x, y, width, height, "Go back",
                        primary_color, hover_color, text_color,
                        go_back, "Baloo2-Bold.ttf", 50, rounding=8)


# menu handlers
# start
def start_menu_events(event):
    start_button.handle_event(event)
    settings_button.handle_event(event)

def start_menu_draw():
    start_button.draw(display)
    settings_button.draw(display)

# settings
def settings_menu_events(event):
    go_back_button.handle_event(event)

def settings_menu_draw():
    text_surface = font.render("No settings yet :(", True, text_color)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 100))
    display.blit(text_surface, text_rect)
    go_back_button.draw(display)

# game
def game_menu_events(event):
    for tile in tiles:
        tile.handle_event(event)

def game_menu_draw():
    for tile in tiles:
        tile.draw(display)

# register the menus
menu_manager.register_menu("start", start_menu_events, start_menu_draw)
menu_manager.register_menu("settings", settings_menu_events, settings_menu_draw)
menu_manager.register_menu("game", game_menu_events, game_menu_draw)

menu_manager.change_menu("start")


# main loopy loopy
if __name__ == "__main__":
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            menu_manager.handle_event(event)

        menu_manager.draw()
        pygame.display.flip()
        clock.tick(TARGET_FPS)
