import os
import sys
from copy import deepcopy
from colours import Colours as C
import random

# ===========================
# |     Helper functions    |
# ===========================
def clear():
    os.system('cls' if sys.platform.startswith('win') else 'clear')

def colourTile(tile):
    if tile == 'R':
        return f"{C.BOLD}{C.RED}R{C.END}"
    elif tile == 'Y':
        return f"{C.BOLD}{C.YELLOW}Y{C.END}"
    elif tile == 'r':
        return f"{C.BOLD}{C.LIGHT_GREEN}R{C.END}"
    elif tile == 'y':
        return f"{C.BOLD}{C.LIGHT_GREEN}Y{C.END}"
    else:
        return "O"

def printBoard(board):
    rows = []
    for i in range(6):
        row = ""
        for column in board:
            row += f"{C.BOLD}| {C.END}" + colourTile(column[i]) + " "
        row += f"{C.BOLD}|{C.END}"
        rows.append(row)
    rows.reverse()

    print(f"""        {C.BOLD}CONNECT  FOUR
============================={C.END}
{'\n'.join(rows)}
{C.BOLD}==1===2===3===4===5===6===7=={C.END}""")

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

# ===========================
# |  Player move providers  |
# ===========================
def local_move_provider(player, board):
    col = getIntInput(f"{colourTile(player)} where do you want to drop your tile? 1-7.\n>>> ", board) - 1
    return col

def cpu_move_provider(player, board):
    # start with a random move
    col = random.randint(0, 6)
    while 'O' not in board[col]:
        col += 1
        if col == 7:
            col = 0

    # prevent immediate wins
    other_p = 'Y' if player == 'R' else 'R'
    for other_p_col in range(len(board)):
        if 'O' not in board[other_p_col]:
            continue

        new_board = deepcopy(board)
        new_board[other_p_col][new_board[other_p_col].index('O')] = other_p
        if checkWin(new_board, other_p) != None:
            col = other_p_col
            break
    
    # take wins
    for possible_col in range(len(board)):
        if 'O' not in board[possible_col]:
            continue

        new_board = deepcopy(board)
        new_board[possible_col][new_board[possible_col].index('O')] = player
        if checkWin(new_board, player) != None:
            col = possible_col
            break
    
    return col

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
    play_game(cpu_move_provider, local_move_provider)

# ===========================
# |           Menu          |
# ===========================
while True:
    clear()
    print("How do you want to play?")
    print("1. PvP (same device)")
    print("2. PvP (LAN)")
    print("3. PvC (vs computer)")
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
        break
    else:
        input("Invalid choice. Press Enter to try again...")
