import os
import sys
from colours import Colours

def clear():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def printBoard(board):
    rows = []
    for i in range(6):
        row = ""
        for column in board:
            row += f"{Colours.BOLD}| {Colours.END}" + colourTile(column[i]) + " "
        row += f"{Colours.BOLD}|{Colours.END}"
        rows.append(row)

    rows = rows[::-1]

    toPrint = ""
    for row in rows:
        toPrint += (row + "\n")

    print(f"""        {Colours.BOLD}CONNECT  FOUR
============================={Colours.END}
{toPrint[:-1]}
{Colours.BOLD}==1===2===3===4===5===6===7=={Colours.END}""")

def getIntInput(prompt):
    inp = ""
    while True:
        inp = input(prompt)
        try:
            inp = int(inp)
            break
        except:
            clear()
            printBoard(board)
            print("Only positive integers 1-7 allowed")
    
    return inp

def colourTile(tile):
    if tile == 'R':
        return f"{Colours.BOLD}{Colours.RED}R{Colours.END}"
    elif tile == 'Y':
        return f"{Colours.BOLD}{Colours.YELLOW}Y{Colours.END}"
    elif tile == 'r': # winning red
        return f"{Colours.BOLD}{Colours.LIGHT_GREEN}R{Colours.END}"
    elif tile == 'y': # winning yellow
        return f"{Colours.BOLD}{Colours.LIGHT_GREEN}Y{Colours.END}"
    else:
        return "O"

def checkWin(board, player):
    rows, cols = (6, 7)
    winCount = 4

    # hoz check
    for row in range(rows):
        for col in range(cols - winCount + 1):
            if all(board[col + i][row] == player for i in range(winCount)):
                return [(col + i, row) for i in range(winCount)]
    
    # vert check
    for col in range(cols):
        for row in range(rows - winCount + 1):
            if all(board[col][row + i] == player for i in range(winCount)):
                return [(col, row + i) for i in range(winCount)]

    # diag / check
    for col in range(cols - winCount + 1):
        for row in range(rows - winCount + 1):
            if all(board[col + i][row + i] == player for i in range(winCount)):
                return [(col + i, row + i) for i in range(winCount)]

    # diag \ check
    for col in range(cols - winCount + 1):
        for row in range(winCount - 1, rows):
            if all(board[col + i][row - i] == player for i in range(winCount)):
                return [(col + i, row - i) for i in range(winCount)]

# Board will be 7x6.

# O = open, R = red, Y = yellow
# because this is defined like this, you could technically save a game then load from where you left off

# This is defined as columns, not rows. So tile 0 on column 0 is the bottom left tile of the board
board = [
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O'], 
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O'],
]

playing = True
player = 'R'

while playing:
    clear()
    printBoard(board)

    while True:
        try:
            chosenColumn = getIntInput(f"{colourTile(player)} where do you want to drop your tile? 1-7.\n>>> ") - 1
            if chosenColumn < 0:
                raise IndexError
            tile = board[chosenColumn].index("O")
            break
        except ValueError:
            clear()
            printBoard(board)
            print(f"{Colours.BOLD}You chose a column that is full. Try again{Colours.END}")
            tile = ""
        except IndexError:
            clear()
            printBoard(board)
            print(f"{Colours.BOLD}You chose a column outside of the board. Try again{Colours.END}")
            tile = ""
    
    board[chosenColumn][tile] = player
    
    winPositions = checkWin(board, player)
    if winPositions:
        for x, y in winPositions:
            board[x][y] = board[x][y].lower()

        clear()
        printBoard(board)
        print(f"{colourTile(player)} won!")
        break

    if player == 'R':
        player = 'Y'
    else:
        player = 'R'