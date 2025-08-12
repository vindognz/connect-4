import os
import sys
from colours import Colours as C
import random
import json

# ===========================
# |     Helper functions    |
# ===========================

def clear():
    os.system('cls' if sys.platform.startswith('win') else 'clear')

def colourTile(tile):
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        mode = settings.get("display_mode", "coloured_text")
    except (FileNotFoundError, json.JSONDecodeError):
        mode = "coloured_text"

    if mode == "coloured_text":
        if tile == 'R':
            return f"{C.BOLD}{C.RED} R {C.END}"
        elif tile == 'Y':
            return f"{C.BOLD}{C.YELLOW} Y {C.END}"
        elif tile == 'r':
            return f"{C.BOLD}{C.LIGHT_GREEN} R {C.END}"
        elif tile == 'y':
            return f"{C.BOLD}{C.LIGHT_GREEN} Y {C.END}"
        else:
            return " O "

    elif mode == "coloured_background":
        if tile == 'R':
            return f"{C.BG_RED}   {C.END}"
        elif tile == 'Y':
            return f"{C.BG_LIGHT_YELLOW}   {C.END}"
        elif tile == 'r':
            return f"{C.BG_LIGHT_GREEN}{C.BOLD} R {C.END}"
        elif tile == 'y':
            return f"{C.BG_LIGHT_GREEN}{C.BOLD} Y {C.END}"
        else:
            return "   "

    elif mode == "emojis":
        if tile.lower() == 'r':
            return "🔴"
        elif tile.lower() == 'y':
            return "🟡"
        else:
            return "⚪"

    return tile

def printBoard(board):

    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        mode = settings.get("display_mode", "coloured_text")
    except (FileNotFoundError, json.JSONDecodeError):
        mode = "coloured_text"

    rows = []
    for i in range(6):
        row = ""
        for column in board:
            row += f"{C.BOLD}|{C.END}{colourTile(column[i])}"
        row += f"{C.BOLD}|{C.END}"
        rows.append(row)
    rows.reverse()

    if mode == "emojis":
        top = f"""     {C.BOLD}CONNECT FOUR
======================{C.END}"""
        bottom = f"{C.BOLD}==1==2==3==4==5==6==7=={C.END}"
    else:
        top = f"""        {C.BOLD}CONNECT  FOUR
============================={C.END}"""
        bottom = f"{C.BOLD}==1===2===3===4===5===6===7=={C.END}"

#     print(f"""        {C.BOLD}CONNECT  FOUR
# ============================={C.END}
# {'\n'.join(rows)}
# {C.BOLD}==1===2===3===4===5===6===7=={C.END}""")
    print(f"{top}\n{'\n'.join(rows)}\n{bottom}")


def getIntInput(prompt, board=None):
    while True:
        inp = input(prompt)
        try:
            inp = int(inp)
            if not 1 <= inp <= 7:
                raise ValueError
            return inp
        except ValueError:
            clear()
            if board:
                printBoard(board)
            print("Only integers 1-7 allowed")

def checkWin(board, player):
    rows, cols = (6, 7)
    winCount = 4
    for row in range(rows):
        for col in range(cols - winCount + 1):
            if all(board[col + i][row] == player for i in range(winCount)):
                return [(col + i, row) for i in range(winCount)]
    for col in range(cols):
        for row in range(rows - winCount + 1):
            if all(board[col][row + i] == player for i in range(winCount)):
                return [(col, row + i) for i in range(winCount)]
    for col in range(cols - winCount + 1):
        for row in range(rows - winCount + 1):
            if all(board[col + i][row + i] == player for i in range(winCount)):
                return [(col + i, row + i) for i in range(winCount)]
    for col in range(cols - winCount + 1):
        for row in range(winCount - 1, rows):
            if all(board[col + i][row - i] == player for i in range(winCount)):
                return [(col + i, row - i) for i in range(winCount)]

def isTerminalNode(board):
    if checkWin(board, 'R'):
        return "WinX"
    elif checkWin(board, 'Y'):
        return "WinY"

    if all('O' not in col for col in board):
        return "Draw"

    return False

def evalWindow(window, player):
    opponent = 'Y' if player == 'R' else 'R'

    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count('O')

    score = 0
    if player_count == 4:
        score += 100
    elif player_count == 3 and empty_count == 1:
        score += 5
    elif player_count == 2 and empty_count == 2:
        score += 2
    
    if opponent_count == 3 and empty_count == 1:
        score -= 4
    
    return score

def evalPositionForPlayer(board, player):
    score = 0

    # Score center column
    center_col = len(board) // 2
    center_array = board[center_col]
    center_count = center_array.count(player)
    score += center_count * 3

    # Score Horizontal
    for row in range(len(board[0])):
        row_array = [board[col][row] for col in range(len(board))]
        for col in range(len(board) - 3):
            window = row_array[col:col+4]
            score += evalWindow(window, player)

    # Score Vertical
    for col in range(len(board)):
        col_array = board[col]
        for row in range(len(board[col]) - 3):
            window = col_array[row:row+4]
            score += evalWindow(window, player)

    # Score positive diagonals
    for col in range(len(board) - 3):
        for row in range(len(board[0]) - 3):
            window = [board[col+i][row+i] for i in range(4)]
            score += evalWindow(window, player)

    # Score negative diagonals
    for col in range(len(board) - 3):
        for row in range(3, len(board[0])):
            window = [board[col+i][row-i] for i in range(4)]
            score += evalWindow(window, player)

    return score

def evalPosition(board):
    red_score = evalPositionForPlayer(board, 'R')
    yellow_score = evalPositionForPlayer(board, 'Y')
    return red_score - yellow_score

def minimax(board, depth, alpha, beta, maximisingPlayer):
    isTerminal = isTerminalNode(board)

    if isTerminal:
        if isTerminal == "WinX":  # Red wins
            return float('inf')
        elif isTerminal == "WinY":  # Yellow wins
            return float('-inf')
        elif isTerminal == "Draw":
            return 0

    allowedMoves = [i for i, col in enumerate(board) if 'O' in col]

    if depth == 0 or not allowedMoves:
        return evalPosition(board)

    if maximisingPlayer:
        maxEval = float('-inf')
        for move in allowedMoves:
            newPosition = [col.copy() for col in board]
            tile = newPosition[move].index("O")
            newPosition[move][tile] = 'R'

            evaluation = minimax(newPosition, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for move in allowedMoves:
            newPosition = [col.copy() for col in board]
            tile = newPosition[move].index("O")
            newPosition[move][tile] = 'Y'

            evaluation = minimax(newPosition, depth - 1, alpha, beta, True)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval

# ===========================
# |  Player move providers  |
# ===========================
def local_move_provider(player, board):
    col = getIntInput(f"{colourTile(player)} where do you want to drop your tile? 1-7.\n>>> ", board) - 1
    return col

# def cpu_move_provider(player, board):
#     col = 0
#     def other_player_gonna_win(my_move: int|None = None) -> int|bool:
#         if my_move == None: my_move = col
#         my_board = deepcopy(board)
#         my_board[my_move][my_board[my_move].index('O')] = player
        
#         other_p = 'Y' if player == 'R' else 'R'
#         for other_p_col in range(len(my_board)):
#             if 'O' not in my_board[other_p_col]:
#                 continue

#             new_board = deepcopy(my_board)
#             new_board[other_p_col][new_board[other_p_col].index('O')] = other_p
#             if checkWin(new_board, other_p) != None:
#                 return other_p_col
#         return False
    
#     def im_gonna_win() -> int|bool:
#         for possible_col in range(len(my_board)):
#             if 'O' not in my_board[other_p_col]:
#                 continue

#             new_board = deepcopy(my_board)
#             new_board[other_p_col][new_board[other_p_col].index('O')] = other_p
#             if checkWin(new_board, other_p) != None:
#                 return other_p_col
#         return False
    
#     # Start with a random move
#     col = random.randint(0,6)
#     while not any([t == 'O' for t in board[col]]):
#         col += 1
#         if col == 7: col = 0
    
#     # Prevent other player winning 1 move deep
#     if other_player_gonna_win():
#         col = other_player_gonna_win()

#     time.sleep((random.random()*0.5)+0.25)  # Simulate thinking time
#     return col

def cpu_move_provider(player, board):
    allowedMoves = [i for i, col in enumerate(board) if 'O' in col]

    best_score = float('-inf') if player == 'R' else float('inf')
    best_move = None

    search_depth = 5
    maximising = True if player == 'R' else False

    for move in allowedMoves:
        newBoard = [col.copy() for col in board]
        tile = newBoard[move].index('O')
        newBoard[move][tile] = player

        score = minimax(newBoard, search_depth - 1, float('-inf'), float('inf'), not maximising)  # because next move is opponent's turn

        if player == 'R':
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    if best_move is None:
        best_move = random.choice(allowedMoves)

    return best_move

# ===========================
# |      Main game loop     |
# ===========================
def play_game(player1_get_move, player2_get_move):
    board = [['O'] * 6 for _ in range(7)]
    player = 'R'

    while True:
        clear()
        printBoard(board)

        # Get column from correct player
        if player == 'R':
            col = player1_get_move(player, board)
        else:
            col = player2_get_move(player, board)

        try:
            tile = board[col].index("O")
        except ValueError:
            continue

        board[col][tile] = player

        winPositions = checkWin(board, player)
        if winPositions:
            for x, y in winPositions:
                board[x][y] = board[x][y].lower()
            clear()
            printBoard(board)
            print(f"{colourTile(player)} won!")
            input("Press ENTER to return to the menu.")
            break

        player = 'Y' if player == 'R' else 'R'

# ===========================
# |          Modes          |
# ===========================
def play_local_pvp():
    play_game(local_move_provider, local_move_provider)

def play_lan_server():
    print("PvP LAN is in maintenance due to exploits.!")
    input("Press Enter to return to menu...")
    return
        
def play_lan_client():
    print("PvP LAN is in maintenance due to exploits.!")
    input("Press Enter to return to menu...")
    return

def play_vs_computer():
    # play_game(cpu_move_provider, local_move_provider)
    play_game(local_move_provider, cpu_move_provider)

# ===========================
# |           Menu          |
# ===========================

def edit_settings():
    settings_file = "settings.json"

    # Default settings if no file exists
    default_settings = {
        "display_mode": "coloured_text"  # options: coloured_text, coloured_background, emojis
    }

    # Load existing settings
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                settings = default_settings.copy()
    else:
        settings = default_settings.copy()

    # Keep a copy for detecting unsaved changes
    original_settings = settings.copy()

    def save_settings():
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=4)
        print("Settings saved.")
        input("Press Enter to return to main menu...")

    while True:
        clear()
        print("=== Settings Menu ===")
        print("1. Display Mode")
        print("--------------------")
        print("S. Save and Exit")
        print("E. Exit without Saving")
        print()
        print(f"Current Settings: {settings}")

        choice = input("Choose a setting to edit, or Save/Exit: ").strip().lower()

        if choice == "1":
            # Display Mode submenu
            while True:
                clear()
                print("=== Display Mode ===")
                modes = [
                    ("coloured_text", "Coloured Text"),
                    ("coloured_background", "Coloured Background"),
                    ("emojis", "Emojis")
                ]
                for i, (key, label) in enumerate(modes, start=1):
                    if settings["display_mode"] == key:
                        print(f"{i}. {C.BOLD}{label}{C.END}")
                    else:
                        print(f"{i}. {label}")
                print("B. Go Back")
                sub_choice = input("Choose a display mode: ").strip().lower()
                if sub_choice == "b":
                    break
                elif sub_choice in [str(i) for i in range(1, len(modes) + 1)]:
                    settings["display_mode"] = modes[int(sub_choice) - 1][0]
                    print(f"Display mode set to {settings['display_mode']}")
                else:
                    input("Invalid choice. Press Enter to try again...")

        elif choice == "save" or choice == "s":
            save_settings()
            return

        elif choice == "exit" or choice == "e":
            if settings != original_settings:
                confirm = input("You have unsaved changes. Exit without saving? (y/n): ").lower()
                if confirm == "y":
                    return
            else:
                return

        else:
            input("Invalid choice. Press Enter to try again...")

while True:
    clear()
    print("How do you want to play?")
    print("1. PvP (same device)")
    print("2. PvP (LAN)")
    print("3. PvC (vs computer)")
    print("4. Edit settings")
    print("4. Quit")
    choice = input("Choose 1-4: ").strip()
    if choice == "1":
        play_local_pvp()
    elif choice == "2":
        if input("Are you hosting? (y/n): ").lower() == "y":
            play_lan_server()
        else:
            play_lan_client()
    elif choice == "3":
        play_vs_computer()
    elif choice == "4":
        edit_settings()
    elif choice == "5":
        break
    else:
        input("Invalid choice. Press Enter to try again...")
