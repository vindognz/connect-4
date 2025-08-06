import numpy as np

class Connect4Env:
    ROWS = 6
    COLS = 7
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = -1

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=np.int8)
        self.current_player = self.PLAYER1

    def reset(self):
        self.board[:] = 0
        self.current_player = self.PLAYER1
        return self.get_state()

    def get_state(self):
        return self.board.copy(), self.current_player

    def available_actions(self):
        return [col for col in range(self.COLS) if self.board[0, col] == 0]

    def step(self, action):
        if action not in self.available_actions():
            raise ValueError("Invalid action")
        
        for row in reversed(range(self.ROWS)):
            if self.board[row][action] == 0:
                self.board[row][action] = self.current_player
                break

        done, winner = self.check_win()
        reward = 0
        if done:
            if winner == 0:
                reward = 0  # draw
            elif winner == self.current_player:
                reward = 1
            else:
                reward = -1
        self.current_player *= -1
        return self.get_state(), reward, done

    def check_win(self):
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                line = self.board[row, col:col + 4]
                if abs(sum(line)) == 4:
                    return True, np.sign(sum(line))

        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                line = self.board[row:row + 4, col]
                if abs(sum(line)) == 4:
                    return True, np.sign(sum(line))

        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                diag = [self.board[row + i][col + i] for i in range(4)]
                if abs(sum(diag)) == 4:
                    return True, np.sign(sum(diag))

        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                diag = [self.board[row - i][col + i] for i in range(4)]
                if abs(sum(diag)) == 4:
                    return True, np.sign(sum(diag))

        if all(self.board[0, :] != 0):
            return True, 0  # draw

        return False, None
