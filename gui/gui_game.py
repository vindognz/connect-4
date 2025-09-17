import pygame
from pathlib import Path
from button import Button
from menu_manager import MenuManager
import random

# consts
ROOT_PATH = Path(__file__).parent

TARGET_FPS = 60
COLS, ROWS = 7, 6
TILE_SIZE, TILE_SPACING = 50, 20

WINDOW_WIDTH, WINDOW_HEIGHT = 768, 768

GRID_WIDTH = COLS * TILE_SIZE + (COLS - 1) * TILE_SPACING
GRID_HEIGHT = ROWS * TILE_SIZE + (ROWS - 1) * TILE_SPACING

GRID_ORIGIN_X = None
GRID_ORIGIN_Y = None

CURSOR_HEIGHT = 18
CURSOR_MARGIN = 14

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

# --- Backend board ---
board = [["." for _ in range(ROWS)] for _ in range(COLS)]

# game state
tiles: list[list[Button]] = []
player = "r"
board_full = False
winner = None

cursor_col = COLS // 2
last_tile = None

key_held = None
key_held_time = 0
initial_delay = 200
repeat_interval = 100

cpu = False

# --- Board logic ---
def create_board():
    global board
    board = [["." for _ in range(ROWS)] for _ in range(COLS)]

def drop_tile(board, col, piece):
    for r in reversed(range(ROWS)):
        if board[col][r] == ".":
            board[col][r] = piece
            return r
    return None

def check_win(board, piece):
    winCount = 4
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - winCount + 1):
            if all(board[col + i][row] == piece for i in range(winCount)):
                return [(col + i, row) for i in range(winCount)]
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - winCount + 1):
            if all(board[col][row + i] == piece for i in range(winCount)):
                return [(col, row + i) for i in range(winCount)]
    # Diagonal \
    for col in range(COLS - winCount + 1):
        for row in range(ROWS - winCount + 1):
            if all(board[col + i][row + i] == piece for i in range(winCount)):
                return [(col + i, row + i) for i in range(winCount)]
    # Diagonal /
    for col in range(COLS - winCount + 1):
        for row in range(winCount - 1, ROWS):
            if all(board[col + i][row - i] == piece for i in range(winCount)):
                return [(col + i, row - i) for i in range(winCount)]
    return None

def is_board_full(board):
    return all(board[c][0] != "." for c in range(COLS))

def lowest_empty_row(board, col):
    for r in reversed(range(ROWS)):
        if board[col][r] == ".":
            return r
    return None

# --- Sync backend board → buttons ---
def sync_board_to_buttons(board, tiles):
    for c in range(COLS):
        for r in range(ROWS):
            val = board[c][r]
            if val == "r":
                tiles[c][r].colour = red_tile
                tiles[c][r].hover_colour = red_tile_hover
            elif val == "y":
                tiles[c][r].colour = yellow_tile
                tiles[c][r].hover_colour = yellow_tile_hover
            else:
                tiles[c][r].colour = tile_colour
                tiles[c][r].hover_colour = tile_hover

# --- Tile + Button setup ---
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

            # bind column to callback, ignore button argument
            callback = lambda *_, col=c: play_move(col)

            tile = Button(
                x, y, TILE_SIZE, TILE_SIZE, "",
                tile_colour, tile_hover, tile_text,
                callback, None, 30, (c, r),
                rounding=30, outline_colour=(0,0,0), outline_width=5,
                hover_action=tile_hover_event
            )
            col.append(tile)
        tiles.append(col)

# --- Gameplay ---
def play_move(col_index, *_):
    global board_full, winner, player, last_tile, cpu

    if board_full or not tiles:
        return

    row_dropped = drop_tile(board, col_index, player)
    if row_dropped is None:
        return

    last_tile = (col_index, row_dropped)

    wins = check_win(board, player)
    if wins:
        winner = player
        for winX, winY in wins:
            tiles[winX][winY].outline_width = 5
            tiles[winX][winY].outline_colour = win_outline_colour
        board_full = True
    elif is_board_full(board):
        winner = None
        board_full = True
    else:
        player = "y" if player == "r" else "r"

def tile_hover_event(tile: Button):
    col_index, _ = tile.extra_data
    global cursor_col
    cursor_col = col_index

def column_is_full(c: int) -> bool:
    return all(board[c][r] != "." for r in range(ROWS))

# --- Ghost + Cursor ---
def draw_ghost_piece(display):
    if not tiles or GRID_ORIGIN_X is None:
        return
    row = lowest_empty_row(board, cursor_col)
    if row is None:
        return

    base_color = red_tile if player == "r" else yellow_tile
    ghost_color = (*base_color, 120)

    x = GRID_ORIGIN_X + cursor_col * (TILE_SIZE + TILE_SPACING)
    y = GRID_ORIGIN_Y + row * (TILE_SIZE + TILE_SPACING)

    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, ghost_color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 4)
    pygame.draw.circle(surf, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 4, 3)

    display.blit(surf, (x, y))

def draw_cursor(display):
    if not tiles or GRID_ORIGIN_X is None:
        return
    base_color = red_tile if player == "r" else yellow_tile
    color = base_color if not column_is_full(cursor_col) else (120, 120, 120)
    col_center_x = GRID_ORIGIN_X + cursor_col * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2
    y_top = GRID_ORIGIN_Y + GRID_HEIGHT + CURSOR_MARGIN
    points = [
        (col_center_x, y_top),
        (col_center_x - TILE_SIZE//3, y_top + CURSOR_HEIGHT),
        (col_center_x + TILE_SIZE//3, y_top + CURSOR_HEIGHT),
    ]
    pygame.draw.polygon(display, color, points)

# --- Draw game ---
def draw_game(display):
    sync_board_to_buttons(board, tiles)

    if board_full:
        if winner:
            game_over_text.text = f"{'Red' if winner == 'r' else 'Yellow'} wins!"
            game_over_text.text_colour = red_tile if winner == "r" else yellow_tile
        else:
            game_over_text.text = "It's a draw!"
            game_over_text.text_colour = text_colour
        game_over_button.draw(display)
    else:
        game_over_text.text = "Red's turn!" if player == "r" else "Yellow's turn!"
        game_over_text.text_colour = red_tile if player == "r" else yellow_tile

    game_over_text.draw(display)

    if not board_full:
        draw_cursor(display)
        draw_ghost_piece(display)

    if last_tile:
        img = pygame.image.load(str(ROOT_PATH / "star.png"))
        tiles[last_tile[0]][last_tile[1]].img = img

# --- Menus ---
width, height = 280, 75
x = WINDOW_WIDTH / 2 - width / 2
y = WINDOW_HEIGHT / 2 - height / 2

start_button = Button(x, y - 100, width, height, "Start Game",
                      primary_colour, hover_colour, text_colour,
                      lambda *_: menu_manager.change_menu("mode_pick"),
                      font, 50, rounding=8)

pvp_button = Button(x-50, y-height/1.5, width+100, height, "Player vs Player",
                    primary_colour, hover_colour, text_colour,
                    lambda *_: start_game("pvp"), font, 50, rounding=8)

pvc_button = Button(x-50, y+height/1.5, width+100, height, "Player vs CPU",
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

def start_game(mode):
    global board_full, winner, player, cursor_col, last_tile, cpu
    board_full = False
    winner = None
    player = "r"
    cursor_col = COLS // 2
    last_tile = None
    create_board()
    create_tiles()
    cpu = (mode == "cpu")
    menu_manager.change_menu("game")

def draw_settings(display):
    text_surface = font.render("No settings yet :(", True, text_colour)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
    display.blit(text_surface, text_rect)

# --- Menu manager ---
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

# --- Cursor move ---
def move_cursor(direction: str):
    global cursor_col
    if direction == "left":
        cursor_col = (cursor_col - 1) % COLS
    elif direction == "right":
        cursor_col = (cursor_col + 1) % COLS

def evalWindow(window, piece):
    opponent = "y" if piece == "r" else "r"
    player_count = window.count(piece)
    opponent_count = window.count(opponent)
    empty_count = window.count(".")
    score = 0

    if player_count == 4:
        score += 100
    elif player_count == 3 and empty_count == 1:
        score += 50
    elif player_count == 2 and empty_count == 2:
        score += 2

    if opponent_count == 3 and empty_count == 1:
        score -= 100
    return score

def evalPositionForPlayer(board, piece):
    score = 0
    # center column preference
    center_col = [board[COLS//2][r] for r in range(ROWS)]
    score += center_col.count(piece) * 3

    # horizontal
    for r in range(ROWS):
        row_array = [board[c][r] for c in range(COLS)]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evalWindow(window, piece)

    # vertical
    for c in range(COLS):
        col_array = board[c]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evalWindow(window, piece)

    # diagonals \
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            window = [board[c+i][r+i] for i in range(4)]
            score += evalWindow(window, piece)

    # diagonals /
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            window = [board[c+i][r-i] for i in range(4)]
            score += evalWindow(window, piece)

    return score

def evalPosition(board):
    return evalPositionForPlayer(board, "r") - evalPositionForPlayer(board, "y")

# --- CPU ---
def cpu_move_provider(depth=4):
    allowed = [c for c in range(COLS) if board[c][0] == "."]
    if not allowed:
        return None

    def minimax(bd, depth, alpha, beta, maximizing):
        if check_win(bd, "r"):
            return float('inf')
        if check_win(bd, "y"):
            return float('-inf')
        if is_board_full(bd) or depth == 0:
            return evalPosition(bd)

        allowed = [c for c in range(COLS) if lowest_empty_row(bd, c) is not None]

        if maximizing:
            maxEval = float('-inf')
            for col in allowed:
                row = lowest_empty_row(bd, col)
                bd[col][row] = "r"
                eval_score = minimax(bd, depth-1, alpha, beta, False)
                bd[col][row] = "."
                maxEval = max(maxEval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for col in allowed:
                row = lowest_empty_row(bd, col)
                bd[col][row] = "y"
                eval_score = minimax(bd, depth-1, alpha, beta, True)
                bd[col][row] = "."
                minEval = min(minEval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return minEval

    best_score = float('-inf') if player == "r" else float('inf')
    best_col = random.choice(allowed)

    for col in allowed:
        row = lowest_empty_row(board, col)
        board[col][row] = player
        score = minimax(board, depth-1, float('-inf'), float('inf'), player=="y")
        board[col][row] = "."
        if player == "r" and score > best_score:
            best_score = score
            best_col = col
        elif player == "y" and score < best_score:
            best_score = score
            best_col = col
    return best_col

# --- Main loop ---
if __name__ == "__main__":
    running = True
    while running:
        dt = clock.tick(TARGET_FPS)

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

        # CPU turn
        if cpu and player == 'y':
            move = cpu_move_provider()
            if move is not None:
                play_move(move)

        # Repeat key hold
        if key_held:
            key_held_time += dt
            if key_held_time > initial_delay:
                if (key_held_time - initial_delay) // repeat_interval > \
                   (key_held_time - initial_delay - dt) // repeat_interval:
                    move_cursor(key_held)

        display.fill(bg_colour)
        menu_manager.draw()
        pygame.display.flip()
