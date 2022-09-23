import random
import time


class TicTacToe:

    def __init__(self):
        self.board = []
        self.empty = []
        self.dict = {}
        self.gamma = 0.9
        self.alfa = 20

    def restart_board(self):
        self.board = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def check_win(self, last_index, turn):
        if self.board[last_index % 3] == self.board[last_index % 3 + 3] == self.board[last_index % 3 + 6] != 1:
            return turn
        if self.board[last_index // 3 * 3] == self.board[last_index // 3 * 3 + 1] == self.board[last_index // 3 * 3 + 2] != 1:
            return turn
        if (self.board[0] == self.board[4] == self.board[8] or self.board[2] == self.board[4] == self.board[6]) and self.board[4] != 1:
            return turn

    def empty_space(self):
        self.empty = []
        for i in range(9):
            if self.board[i] == 1:
                self.empty.append(i + 1)

    def computer_turn(self):
        self.empty_space()
        return random.choice(self.empty)

    def computer2_turn(self):
        self.empty_space()
        return random.choice(self.empty)

    def player_turn(self):
        self.empty_space()
        print(self.empty)
        input1 = int(input("please pick a spot from the list of empty spaces: "))
        while input1 not in self.empty:
            input1 = int(input("please pick a spot from the list of empty spaces: "))
        return input1

    def print_board(self):
        print("the board: ")
        for i in range(9):
            print(self.board[i], end="  ")
            if i % 3 == 2:
                print("")

    def rate_boards(self, game_boards, winner):
        list1 = []
        for i in range(len(game_boards)):
            list1.append((str(game_boards[i]), (winner / 2) * (self.gamma ** (len(game_boards) - i - 1))))
        return list1

    def play_one_game(self):  # pc = x, player = o
        temp_alfa = self.alfa
        self.alfa = 0
        self.restart_board()
        turns = 0
        while True:
            turn = 2
            last_index = int(self.choose_next_turn(2) - 1)
            self.board[last_index] = 2
            turns += 1
            self.print_board()
            if self.check_win(last_index, turn) == 2:
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
            if self.check_win(last_index, turn) == 1:
                print("player won!")
                self.alfa = temp_alfa
                return 0

    def play_one_game_computer(self):
        self.restart_board()
        game_boards = []
        turns = 0
        for j in range(9):
            turn = 2
            last_index = self.computer_turn() - 1
            self.board[last_index] = 2
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4:
                if self.check_win(last_index, turn) == 2:
                    game_boards = self.rate_boards(game_boards, 2)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                        else:
                            self.dict[i[0]] = (i[1], 1)
                    return 2
            if turns == 9:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1
            turn = 1
            last_index = self.computer2_turn() - 1
            self.board[last_index] = 0
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4:
                if self.check_win(last_index, turn) == 1:
                    game_boards = self.rate_boards(game_boards, 0)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                        else:
                            self.dict[i[0]] = (i[1], 1)
                    return 0

    def choose_next_turn(self, player):
        if random.randint(1, 100) <= self.alfa:
            return self.computer_turn()
        self.empty_space()
        max1 = -1
        min1 = 2
        index = -1
        for i in self.empty:
            copy_board = self.board[:]
            copy_board[i - 1] = player
            copy_board = str(copy_board)
            if copy_board in self.dict:
                if player == 2:
                    if max1 < self.dict[copy_board][0]:
                        max1 = self.dict[copy_board][0]
                        index = i
                else:
                    if min1 > self.dict[copy_board][0]:
                        min1 = self.dict[copy_board][0]
                        index = i
        if index == -1:
            index = self.computer_turn()
        return index

    def play_one_game_ai(self):
        self.restart_board()
        game_boards = []
        turns = 0
        for j in range(9):
            turn = 2
            if turns == 0:
                last_index = self.computer_turn() - 1
            else:
                last_index = self.choose_next_turn(2) - 1
            self.board[last_index] = 2
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4:
                if self.check_win(last_index, turn) == 2:
                    game_boards = self.rate_boards(game_boards, 2)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                        else:
                            self.dict[i[0]] = (i[1], 1)
                    return 2
            if turns == 9:
                game_boards = self.rate_boards(game_boards, 1)
                for i in game_boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1
            turn = 1
            last_index = self.choose_next_turn(0) - 1
            self.board[last_index] = 0
            turns += 1
            game_boards.append(self.board[:])
            if turns > 4:
                if self.check_win(last_index, turn) == 1:
                    game_boards = self.rate_boards(game_boards, 0)
                    for i in game_boards:
                        if i[0] in self.dict:
                            self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                        else:
                            self.dict[i[0]] = (i[1], 1)
                    return 0

    def run_games(self):
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
        print("1st generation (random)")
        print("player x won: " + str(wins1 / 1000) + "%")
        print("player o won: " + str(wins2 / 1000) + "%")
        print("a tie happened " + str(ties / 1000) + "% of the time")
        j = 0
        self.alfa = 0
        while ties != 100000:
            # self.alfa -= 2
            wins1 = 0
            wins2 = 0
            ties = 0
            j += 1
            for i in range(100000):
                winner = self.play_one_game_ai()
                if winner == 2:
                    wins1 += 1
                elif winner == 0:
                    wins2 += 1
                else:
                    ties += 1
            print("generation: " + str(j+1) + " random: " + str(self.alfa) + "%")
            print("player x won: " + str(wins1 / 1000) + "%")
            print("player o won: " + str(wins2 / 1000) + "%")
            print("a tie happened " + str(ties / 1000) + "% of the time")


def main():
    start = time.time()
    game = TicTacToe()
    game.run_games()
    print(time.time()-start)
    game.play_one_game()
    game.play_one_game()
    game.play_one_game()


if __name__ == "__main__":
    main()
