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
    print("===============")

    rows = []

    for column in board:
        row = ""
        for i in range(len(column)):
            index = board.index(column)
            row += "|" + board[index][i]
        rows.append(row+"\n")

    rows = rows[::-1]

    toPrint = ""
    for row in rows:
        toPrint += row

    print(toPrint)
    

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

    try:
        chosenColumn = int(input(f"{turn} where do you want to drop your tile? 1-7.\n>>> "))
    except Exception as e:
        print("Please enter a positive integer.")

    try:
        tile = findLowest(board, chosenColumn)
    except ValueError:
        print("You chose a column that is full. Try again")
    
    board[chosenColumn][tile] = turn

    print(board)
    printBoard(board)

    input()

    turn = 'Y' if turn == 'R' else 'R'

