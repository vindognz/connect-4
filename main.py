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

# Board will be 7x6.

# O = open, R = red, Y = yellow
# because this is defined like this, you could technically save a game then load from where you left off
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

    input()

    turn = 'Y' if turn == 'R' else 'R'