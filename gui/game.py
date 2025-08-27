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

# colourss
primary_colour     = (70, 130, 180)  # button background
hover_colour       = (51, 102, 145)  # button hover
text_colour        = (245, 245, 245) # button text
tile_colour        = (200, 200, 200) # tile main
tile_hover        = (170, 170, 170) # tile hover
tile_text         = (50, 50, 50)    # tile text
bg_colour          = (30, 30, 40)    # main background

red_tile          = (255, 0, 0)     # the red that a red tile is
red_tile_hover    = (220, 0, 0)     # the red that a hovered red tile is
yellow_tile       = (255, 255, 0)   # the yellow that a yellow tile is
yellow_tile_hover = (220, 220, 0)   # the yellow that a hovered yellow tile is

# variables
tiles = []
menu_manager = MenuManager(display, bg_colour)  # background colour
player = "red"
board_full = False

# menu functions
def start_game_func(*_):
    global board_full
    board_full = False
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
        col = []
        for r in range(ROWS):
            x = start_x + c * (TILE_SIZE + TILE_SPACING)
            y = start_y + r * (TILE_SIZE + TILE_SPACING)

            id = str(c * ROWS + r)
            
            tile = Button(
                x, y, TILE_SIZE, TILE_SIZE, "",
                tile_colour, tile_hover, tile_text, tile_press, None, 30, (id, c, r),
                rounding=30
            )
            col.append(tile)
        tiles.append(col)

def checkWin():
    global tiles, player

    colours = [yellow_tile, yellow_tile_hover] if player == "red" else [red_tile, red_tile_hover] # this is backwards on purpose

    rows, cols = (6, 7)
    winCount = 4
    for row in range(rows):
        for col in range(cols - winCount + 1):
            if all(tiles[col + i][row].colour in colours for i in range(winCount)):
                return [(col + i, row) for i in range(winCount)]
    for col in range(cols):
        for row in range(rows - winCount + 1):
            if all(tiles[col][row + i].colour in colours for i in range(winCount)):
                return [(col, row + i) for i in range(winCount)]
    for col in range(cols - winCount + 1):
        for row in range(rows - winCount + 1):
            if all(tiles[col + i][row + i].colour in colours for i in range(winCount)):
                return [(col + i, row + i) for i in range(winCount)]
    for col in range(cols - winCount + 1):
        for row in range(winCount - 1, rows):
            if all(tiles[col + i][row - i].colour in colours for i in range(winCount)):
                return [(col + i, row - i) for i in range(winCount)]

def drop_tile(col_index):
    global player
    column = tiles[col_index]

    # find the lowest unoccupied tile in this column
    for r in reversed(range(ROWS)):
        target_tile = column[r]

        # check if already taken (coloured by a player)
        if target_tile.colour == tile_colour:
            # claim this tile for the current player
            target_tile.colour = red_tile if player == "red" else yellow_tile
            target_tile.hover_colour = red_tile_hover if player == "red" else yellow_tile_hover

            # print(f"Player {player} placed at col {col_index}, row {r}")

            # switch turn
            player = "yellow" if player == "red" else "red"
            # print(f"Next turn: {player}")
            break
    else:
        # column is full
        print(f"Column {col_index} is full!")

def is_board_full():
    global tiles, board_full
    for col in tiles:
        for row in reversed(range(ROWS)):
            target = col[row]
            
            if target.colour == tile_colour:
                return False
    
    return True

def tile_press(tile: Button):
    global board_full

    id, col_index, row_index = tile.extra_data  # we only care about column
    drop_tile(col_index)

    win = checkWin()

    print(f"Win tiles: {win}")

    if win:
        print("Somebody won fr")

    if is_board_full():
        board_full = True
        print(f"Draw! The board is full.")
    

# button stuff
width, height = 280, 75
x = WINDOW_SIZE[0] / 2 - width / 2
y = WINDOW_SIZE[1] / 2 - height / 2

start_button = Button(x, y - 100, width, height, "Start Game",
                      primary_colour, hover_colour, text_colour,
                      start_game_func, "Baloo2-Bold.ttf", 50, rounding=8)

settings_button = Button(x, y - 100 + height * 2, width, height, "Settings",
                         primary_colour, hover_colour, text_colour,
                         settings_menu, "Baloo2-Bold.ttf", 50, rounding=8)

go_back_button = Button(x, y, width, height, "Go back",
                        primary_colour, hover_colour, text_colour,
                        go_back, "Baloo2-Bold.ttf", 50, rounding=8)

game_over_button = Button(x, y*2-50, width, height, "Go back",
                           primary_colour, hover_colour, text_colour,
                           go_back, "Baloo2-Bold.ttf", 50, rounding=8)

game_over_text = Button(x, 50, width, height/1.5, "text",
                        bg_colour, (0, 0, 0), text_colour,
                        None, "Baloo2-Bold.ttf", 50, rounding=8)

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
    text_surface = font.render("No settings yet :(", True, text_colour)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 100))
    display.blit(text_surface, text_rect)
    go_back_button.draw(display)


# game
def game_menu_events(event):
    if board_full:
        game_over_button.handle_event(event)
    else:
        for col in tiles:
            for tile in col:
                tile: Button
                tile.handle_event(event)

def game_menu_draw():
    global player
    for col in tiles:
        for tile in col:
            tile: Button
            tile.draw(display)

    if board_full:
        game_over_text.text = f"{'RED' if player == 'red' else 'YELLOW'} WINS"
        game_over_button.draw(display)
        game_over_text.draw(display)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_d:
                    board_full = True

            menu_manager.handle_event(event)

        menu_manager.draw()
        pygame.display.flip()
        clock.tick(TARGET_FPS)
