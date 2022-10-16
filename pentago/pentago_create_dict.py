import csv
import numpy as np
import random


class Game:

    def __init__(self):
        self.board = np.full(36, 1)
        self.empty = []
        self.dict = {}
        self.gamma = 0.9
        self.index = -1
        self.quarter = 0
        self.direction = "I"

    def restart_board(self):
        self.board = np.full(36, 1)

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
        return 1

    def empty_space(self):
        self.empty = []
        for i in range(36):
            if self.board[i] == 1:
                self.empty.append(i)

    def computer_turn(self):
        self.empty_space()
        choice = random.choice(self.empty)
        self.board[choice] = 4
        quarter = random.randint(1, 4)
        direction = random.randint(1, 2)
        last_index = self.rotate_board(quarter, direction, self.board)
        return last_index

    def computer_turn2(self):
        self.empty_space()
        choice = random.choice(self.empty)
        self.board[choice] = 3
        quarter = random.randint(1, 4)
        direction = random.randint(1, 2)
        last_index = self.rotate_board(quarter, direction, self.board)
        return last_index

    def player_turn(self):
        self.print_board()
        self.empty_space()
        input1 = int(input("please pick a spot from the empty spaces: "))
        while input1 not in self.empty:
            input1 = int(input("please pick a spot from the empty spaces: "))
        self.board[input1] = 3
        self.print_board()
        print("insert the quarter you want to rotate:")
        print("1 | 2")
        input1 = int(input("3 | 4 "))
        while input1 < 1 or input1 > 4:
            input1 = int(input("please enter a valid number"))
        input2 = input("enter the direction you want to rotate the quarter in: (L/R) ")
        while input2 != "L" and input2 != "R":
            input2 = input("enter the direction you want to rotate the quarter in: (L/R) ")
        last_index = self.rotate_board(input1, input2, self.board)
        self.print_board()
        return last_index

    def rotate_board(self, quarter, direction, board):
        board = np.reshape(board, (6, 6))
        if quarter == 1:
            x = board[0:3, 0:3]
            if direction == "L":
                board[0:3, 0:3] = np.rot90(x, k=1, axes=(0, 1))
            else:
                board[0:3, 0:3] = np.rot90(x, k=3, axes=(0, 1))
            board = np.reshape(board, 36)
        elif quarter == 2:
            x = board[0:3, 3:6]
            if direction == "L":
                board[0:3, 3:6] = np.rot90(x, k=1, axes=(0, 1))
            else:
                board[0:3, 3:6] = np.rot90(x, k=3, axes=(0, 1))
            board = np.reshape(board, 36)
        elif quarter == 3:
            x = board[3:6, 0:3]
            if direction == "L":
                board[3:6, 0:3] = np.rot90(x, k=1, axes=(0, 1))
            else:
                board[3:6, 0:3] = np.rot90(x, k=3, axes=(0, 1))
            board = np.reshape(board, 36)
        else:
            x = board[3:6, 3:6]
            if direction == "L":
                board[3:6, 3:6] = np.rot90(x, k=1, axes=(0, 1))
            else:
                board[3:6, 3:6] = np.rot90(x, k=3, axes=(0, 1))
            board = np.reshape(board, 36)
        if 3 in board:
            index1 = np.where(board == 3)[0][0]
            board[index1] = 0
        else:
            index1 = np.where(board == 4)[0][0]
            board[index1] = 2
        return index1

    def print_board(self):
        print("the board: ")
        for i in range(36):
            if self.board[i] == 2:
                print("|X", end="")
            elif self.board[i] == 0:
                print("|O", end="")
            else:
                print("|" + str(i), end="")
            if i < 10 or self.board[i] == 2 or self.board[i] == 0:
                print(" |", end="")
            else:
                print("|", end="")
            if i % 6 == 5:
                print("")

    def rate_boards(self, game_boards, winner):
        list1 = []
        for i in range(len(game_boards)):
            list1.append((str(list(game_boards[i])), (winner / 2) * (self.gamma ** (len(game_boards) - i - 1))))
        return list1

    def play_one_game(self):
        self.restart_board()
        turns = 0
        while True:
            turns += 1
            turn = 2
            last_index = self.computer_turn()
            self.print_board()
            if turns > 9 and self.check_win(last_index, turn) == 2:
                print("computer won")
                return 2
            turn = 0
            turns += 1
            last_index = self.player_turn()
            if turns > 9 and self.check_win(last_index, turn) == 0:
                print("player won")
                return 0
            if turns == 36:
                print("tie")
                return 1

    def play_one_game_computer(self):
        game_boards = []
        self.restart_board()
        turns = 0
        while True:
            turns += 1
            turn = 2
            last_index = self.computer_turn()
            game_boards.append(np.copy(self.board))
            if turns > 9 and self.check_win(last_index, turn) == 2:
                game_boards = self.rate_boards(game_boards, 2)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 2
            turn = 0
            turns += 1
            last_index = self.computer_turn2()
            game_boards.append(np.copy(self.board))
            if turns > 9 and self.check_win(last_index, turn) == 0:
                game_boards = self.rate_boards(game_boards, 0)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 0
            if turns == 36:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1

    def choose_next_turn(self, player):
        self.empty_space()
        max1 = -1
        self.index = -1
        best_board = np.empty(1)
        for i in self.empty:
            for j in range(4):
                for g in range(2):
                    copy_board = self.board.copy()
                    copy_board[i] = player + 2
                    quarter = j + 1
                    if g == 0:
                        direction = "L"
                    else:
                        direction = "R"
                    self.rotate_board(quarter, direction, copy_board)
                    copy_board = str(copy_board)
                    if copy_board in self.dict:
                        if max1 < self.dict[copy_board][0]:
                            max1 = self.dict[copy_board][0]
                            best_board = np.copy(list(copy_board))
                            self.index = i
                            self.quarter = quarter
                            self.direction = direction
        if self.index == -1:
            self.index = self.computer_turn()
            return 0
        return best_board

    def play_one_game_ai(self):
        self.restart_board()
        turns = 0
        while True:
            turns += 1
            turn = 2
            next1 = self.choose_next_turn(2)
            if type(next1) != int:
                self.empty_space()
                self.board[self.index] = 4
                last_index = self.rotate_board(self.quarter, self.direction, self.board)
            else:
                last_index = self.index
            if turns > 9 and self.check_win(last_index, turn) == 2:
                return 2
            turn = 0
            turns += 1
            last_index = self.computer_turn2()
            if turns > 9 and self.check_win(last_index, turn) == 0:
                return 0
            if turns == 36:
                return 1

    def run_games(self):
        wins1 = 0
        wins2 = 0
        ties = 0
        for _ in range(200):
            for i in range(10000):
                winner = self.play_one_game_computer()
                if winner == 2:
                    wins1 += 1
                elif winner == 0:
                    wins2 += 1
                else:
                    ties += 1
            print(_)
        print("player x won: " + str(wins1 / 1000) + "%")
        print("player o won: " + str(wins2 / 1000) + "%")
        print("a tie happened " + str(ties / 1000) + "% of the time")

    def run_games_ai(self):
        wins1 = 0
        wins2 = 0
        ties = 0
        for i in range(2000000):
            winner = self.play_one_game_ai()
            if winner == 2:
                wins1 += 1
            elif winner == 0:
                wins2 += 1
            else:
                ties += 1
        print("player x won: " + str(wins1 / 1) + "%")
        print("player o won: " + str(wins2 / 1) + "%")
        print("a tie happened " + str(ties / 1) + "% of the time")


def main():
    game = Game()
    # game.run_games_ai()
    game.run_games()
    with open('pentago_dict2.csv', 'w') as output_file:
        for key in game.dict:
            output_file.write("%s,%s\n" % (key, game.dict[key]))
    output_file.close()


if __name__ == '__main__':
    main()