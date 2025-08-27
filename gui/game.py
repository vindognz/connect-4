import pygame
from pathlib import Path
from button import Button
from menu_manager import MenuManager

# consts
ROOT_PATH = Path(__file__).parent
WINDOW_SIZE = (768, 768)
TARGET_FPS = 60
COLS, ROWS = 7, 6
TILE_SIZE, TILE_SPACING = 50, 20

GRID_WIDTH = COLS * TILE_SIZE + (COLS - 1) * TILE_SPACING
GRID_HEIGHT = ROWS * TILE_SIZE + (ROWS - 1) * TILE_SPACING

# inits
pygame.init()
font = pygame.font.Font(ROOT_PATH / "Baloo2-Bold.ttf", 50)
display = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# coloursss
primary_colour     = (70, 130, 180)
hover_colour       = (51, 102, 145)
text_colour        = (245, 245, 245)
tile_colour        = (200, 200, 200)
tile_hover         = (170, 170, 170)
tile_text          = (50, 50, 50)
bg_colour          = (30, 30, 40)

red_tile           = (255, 0, 0)
red_tile_hover     = (220, 0, 0)
yellow_tile        = (255, 255, 0)
yellow_tile_hover  = (220, 220, 0)

# game state inits
tiles = []
player = "red"
board_full = False
winner = None  # "red", "yellow", or None for draw

# tile + board logic
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
            tile = Button(
                x, y, TILE_SIZE, TILE_SIZE, "",
                tile_colour, tile_hover, tile_text,
                tile_press, None, 30, (c, r),
                rounding=30
            )
            col.append(tile)
        tiles.append(col)

def drop_tile(col_index):
    column = tiles[col_index]
    for r in reversed(range(ROWS)):
        target_tile = column[r]
        if target_tile.colour == tile_colour:
            if player == "red":
                target_tile.colour = red_tile
                target_tile.hover_colour = red_tile_hover
            else:
                target_tile.colour = yellow_tile
                target_tile.hover_colour = yellow_tile_hover
            return r  # row where tile landed
    return None  # column full

def check_win():
    global tiles, player

    colours = [yellow_tile, yellow_tile_hover] if player == "yellow" else [red_tile, red_tile_hover]

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

def is_board_full():
    for col in tiles:
        for tile in col:
            if tile.colour == tile_colour:
                return False
    return True

def tile_press(tile: Button):
    global board_full, winner, player
    if board_full:
        return

    col_index, row_index = tile.extra_data
    row_dropped = drop_tile(col_index)
    if row_dropped is None:
        return  # column full

    win = check_win()

    # check for win
    if win:
        winner = player
        board_full = True
    elif is_board_full():
        winner = None  # draw
        board_full = True
    else:
        player = "yellow" if player == "red" else "red"

# buttons
width, height = 280, 75
x = WINDOW_SIZE[0] / 2 - width / 2
y = WINDOW_SIZE[1] / 2 - height / 2

start_button = Button(x, y - 100, width, height, "Start Game",
                      primary_colour, hover_colour, text_colour,
                      lambda *_: start_game(), font, 50, rounding=8)

settings_button = Button(x, y - 100 + height * 2, width, height, "Settings",
                         primary_colour, hover_colour, text_colour,
                         lambda *_: menu_manager.change_menu("settings"),
                         font, 50, rounding=8)

go_back_button = Button(x, y, width, height, "Go back",
                        primary_colour, hover_colour, text_colour,
                        lambda *_: menu_manager.change_menu("start"),
                        font, 50, rounding=8)

game_over_button = Button(x, y * 2 - 50, width, height, "Go back",
                          primary_colour, hover_colour, text_colour,
                          lambda *_: menu_manager.change_menu("start"),
                          font, 50, rounding=8)

game_over_text = Button(x, 50, width, height / 1.5, "text",
                        bg_colour, (0, 0, 0), text_colour,
                        None, font, 50, rounding=8)

# menu callbacks
def start_game():
    global board_full, player, winner
    board_full = False
    winner = None
    player = "red"
    create_tiles()
    menu_manager.change_menu("game")

def draw_settings(display):
    text_surface = font.render("No settings yet :(", True, text_colour)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 100))
    display.blit(text_surface, text_rect)

def draw_game(display):
    if board_full:
        if winner:
            game_over_text.text = f"{winner.upper()} wins!"
        else:
            game_over_text.text = "Draw!"
        game_over_button.draw(display)
        game_over_text.draw(display)

# menu manager init + setup
menu_manager = MenuManager(display, bg_colour)

menu_manager.register_menu("start",
    buttons=[start_button, settings_button]
)

menu_manager.register_menu("settings",
    buttons=[go_back_button],
    draw=draw_settings
)

menu_manager.register_menu("game",
    buttons=lambda: [tile for col in tiles for tile in col] + ([game_over_button] if board_full else []),
    draw=draw_game
)

menu_manager.change_menu("start")

# main loop
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
