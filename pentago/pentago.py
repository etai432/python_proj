import numpy as np
import random


class Game:

    def __init__(self):
        self.board = np.full(1, 36)
        self.empty = []
        self.dict = {}

    def restart_board(self):
        self.board = np.full(1, 36)

    def check_win(self, last_index, turn):
        if self.board[last_index // 6 * 6] == self.board[last_index // 6 * 6 + 1] == self.board[last_index // 6 * 6 + 2] == self.board[last_index // 6 * 6 + 3] == self.board[last_index // 6 * 6 + 4] != 1:
            return turn
        if self.board[last_index // 6 * 6 + 5] == self.board[last_index // 6 * 6 + 1] == self.board[last_index // 6 * 6 + 2] == self.board[last_index // 6 * 6 + 3] == self.board[last_index // 6 * 6 + 4] != 1:
            return turn
        if self.board[last_index % 6] == self.board[last_index % 6 + 6] == self.board[last_index % 6 + 12] == self.board[last_index % 6 + 18] == self.board[last_index % 6 + 24] != 1:
            return turn
        if self.board[last_index % 6 + 30] == self.board[last_index % 6 + 6] == self.board[last_index % 6 + 12] == self.board[last_index % 6 + 18] == self.board[last_index % 6 + 24] != 1:
            return turn
        if self.board[0] == self.board[7] == self.board[14] == self.board[21] == self.board[28] != 1:
            return turn
        if self.board[35] == self.board[7] == self.board[14] == self.board[21] == self.board[28] != 1:
            return turn
        if self.board[1] == self.board[8] == self.board[15] == self.board[22] == self.board[29] != 1:
            return turn
        if self.board[6] == self.board[13] == self.board[20] == self.board[27] == self.board[34] != 1:
            return turn
        if self.board[5] == self.board[10] == self.board[15] == self.board[20] == self.board[25] != 1:
            return turn
        if self.board[30] == self.board[10] == self.board[15] == self.board[20] == self.board[25] != 1:
            return turn
        if self.board[4] == self.board[9] == self.board[14] == self.board[19] == self.board[24] != 1:
            return turn
        if self.board[11] == self.board[16] == self.board[21] == self.board[26] == self.board[31] != 1:
            return turn

    def empty_space(self):
        self.empty = np.where(self.board, 1)

    def computer_turn(self):
        pass

    def player_turn(self):
        self.empty_space()
        input1 = int(input("please pick a spot from the empty spaces: "))
        while input1 not in self.empty:
            input1 = int(input("please pick a spot from the empty spaces: "))
        self.print_board()
        print("insert the quarter you want to rotate:")
        print("1 | 2")
        input1 = int(input("3 | 4"))
        while input < 1 or input > 4:
            input1 = int(input("please enter a valid number"))
        input2 = input("enter the direction you want to rotate the quarter in: (L/R)")
        while input2 != "L" and input2 != "R":
            input2 = input("enter the direction you want to rotate the quarter in: (L/R)")
        self.rotate_board(input1, input2)
        self.print_board()

    def rotate_board(self, quarter, direction):
        self.board = np.reshape(self.board, (6, 6))
        if quarter == 1:
            x = self.board[0:3, 0:3]
            if direction == "L":
                x = np.rot90(x, k=1, axes=(0, 1))
            else:
                x = np.rot90(x, k=3, axes=(0, 1))
            self.board[0:3, 0:3] = x
        elif quarter == 2:
            x = self.board[3:6, 0:3]
            if direction == "L":
                x = np.rot90(x, k=1, axes=(0, 1))
            else:
                x = np.rot90(x, k=3, axes=(0, 1))
            self.board[3:6, 0:3] = x
        elif quarter == 3:
            x = self.board[0:3, 3:6]
            if direction == "L":
                x = np.rot90(x, k=1, axes=(0, 1))
            else:
                x = np.rot90(x, k=3, axes=(0, 1))
            self.board[0:3, 3:6] = x
        else:
            x = self.board[3:6, 3:6]
            if direction == "L":
                x = np.rot90(x, k=1, axes=(0, 1))
            else:
                x = np.rot90(x, k=3, axes=(0, 1))
            self.board[3:6, 3:6] = x

    def print_board(self):
        print("the board: ")
        for i in range(36):
            if self.board[i] == 2:
                print("|X|", end="")
            elif self.board[i] == 0:
                print("|O|", end="")
            else:
                print("|" + str(i) + "|", end="")
            if i % 6 == 5:
                print("")


def main():
    game = Game
    game.print_board()
    game.player_turn()


if __name__ == '__main__':
    main()
