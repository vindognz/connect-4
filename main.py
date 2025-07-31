import os
import sys

def clear():
    if sys.platform.startswith('win'):
        # For Windows
        os.system('cls')
    else:
        # For Linux and macOS
        os.system('clear')

def findLowest(board, column):
    return board[column].index("O")

"""
This is how the board should output:

===============
|O|O|O|O|O|O|O|
|O|O|O|O|O|O|O|
|O|O|O|O|O|O|O|
|O|O|O|O|O|O|O|
|O|O|O|O|O|O|O|
|O|O|O|O|O|O|O|
===============
"""

def printBoard(board):

    rows = []
    for i in range(6):
        row = ""
        for column in board:
            row += "|" + column[i]
        row += "|"
        rows.append(row)

    rows = rows[::-1]

    toPrint = ""
    for row in rows:
        toPrint += (row + "\n")

    print(f"===============\n{toPrint[:-1]}\n===============")

def getIntInput(prompt):
    success = False
    inp = ""
    while not success:
        inp = input(prompt)
        try:
            inp = int(inp)
            break
        except:
            print("Only integers allowed")
    
    return inp

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
turn = 'R'

while playing:
    clear()

    chosenColumn = getIntInput(f"{turn} where do you want to drop your tile? 1-7.\n>>> ")

    try:
        tile = findLowest(board, chosenColumn)
    except ValueError:
        print("You chose a column that is full. Try again")
    
    board[chosenColumn][tile] = turn

    printBoard(board)

    input()

    turn = 'Y' if turn == 'R' else 'R'
