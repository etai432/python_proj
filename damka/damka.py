import random
import time
import csv

class Damka:
    def __init__(self):
        self.board = []
        self.moves = []
        self.kills = []
        self.players2 = []
        self.players0 = []
        self.turn = []
        self.dict = {}
    
    def restart_board(self):
        self.board = [3, 0, 3, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 3, 3, 0, 3, 0, 3, 0, 3, 0, 1, 3, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 3, 1, 3, 1, 2, 3, 2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 2, 3]

    def random_turn(self, player):
        counter = 0
        players = self.count_troops(self.board)
        if player == 0:
            self.players(player, self.board)
            self.turn = []
            while(len(self.turn) == 0):
                place = random.choice(self.players0)
                self.gen_all_moves(place, self.board)
                counter += 1
                if counter > players[0]:
                    for i in range(64):
                        if self.board[i] == 0:
                            self.gen_all_moves(i, self.board)
                            if len(self.turn) > 0:
                                return(place, random.choice(self.turn))
                    return (-1, -1)
            return (place, random.choice(self.turn))
        if player == 2:
            self.players(player, self.board)
            self.turn = []
            while(len(self.turn) == 0):
                place = random.choice(self.players2)
                self.gen_all_moves(place, self.board)
                counter += 1
                if counter > players[1]:
                    for i in range(64):
                        if self.board[i] == 2:
                            self.gen_all_moves(i, self.board)
                            if len(self.turn) > 0:
                                return(place, random.choice(self.turn))
                    return (-1, -1)
            return (place, random.choice(self.turn))

    def check_win(self, board):
        for i in range(8):
            if board[i] == 2:
                return 2
            if board[63-i] == 0:
                return 0
        return 1
    
    def is_tie(self, turn, board):
        self.players(turn, board)
        if turn == 2:
            for i in self.players2:
                self.gen_all_moves(i, board)
                if len(self.turn) != 0:
                    return False
            return True
        if turn == 0:
            for i in self.players0:
                self.gen_all_moves(i, board)
                if len(self.turn) != 0:
                    return False
            return True
    
    def count_troops(self, board):
        troop0 = 0
        troop2 = 0
        for i in board:
            if i == 0:
                troop0 += 1
            if i == 2:
                troop2 += 1
        return (troop0, troop2)

    def players(self, turn, board):
        if turn == 0:
            for i in range(64):
                if board[i] == 0:
                    self.players0.append(i)
        if turn == 2:
            for i in range(64):
                if board[i] == 2:
                    self.players2.append(i)
            
    def gen_moves(self, place, board):
        self.moves = []
        if board[place] == 0:
            if place < 57 and place % 8 != 0 and board[place + 7] == 1:
                self.moves.append(place + 7)
            if place < 55 and place % 8 != 7 and board[place + 9] == 1:
                self.moves.append(place + 9)
        if board[place] == 2:
            if place > 8 and place % 8 != 0 and board[place - 9] == 1:
                self.moves.append(place - 9)
            if place > 6 and place % 8 != 7 and board[place - 7] == 1:
                self.moves.append(place - 7)

    def gen_kill(self, place, board):
        self.kills = []
        if board[place] == 0:
            if place < 50 and place % 8 != 0 and place % 8 != 1 and board[place + 7] == 2 and board[place + 14] == 1:
                self.kills.append(place + 14)
            if place < 46 and place % 8 != 7 and place % 8 != 6 and board[place + 9] == 2 and board[place + 18] == 1:
                self.kills.append(place + 18)
        if board[place] == 2:
            if place > 17 and place % 8 != 0 and place % 8 != 1 and board[place - 9] == 0 and board[place - 18] == 1:
                self.kills.append(place - 18)
            if place > 13 and place % 8 != 7 and place % 8 != 6 and board[place - 7] == 0 and board[place - 14] == 1:
                self.kills.append(place - 14)
    
    def gen_more_kills(self, place, kill_list, board):
        doubles = []
        extra = []
        for i in kill_list:
            player = board[place]
            board[i] = player
            board[place] = 1
            board[int((i + place)/2)] = 1
            if player == 0:
                if i < 50 and i % 8 != 0 and i % 8 != 1 and board[i + 7] == 2 and board[i + 14] == 1:
                    doubles.append((i, i + 14))
                    extra = self.gen_more_kills(i, [i + 14], board)
                    for j in extra:
                        doubles.append(j)
                if i < 46 and i % 8 != 7 and i * 8 != 6 and board[i + 9] == 2 and board[i + 18] == 1:
                    doubles.append((i, i + 18))
                    extra = self.gen_more_kills(i, [i + 18], board)
                    for j in extra:
                        doubles.append(j)
                if i > 17 and i % 8 != 0 and i % 8 != 1 and board[i - 9] == 2 and board[i - 18] == 1:
                    doubles.append((i, i - 18))
                    extra = self.gen_more_kills(i, [i - 18], board)
                    for j in extra:
                        doubles.append(j)
                if i > 13 and i % 8 != 7 and i * 8 != 6 and board[i - 7] == 2 and board[i - 14] == 1:
                    doubles.append((i, i - 14))
                    extra = self.gen_more_kills(i, [i - 14], board)
                    for j in extra:
                        doubles.append(j)
            if player == 2:
                if i < 50 and i % 8 != 0 and i % 8 != 1 and board[i + 7] == 0 and board[i + 14] == 1:
                    doubles.append((i, i + 14))
                    extra = self.gen_more_kills(i, [i + 14], board)
                    for j in extra:
                        doubles.append(j)
                if i < 46 and i % 8 != 7 and i * 8 != 6 and board[i + 9] == 0 and board[i + 18] == 1:
                    doubles.append((i, i + 18))
                    extra = self.gen_more_kills(i, [i + 18], board)
                    for j in extra:
                        doubles.append(j)
                if i > 17 and i % 8 != 0 and i % 8 != 1 and board[i - 9] == 0 and board[i - 18] == 1:
                    doubles.append((i, i - 18))
                    extra = self.gen_more_kills(i, [i - 18], board)
                    for j in extra:
                        doubles.append(j)
                if i > 13 and i % 8 != 7 and i * 8 != 6 and board[i - 7] == 0 and board[i - 14] == 1:
                    doubles.append((i, i - 14))
                    extra = self.gen_more_kills(i, [i - 14], board)
                    for j in extra:
                        doubles.append(j)
            board[i] = 1
            board[place] = player
            board[int((i + place)/2)] = abs(2-player)
        return doubles

    def gen_all_moves(self, place, board):
        self.turn = []
        self.gen_moves(place, board)
        for i in self.moves:
            self.turn.append(i)
        self.gen_kill(place, board)
        for i in self.kills:
            self.turn.append(i)
        doubles = self.gen_more_kills(place, self.kills, board)
        for i in doubles:
            self.turn.append(i)
    
    def move(self, place, goal, last, board):
        for i in self.turn:
            if isinstance(i, int):
                if i == goal:
                    player = board[place]
                    if abs(goal - place) > 10:
                        board[place] = 1
                        board[int((goal + place)/2)] = 1
                        board[goal] = player
                    else:
                        board[place] = 1
                        board[goal] = player
            else:
                if last != i[1] and i[1] == goal:
                    self.move(place, i[0], i[0], board)
                    player = board[i[0]]
                    board[i[0]] = 1
                    board[int((i[1] + i[0])/2)] = 1
                    board[i[1]] = player

    def print_board(self):
        print("the board: ")
        for i in range(64):
            if self.board[i] == 2:
                print("|2|", end="")
            elif self.board[i] == 0:
                print("|0|", end="")
            else:
                print("| |", end="")
            if i % 8 == 7:
                print("")
    
    def rate_boards(self, boards, winner):
        boards1 = []
        for i in range(len(boards)):
            tup = self.count_troops(boards[i])
            score = (winner / 2) * (0.92 ** (len(boards) - i - 1)) + (tup[1] - tup[0]) / 10
            str1 = str(boards[i]).replace('3','').replace(',','').replace(' ','')[1:33]
            boards1.append((str1, score))
        return boards1
                 
    def random_play(self):
        self.restart_board()
        turn = 2
        tup = (0, 0)
        counter = 0
        boards = []
        is_tie = False
        while self.check_win(self.board) == 1 and counter < 40:
            counter += 1
            if is_tie:
                boards = self.rate_boards(boards, 1)
                for i in boards:
                    if i[0] in self.dict:
                        self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
                    else:
                        self.dict[i[0]] = (i[1], 1)
                return 1
            if turn == 2:
                tup = self.random_turn(2)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1], -1, self.board)
                turn = 0
            if turn == 0:
                tup = self.random_turn(0)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1], -1, self.board)
                turn = 2
            boards.append(self.board[:])
        boards = self.rate_boards(boards, self.check_win(self.board))
        for i in boards:
            if i[0] in self.dict:
                self.dict[i[0]] = ((self.dict[i[0]][0] * self.dict[i[0]][1] + i[1]) / (self.dict[i[0]][1] + 1), self.dict[i[0]][1] + 1)
            else:
                self.dict[i[0]] = (i[1], 1)
        return self.check_win(self.board)
    
    def run(self):
        wins1 = 0
        wins2 = 0
        ties = 0
        for _ in range(10000000):
            winner = self.random_play()
            if winner == 2:
                wins1 += 1
            elif winner == 0:
                wins2 += 1
            else:
                ties += 1
        print("player 2 won: " + str(wins1 / 1000) + "%")
        print("player 0 won: " + str(wins2 / 1000) + "%")
        print("a tie happened " + str(ties / 1000) + "% of the time")
        with open('damka\damka_dict.csv', 'w') as output_file:
            for key in self.dict:
                output_file.write("%s,%s\n"%(key, self.dict[key][0]))
        output_file.close()
    
    def random_play_without_saving(self):
        self.restart_board()
        turn = 2
        tup = (0, 0)
        counter = 0
        is_tie = False
        found = 0
        not_found = 0
        while self.check_win(self.board) == 1 and counter < 40:
            counter += 1
            if is_tie:
                return (found, not_found)
            if turn == 2:
                tup = self.random_turn(2)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1], -1, self.board)
                turn = 0
            if turn == 0:
                tup = self.random_turn(0)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1], -1, self.board)
                turn = 2
            str1 = str(self.board).replace('3','').replace(',','').replace(' ','')[1:33]
            if counter > 5:
                if str1 in self.dict.keys():
                    found += 1
                else:
                    not_found += 1
        return (found, not_found)

    def find_percentage(self):
        with open('damka\damka_dict_test.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.dict = {rows[0]:rows[1] for rows in reader}
        found = 0
        not_found = 0
        for i in range(100000):
            tup = self.random_play_without_saving()
            found += tup[0]
            not_found += tup[1]
        print("percentage of found boards: ", found / (found + not_found)*100, "%")
        print("found: ", found)
    
    def dfs(self, board, turn):
        if self.is_tie(turn, board):
            str1 = str(board).replace('3','').replace(',','').replace(' ','')[1:33]
            if str1 not in self.dict:
                tup = self.count_troops(board)
                self.dict[str1] = 0.5 + (tup[1] - tup[0]) / 10
            return 0.5 * 0.92
        win = self.check_win(board)
        if win != 1:
            str1 = str(board).replace('3','').replace(',','').replace(' ','')[1:33]
            if str1 not in self.dict:
                tup = self.count_troops(board)
                self.dict[str1] = win / 2 + (tup[1] - tup[0]) / 10
            return win / 2 * 0.92
        total_score = 0
        counter = 0
        if turn == 2:
            self.players(2, board)
            for player in self.players2:
                self.gen_all_moves(player, board)
                for move in self.turn:
                    copy_board = board[:]
                    if isinstance(move, tuple):
                        self.move(player, move[1], -1, copy_board)
                    else:
                        self.move(player, move, -1, copy_board)
                    counter += 1
                    str1 = str(copy_board).replace('3','').replace(',','').replace(' ','')[1:33]
                    if str1 in self.dict:
                        return self.dict[str1] * 0.92
                    else:
                        tup = self.count_troops(copy_board)
                        score = self.dfs(copy_board[:], 0)
                        total_score += score
                        score1 = score + (tup[1] - tup[0]) / 10
                        self.dict[str1] = score1
        if turn == 0:
            self.players(0, board)
            for player in self.players0:
                self.gen_all_moves(player, board)
                for move in self.turn:
                    copy_board = board[:]
                    if isinstance(move, tuple):
                        self.move(player, move[1], -1, copy_board)
                    else:
                        self.move(player, move, -1, copy_board)
                    counter += 1
                    str1 = str(copy_board).replace('3','').replace(',','').replace(' ','')[1:33]
                    if str1 in self.dict:
                        return self.dict[str1] * 0.92
                    else:
                        tup = self.count_troops(copy_board)
                        score = self.dfs(copy_board[:], 2)
                        total_score += score
                        score1 = score + (tup[1] - tup[0]) / 10
                        self.dict[str1] = score1
        return total_score/counter * 0.92         
                    


def main():
    start = time.time()
    damka = Damka()
    damka.restart_board()
    damka.dfs(damka.board, 2)
    with open('damka\damka_dict.csv', 'w') as output_file:
        for key in damka.dict:
            output_file.write("%s,%s\n"%(key, damka.dict[key][0]))
    output_file.close()
    print(time.time() - start)
    

if __name__ == "__main__":
    main()