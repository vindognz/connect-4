board = '0'*42
player = '1'

def clear():
    print(end='\033[2J\033[1;1H',flush=True)

def prettyChar(char):
    if char == "0":
        return " "
    elif char == "1":
        return "R"
    elif char == "2":
        return "Y"
    
    else:
        return "C"

def printBoard():
    global board

    boardChunks = []

    for i in range(0, len(board), 7):
        chunk = board[i:i+7]
        boardChunks.append(chunk)

    print("         CONNECT FOUR")
    print("=============================")

    for chunk in boardChunks:
        row = "|"
        for tile in chunk:
            row += f" {prettyChar(tile)} |"
        print(row)

    print("=============================")
    
def getColumn():
    global player
    while True:
        try:
            column = int(input(f"{prettyChar(player)}, where drop the tile? "))-1
            return column
        except ValueError:
            print("bro enter an int")

def dropTile(col):
    global board, player
    index = next((row * 7 + col for row in range(5, -1, -1) if board[row * 7 + col] == '0'), None)

    if index is None:
        raise ValueError("Column is full")
    
    board = board[:index] + str(player) + board[index+1:]

while True:
    clear()
    printBoard()
    while True:
        try:
            col = getColumn()
            dropTile(col)
            break
        except KeyboardInterrupt:
            print("toodle-oo")
            exit()
        except:
            print('monkey')
            print(player)


    player = "2" if player == "1" else "1"