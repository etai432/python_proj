import random
import time
import numpy as np


class TicTacToe:

    def __init__(self):
        self.board = np.ones(9)
        self.empty = []
        self.dict = {}
        self.all_boards = []

    def restart_board(self):
        self.board = np.ones(9)

    def check_win(self, last_index, turn):
        if self.board[last_index % 3] == self.board[last_index % 3 + 3] == self.board[last_index % 3 + 6] != 1:
            return turn
        if self.board[last_index // 3 * 3] == self.board[last_index // 3 * 3 + 1] == self.board[last_index // 3 * 3 + 2] != 1:
            return turn
        if (self.board[0] == self.board[4] == self.board[8] or self.board[2] == self.board[4] == self.board[6]) and self.board[4] != 1:
            return turn

    def empty_space(self):
        self.empty = list(np.where(self.board == 1)[0])

    def computer_turn(self):
        self.empty_space()
        return random.choice(self.empty) + 1

    def computer2_turn(self):
        self.empty_space()
        return random.choice(self.empty) + 1

    def player_turn(self):
        self.empty_space()
        list1 = self.empty
        print(list1)
        input1 = int(input("please pick a spot from the list of empty spaces: "))
        while list1.count(input1) == 0:
            input1 = int(input("please pick a spot from the list of empty spaces: "))
        return input1

    def print_board(self):
        print("the board: ")
        for i in range(9):
            print(self.board[i], end="  ")
            if i % 3 == 2:
                print("")

    def rate_boards(self, game_boards, winner, gamma=0.9):
        list1 = []
        for i in range(len(game_boards)):
            list1.append((str(game_boards[i]), (winner / 2) * (gamma ** (len(game_boards) - i - 1))))
        return list1

    def play_one_game(self):  # pc = x, player = o
        self.restart_board()
        turns = 0
        while True:
            turn = 2
            last_index = int(self.computer_turn()-1)
            self.board[last_index] = 2
            turns += 1
            self.print_board()
            if self.check_win(last_index, turn) == 2:
                print("computer won!")
                return 2
            if turns == 9:
                print("its a tie!")
                return 1
            turn = 1
            last_index = int(self.player_turn())
            self.board[last_index] = 0
            turns += 1
            self.print_board()
            if self.check_win(last_index, turn) == 1:
                print("player won!")
                return 0

    def play_one_game_computer(self):
        self.restart_board()
        game_boards = []
        turns = 0
        for j in range(9):
            turn = 2
            last_index = int(self.computer_turn() - 1)
            self.board[last_index] = 2
            turns += 1
            game_boards.append(list(np.copy(self.board)))
            if turns > 4:
                if self.check_win(last_index, turn) == 2:
                    game_boards = self.rate_boards(game_boards, 2)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = (self.dict[i[0]][0] + 1, i[1])
                        else:
                            self.dict[i[0]] = (1, i[1])
                    return 2
            if turns == 9:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = (self.dict[i[0]][0] + 1, i[1])
                    else:
                        self.dict[i[0]] = (1, i[1])
                return 1
            turn = 1
            last_index = int(self.computer2_turn() - 1)
            self.board[last_index] = 0
            turns += 1
            game_boards.append(list(np.copy(self.board)))
            if turns > 4:
                if self.check_win(last_index, turn) == 1:
                    game_boards = self.rate_boards(game_boards, 0)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = (self.dict[i[0]][0] + 1, i[1])
                        else:
                            self.dict[i[0]] = (1, i[1])
                    return 0

    def run_games(self):
        games = 0
        wins1 = 0
        wins2 = 0
        ties = 0
        for i in range(100000):
            winner = self.play_one_game_computer()
            if winner == 2:
                wins1 += 1
            elif winner == 0:
                wins2 += 1
            else:
                ties += 1
            games += 1
        print("player x won: " + str(wins1 / 1000) + "%")
        print("player o won: " + str(wins2 / 1000) + "%")
        print("a tie happened " + str(ties / 1000) + "% of the time")
        print(self.dict)


def main():
    start = time.time()
    game = TicTacToe()
    game.run_games()
    print(time.time() - start)


if __name__ == "__main__":
    main()
