import pygame
from pathlib import Path
from button import Button
from menu_manager import MenuManager

# consts
ROOT_PATH = Path(__file__).parent

TARGET_FPS = 60
COLS, ROWS = 7, 6
TILE_SIZE, TILE_SPACING = 50, 20

WINDOW_WIDTH, WINDOW_HEIGHT = 768, 768

GRID_WIDTH = COLS * TILE_SIZE + (COLS - 1) * TILE_SPACING
GRID_HEIGHT = ROWS * TILE_SIZE + (ROWS - 1) * TILE_SPACING

# grid origin cache for cursor drawing
GRID_ORIGIN_X = None
GRID_ORIGIN_Y = None

# cursor attributes
CURSOR_HEIGHT = 18
CURSOR_MARGIN = 14

# inits
pygame.init()
font = pygame.font.Font(ROOT_PATH / "Baloo2-Bold.ttf", 50)
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# colours
primary_colour     = (70, 130, 180)
hover_colour       = (51, 102, 145)
text_colour        = (245, 245, 245)
tile_colour        = (200, 200, 200)
tile_hover         = (170, 170, 170)
tile_text          = (50, 50, 50)
bg_colour          = (30, 30, 40)
win_outline_colour = (0, 255, 0)

red_tile           = (255, 0, 0)
red_tile_hover     = (220, 0, 0)
yellow_tile        = (255, 255, 0)
yellow_tile_hover  = (220, 220, 0)

# game state inits
tiles = []
player = "red"
board_full = False
winner = None

# cursor state
cursor_col = COLS // 2

last_tile = None

# repeat cursor move
key_held = None
key_held_time = 0
initial_delay = 200  # ms before repeat starts
repeat_interval = 100  # ms between repeats

# tile + board logic
def create_tiles():
    global tiles, GRID_ORIGIN_X, GRID_ORIGIN_Y
    tiles = []

    start_x = (WINDOW_WIDTH - GRID_WIDTH) // 2
    start_y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

    GRID_ORIGIN_X, GRID_ORIGIN_Y = start_x, start_y

    for c in range(COLS):
        col = []
        for r in range(ROWS):
            x = start_x + c * (TILE_SIZE + TILE_SPACING)
            y = start_y + r * (TILE_SIZE + TILE_SPACING)
            tile = Button(
                x, y, TILE_SIZE, TILE_SIZE, "",
                tile_colour, tile_hover, tile_text,
                tile_press, None, 30, (c, r),
                rounding=30, outline_colour=(0,0,0), outline_width=5,
                hover_action=tile_hover_event
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
            return r
    
def check_win():
    global tiles, player

    colours = [yellow_tile, yellow_tile_hover] if player == "yellow" else [red_tile, red_tile_hover]

    winCount = 4
    for row in range(ROWS):
        for col in range(COLS - winCount + 1):
            if all(tiles[col + i][row].colour in colours for i in range(winCount)):
                return [(col + i, row) for i in range(winCount)]
    for col in range(COLS):
        for row in range(ROWS - winCount + 1):
            if all(tiles[col][row + i].colour in colours for i in range(winCount)):
                return [(col, row + i) for i in range(winCount)]
    for col in range(COLS - winCount + 1):
        for row in range(ROWS - winCount + 1):
            if all(tiles[col + i][row + i].colour in colours for i in range(winCount)):
                return [(col + i, row + i) for i in range(winCount)]
    for col in range(COLS - winCount + 1):
        for row in range(winCount - 1, ROWS):
            if all(tiles[col + i][row - i].colour in colours for i in range(winCount)):
                return [(col + i, row - i) for i in range(winCount)]

def is_board_full():
    for col in tiles:
        for tile in col:
            if tile.colour == tile_colour:
                return False
    return True

# drop a tile in a column
def play_move(col_index: int):
    global board_full, winner, player, last_tile
    if board_full or not tiles:
        return

    row_dropped = drop_tile(col_index)
    if row_dropped is None:
        return

    if last_tile:
        tiles[last_tile[0]][last_tile[1]].img = None
    last_tile = (col_index, row_dropped)

    wins = check_win()
    if wins:
        winner = player
        for winX, winY in wins:
            tiles[winX][winY].outline_width = 5
            tiles[winX][winY].outline_colour = win_outline_colour
        board_full = True
    elif is_board_full():
        winner = None
        board_full = True
    else:
        player = "yellow" if player == "red" else "red"

def tile_press(tile: Button):
    col_index, _row_index = tile.extra_data
    play_move(col_index)

def tile_hover_event(tile: Button):
    col_index, _row_index = tile.extra_data
    global cursor_col
    cursor_col = col_index

# buttons
width, height = 280, 75
x = WINDOW_WIDTH / 2 - width / 2
y = WINDOW_HEIGHT / 2 - height / 2

start_button = Button(x, y - 100, width, height, "Start Game",
                      primary_colour, hover_colour, text_colour,
                      lambda *_: menu_manager.change_menu("mode_pick"),
                      font, 50, rounding=8)

pvp_button = Button(x, y-height/1.5, width, height, "Player vs Player",
                    primary_colour, hover_colour, text_colour,
                    lambda *_: start_game("pvp"), font, 50, rounding=8)

pvc_button = Button(x, y+height/1.5, width, height, "Player vs CPU",
                    primary_colour, hover_colour, text_colour,
                    lambda *_: start_game("cpu"), font, 50, rounding=8)

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
def start_game(mode):
    if mode == "pvp":
        global board_full, winner, player, cursor_col, last_tile
        board_full = False
        winner = None
        player = "red"
        cursor_col = COLS // 2
        last_tile = None
        create_tiles()
        menu_manager.change_menu("game")
    elif mode == "cpu":
        print("not implemented yet. give me money and i might make it fr")

def draw_settings(display):
    text_surface = font.render("No settings yet :(", True, text_colour)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
    display.blit(text_surface, text_rect)

# checks if a column is full
def column_is_full(c: int) -> bool:
    return all(t.colour != tile_colour for t in tiles[c])

# helper for ghost, find the lowest empty tile
def lowest_empty_row(c: int):
    for r in reversed(range(ROWS)):
        if tiles[c][r].colour == tile_colour:
            return r
    
# ghost preview tile
def draw_ghost_piece(display):
    if not tiles or GRID_ORIGIN_X is None:
        return
    row = lowest_empty_row(cursor_col)
    if row is None:  # column full
        return

    # semi-transparent ghost color
    base_color = red_tile if player == "red" else yellow_tile
    ghost_color = (*base_color, 120)  # RGBA

    # compute position
    x = GRID_ORIGIN_X + cursor_col * (TILE_SIZE + TILE_SPACING)
    y = GRID_ORIGIN_Y + row * (TILE_SIZE + TILE_SPACING)

    # create surface with alpha
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, ghost_color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 4)
    # white outline for ghost
    pygame.draw.circle(surf, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 4, 3)

    display.blit(surf, (x, y))

# draws the cursor
def draw_cursor(display):
    if not tiles or GRID_ORIGIN_X is None:
        return
    base_color = red_tile if player == "red" else yellow_tile
    color = base_color if not column_is_full(cursor_col) else (120, 120, 120)
    col_center_x = GRID_ORIGIN_X + cursor_col * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2
    y_top = GRID_ORIGIN_Y + GRID_HEIGHT + CURSOR_MARGIN
    points = [
        (col_center_x, y_top),
        (col_center_x - TILE_SIZE//3, y_top + CURSOR_HEIGHT),
        (col_center_x + TILE_SIZE//3, y_top + CURSOR_HEIGHT),
    ]
    pygame.draw.polygon(display, color, points)

def draw_game(display):
    if board_full:
        if winner:
            game_over_text.text = f"{winner.title()} wins!"
            if winner == "red":
                game_over_text.text_colour = red_tile
            elif winner == "yellow":
                game_over_text.text_colour = yellow_tile
        else:
            game_over_text.text = "It's a draw!"
            game_over_text.text_colour = text_colour
        game_over_button.draw(display)
    else:
        game_over_text.text = "Red's turn!" if player == "red" else "Yellow's turn!"
        game_over_text.text_colour = red_tile if player == "red" else yellow_tile
    game_over_text.draw(display)

    if not board_full:
        draw_cursor(display)
        draw_ghost_piece(display)

    if last_tile:
        img = pygame.image.load(str(ROOT_PATH / "star.png"))
        tiles[last_tile[0]][last_tile[1]].img = img
 
# menu manager init
menu_manager = MenuManager(display, bg_colour)

menu_manager.register_menu("start",
    buttons=[start_button, settings_button]
)

menu_manager.register_menu("mode_pick",
    buttons=[pvp_button, pvc_button]
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

# cursor movement + wrapping
def move_cursor(direction: str):
    global cursor_col
    if direction == "left":
        cursor_col = (cursor_col - 1) % COLS
    elif direction == "right":
        cursor_col = (cursor_col + 1) % COLS

# main loop
if __name__ == "__main__":
    running = True
    while running:
        dt = clock.tick(TARGET_FPS) # time since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_d:
                    board_full = True
                elif event.key == pygame.K_LEFT:
                    move_cursor("left")
                    key_held = "left"
                    key_held_time = 0
                elif event.key == pygame.K_RIGHT:
                    move_cursor("right")
                    key_held = "right"
                    key_held_time = 0
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    if tiles and not board_full and not column_is_full(cursor_col):
                        play_move(cursor_col)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    key_held = None
                    key_held_time = 0

            menu_manager.handle_event(event)

        # repeat held key
        if key_held:
            key_held_time += dt
            if key_held_time > initial_delay:
                if (key_held_time - initial_delay) // repeat_interval > \
                   (key_held_time - initial_delay - dt) // repeat_interval:
                    move_cursor(key_held)

        display.fill(bg_colour)
        menu_manager.draw()
        pygame.display.flip()
