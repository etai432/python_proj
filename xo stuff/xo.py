import csv
import random
import time
import pandas as pd
import numpy as np


class TicTacToe:

    def __init__(self):
        self.board = []
        self.empty = []
        # self.dict = {row[0]: row[1]
        #              for _, row in pd.read_csv(r"xo stuff/xo_dict.csv").iterrows()}
        self.dict = {}
        self.gamma = 0.9
        self.alfa = 20

    def restart_board(self):
        self.board = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def check_win(self, board, last_index, turn):
        if board[last_index % 3] == board[last_index % 3 + 3] == board[last_index % 3 + 6] != 1:
            return turn
        if board[last_index // 3 * 3] == board[last_index // 3 * 3 + 1] == board[last_index // 3 * 3 + 2] != 1:
            return turn
        if (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]) and board[4] != 1:
            return turn
        return 1

    def empty_space(self, board):
        self.empty = []
        for i in range(9):
            if board[i] == 1:
                self.empty.append(i + 1)

    def computer_turn(self):
        self.empty_space(self.board)
        return random.choice(self.empty)

    def player_turn(self):
        self.empty_space(self.board)
        input1 = int(input("please pick a spot from the empty spaces: "))
        while input1 not in self.empty:
            input1 = int(input("please pick a spot from the empty spaces: "))
        return input1

    def print_board(self):
        print("the board: ")
        for i in range(9):
            if self.board[i] == 2:
                print("|X|", end="")
            elif self.board[i] == 0:
                print("|O|", end="")
            else:
                print("| |", end="")
            if i % 3 == 2:
                print("")

    def rate_boards(self, game_boards, winner):
        list1 = []
        for i in range(len(game_boards)):
            list1.append(((str(game_boards[i]).replace(',', '').replace(' ', '')[1:10]), (winner / 2) * (self.gamma ** (len(game_boards) - i - 1))))
        return list1

    def play_one_game(self):  # pc = x, player = o
        temp_alfa = self.alfa
        self.alfa = 0
        self.restart_board()
        turns = 0
        while True:
            turn = 2
            if turns == 0:
                last_index = random.randint(1, 9) - 1
            else:
                last_index = self.choose_next_turn(2) - 1
            self.board[last_index] = 2
            turns += 1
            self.print_board()
            if self.check_win(self.board, last_index, turn) == 2:
                print("computer won!")
                self.alfa = temp_alfa
                return 2
            if turns == 9:
                print("its a tie!")
                self.alfa = temp_alfa
                return 1
            turn = 1
            last_index = int(self.player_turn() - 1)
            self.board[last_index] = 0
            turns += 1
            self.print_board()
            if self.check_win(self.board, last_index, turn) == 1:
                print("player won!")
                self.alfa = temp_alfa
                return 0

    def play_one_game_computer(self):
        self.restart_board()
        game_boards = []
        turns = 0
        for _ in range(9):
            turn = 2
            last_index = self.computer_turn() - 1
            self.board[last_index] = 2
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4 and self.check_win(self.board, last_index, turn) == 2:
                game_boards = self.rate_boards(game_boards, 2)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 2
            if turns == 9:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1
            turn = 1
            last_index = self.computer_turn() - 1
            self.board[last_index] = 0
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4 and self.check_win(self.board, last_index, turn) == 1:
                game_boards = self.rate_boards(game_boards, 0)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 0

    def choose_next_turn(self, player):
        if random.randint(1, 100) <= self.alfa:
            return self.computer_turn()
        self.empty_space(self.board)
        max1 = -1
        min1 = 2
        index = -1
        for i in self.empty:
            copy_board = self.board[:]
            copy_board[i - 1] = player
            copy_board = str(copy_board).replace(',', '').replace(' ', '')[1:10]
            if copy_board in self.dict:
                if player == 2:
                    if max1 < self.dict[copy_board]:
                        max1 = self.dict[copy_board]
                        index = i
                else:
                    if min1 > self.dict[copy_board]:
                        min1 = self.dict[copy_board]
                        index = i
        if index == -1:
            index = self.computer_turn()
        return index

    def play_one_game_ai(self):
        self.restart_board()
        game_boards = []
        turns = 0
        for _ in range(9):
            turn = 2
            if turns == 0:
                last_index = random.randint(1, 9) - 1
            else:
                last_index = self.choose_next_turn(2) - 1
            self.board[last_index] = 2
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4 and self.check_win(self.board, last_index, turn) == 2:
                game_boards = self.rate_boards(game_boards, 2)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 2
            if turns == 9:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1
            turn = 1
            last_index = self.choose_next_turn(0) - 1
            self.board[last_index] = 0
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4 and self.check_win(self.board, last_index, turn) == 1:
                game_boards = self.rate_boards(game_boards, 0)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (
                            self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 0

    def run_games(self):
        wins1 = 0
        wins2 = 0
        ties = 0
        for _ in range(100000):
            winner = self.play_one_game_computer()
            if winner == 2:
                wins1 += 1
            elif winner == 0:
                wins2 += 1
            else:
                ties += 1
        print("1st generation (random)")
        print("player x won: " + str(wins1 / 1000) + "%")
        print("player o won: " + str(wins2 / 1000) + "%")
        print("a tie happened " + str(ties / 1000) + "% of the time")
        # j = 0
        # while ties != 100000:
        #     self.alfa -= 2
        #     wins1 = 0
        #     wins2 = 0
        #     ties = 0
        #     j += 1
        #     for i in range(100000):
        #         winner = self.play_one_game_ai()
        #         if winner == 2:
        #             wins1 += 1
        #         elif winner == 0:
        #             wins2 += 1
        #         else:
        #             ties += 1
        #     print("generation: " + str(j+1) + " random: " + str(self.alfa) + "%")
        #     print("player x won: " + str(wins1 / 1000) + "%")
        #     print("player o won: " + str(wins2 / 1000) + "%")
        #     print("a tie happened " + str(ties / 1000) + "% of the time")
        with open('xo_dict.csv', 'w') as output_file:
            for key in self.dict:
                output_file.write("%s,%s\n" % (key, self.dict[key][0]))
        output_file.close()
    
    def dfs(self, board, turn, last_index):
        win = abs(self.check_win(board, last_index, turn) - 2)
        if win != 1:
            return win / 2
        self.empty_space(board)
        if len(self.empty) == 0:
            return 0.5
        total_score = 0
        counter = 0
        if turn == 2:
            for i in self.empty:
                copy_board = board[:]
                copy_board[i-1] = 2
                counter += 1
                str1 = str(copy_board).replace(',', '').replace(' ', '')[1:10]
                if str1 in self.dict:
                    total_score += self.dict[str1]
                else:
                    score = self.dfs(copy_board[:], 0, i-1)
                    total_score += score
                    self.dict[str1] = score
        if turn == 0:
            for i in self.empty:
                copy_board = board[:]
                copy_board[i-1] = 0
                counter += 1
                str1 = str(copy_board).replace(',', '').replace(' ', '')[1:10]
                if str1 in self.dict:
                    total_score += self.dict[str1]
                else:
                    score = self.dfs(copy_board[:], 2, i-1)
                    total_score += score
                    self.dict[str1] = score
        return total_score/counter * 0.9


        


def main():
    start = time.time()
    game = TicTacToe()
    game.restart_board()
    game.dfs(game.board, 2, -1)
    with open('xo stuff/xo_dict1.csv', 'w') as output_file:
        for key in game.dict:
            output_file.write("%s,%s\n" % (key, game.dict[key]))
    output_file.close()
    print(time.time() - start)


def load_dict():
    with open('xo stuff/xo_dict1.csv', mode='r') as infile:
        reader = csv.reader(infile)
        dict1 = {rows[0]:rows[1] for rows in reader}
    return dict1


def choose_next_move(board, dict1):
    empty = []
    for i in range(9):
        if board[i] == 1:
            empty.append(i)
    max1 = -1
    index = -1
    for i in empty:
        copy_board = board[:]
        copy_board[i] = 2
        str1 = str(copy_board).replace(',', '').replace(' ', '')[1:10]
        if str1 in dict1:
            if max1 < float(dict1[str1]):
                max1 = float(dict1[str1])
                index = i
    if index == -1:
        index = random.choice(empty)
    return index


def reset_board():
    return [1, 1, 1, 1, 1, 1, 1, 1, 1]


def check_win(board, last_index, turn):
    if board[last_index % 3] == board[last_index % 3 + 3] == board[last_index % 3 + 6] != 1:
        return turn
    if board[last_index // 3 * 3] == board[last_index // 3 * 3 + 1] == board[last_index // 3 * 3 + 2] != 1:
        return turn
    if (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]) and board[4] != 1:
        return turn


def is_empty(board):
    if 1 in board:
        return False
    return True


if __name__ == "__main__":
    main()
