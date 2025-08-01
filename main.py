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
            row += "| " + colourTile(column[i]) + " "
        row += "|"
        rows.append(row)

    rows = rows[::-1]

    toPrint = ""
    for row in rows:
        toPrint += (row + "\n")

    line = '=' * (len(board) * 4 + 1)
    print(f"{line}\n{toPrint[:-1]}\n{line}")

def getIntInput(prompt):
    success = False
    inp = ""
    while not success:
        inp = input(prompt)
        try:
            inp = int(inp)
            break
        except:
            clear()
            printBoard(board)
            print("Only integers allowed")
    
    return inp

def colourTile(tile):
    if tile == 'R':
        return f"{Colours.BOLD}{Colours.RED}R{Colours.END}"
    elif tile == 'Y':
        return f"{Colours.BOLD}{Colours.YELLOW}Y{Colours.END}"
    else:
        return "O"

def checkWin(board):
    return False

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
            chosenColumn = getIntInput(f"{colourTile(player)} where do you want to drop your tile? 0-6.\n>>> ")
            tile = board[chosenColumn].index("O")
            break
        except ValueError:
            clear()
            printBoard(board)
            print("You chose a column that is full. Try again")
            tile = ""
        except IndexError:
            clear()
            printBoard(board)
            print("You chose a column outside of the board. Try again")
            tile = ""
    
    board[chosenColumn][tile] = player

    if checkWin(board):
        clear()
        printBoard()
        print(f"{colourTile(player)} won!")
        break

    if player == 'R':
        player = 'Y'
    else:
        player = 'R'