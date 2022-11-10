import random

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
        self.board = [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1]

    def random_turn(self, player):
        counter = 0
        players = self.count_troops()
        if player == 0:
            self.players(player)
            self.turn = []
            while(len(self.turn) == 0):
                place = random.choice(self.players0)
                self.gen_all_moves(place)
                counter += 1
                if counter > players[0]:
                    for i in range(64):
                        if self.board[i] == 0:
                            self.gen_all_moves(i)
                            print(i)
                            if len(self.turn) > 0:
                                return(place, random.choice(self.turn))
                    return (-1, -1)
            return (place, random.choice(self.turn))
        if player == 2:
            self.players(player)
            self.turn = []
            while(len(self.turn) == 0):
                place = random.choice(self.players2)
                self.gen_all_moves(place)
                counter += 1
                if counter > players[1]:
                    for i in range(64):
                        if self.board[i] == 2:
                            self.gen_all_moves(i)
                            print(i)
                            if len(self.turn) > 0:
                                return(place, random.choice(self.turn))
                    return (-1, -1)
            return (place, random.choice(self.turn))

    def check_win(self):
        for i in range(8):
            if self.board[i] == 2:
                return 2
            if self.board[63-i] == 0:
                return 0
        return 1
    
    def count_troops(self):
        troop0 = 0
        troop2 = 0
        for i in self.board:
            if i == 0:
                troop0 += 1
            if i == 2:
                troop2 += 1
        return (troop0, troop2)

    def players(self, turn):
        if turn == 0:
            for i in range(64):
                if self.board[i] == 0:
                    self.players0.append(i)
        if turn == 2:
            for i in range(64):
                if self.board[i] == 2:
                    self.players2.append(i)
            
    def gen_moves(self, place):
        self.moves = []
        if self.board[place] == 0:
            if place % 8 != 0 and self.board[place + 7] == 1:
                self.moves.append(place + 7)
            if place % 8 != 7 and self.board[place + 9] == 1:
                self.moves.append(place + 9)
        if self.board[place] == 2:
            if place % 8 != 0 and self.board[place - 9] == 1:
                self.moves.append(place - 9)
            if place % 8 != 7 and self.board[place - 7] == 1:
                self.moves.append(place - 7)

    def gen_kill(self, place):
        self.kills = []
        if self.board[place] == 0:
            if place < 50 and place % 8 != 0 and place % 8 != 1 and self.board[place + 7] == 2 and self.board[place + 14] == 1:
                self.kills.append(place + 14)
            if place < 46 and place % 8 != 7 and place % 8 != 6 and self.board[place + 9] == 2 and self.board[place + 18] == 1:
                self.kills.append(place + 18)
        if self.board[place] == 2:
            if place > 17 and place % 8 != 0 and place % 8 != 1 and self.board[place - 9] == 0 and self.board[place - 18] == 1:
                self.kills.append(place - 18)
            if place > 13 and place % 8 != 7 and place % 8 != 6 and self.board[place - 7] == 0 and self.board[place - 14] == 1:
                self.kills.append(place - 14)
    
    def gen_more_kills(self, place, kill_list):
        doubles = []
        extra = []
        for i in kill_list:
            player = self.board[place]
            self.board[i] = player
            self.board[place] = 1
            self.board[int((i + place)/2)] = 1
            if player == 0:
                if i < 50 and i % 8 != 0 and i % 8 != 1 and self.board[i + 7] == 2 and self.board[i + 14] == 1:
                    doubles.append((i, i + 14))
                    extra = self.gen_more_kills(i, [i + 14])
                    for j in extra:
                        doubles.append(j)
                if i < 46 and i % 8 != 7 and i * 8 != 6 and self.board[i + 9] == 2 and self.board[i + 18] == 1:
                    doubles.append((i, i + 18))
                    extra = self.gen_more_kills(i, [i + 18])
                    for j in extra:
                        doubles.append(j)
                if i > 17 and i % 8 != 0 and i % 8 != 1 and self.board[i - 9] == 2 and self.board[i - 18] == 1:
                    doubles.append((i, i - 18))
                    extra = self.gen_more_kills(i, [i - 18])
                    for j in extra:
                        doubles.append(j)
                if i > 13 and i % 8 != 7 and i * 8 != 6 and self.board[i - 7] == 2 and self.board[i - 14] == 1:
                    doubles.append((i, i - 14))
                    extra = self.gen_more_kills(i, [i - 14])
                    for j in extra:
                        doubles.append(j)
            if player == 2:
                if i < 50 and i % 8 != 0 and i % 8 != 1 and self.board[i + 7] == 0 and self.board[i + 14] == 1:
                    doubles.append((i, i + 14))
                    extra = self.gen_more_kills(i, [i + 14])
                    for j in extra:
                        doubles.append(j)
                if i < 46 and i % 8 != 7 and i * 8 != 6 and self.board[i + 9] == 0 and self.board[i + 18] == 1:
                    doubles.append((i, i + 18))
                    extra = self.gen_more_kills(i, [i + 18])
                    for j in extra:
                        doubles.append(j)
                if i > 17 and i % 8 != 0 and i % 8 != 1 and self.board[i - 9] == 0 and self.board[i - 18] == 1:
                    doubles.append((i, i - 18))
                    extra = self.gen_more_kills(i, [i - 18])
                    for j in extra:
                        doubles.append(j)
                if i > 13 and i % 8 != 7 and i * 8 != 6 and self.board[i - 7] == 0 and self.board[i - 14] == 1:
                    doubles.append((i, i - 14))
                    extra = self.gen_more_kills(i, [i - 14])
                    for j in extra:
                        doubles.append(j)
            self.board[i] = 1
            self.board[place] = player
            self.board[int((i + place)/2)] = abs(2-player)
        return doubles

    def gen_all_moves(self, place):
        self.turn = []
        self.gen_moves(place)
        for i in self.moves:
            self.turn.append(i)
        self.gen_kill(place)
        for i in self.kills:
            self.turn.append(i)
        doubles = self.gen_more_kills(place, self.kills)
        for i in doubles:
            self.turn.append(i)
    
    def move(self, place, goal):
        for i in self.turn:
            if isinstance(i, int):
                if i == goal:
                    player = self.board[place]
                    if abs(goal - place) > 10:
                        self.board[place] = 1
                        self.board[int((goal + place)/2)] = 1
                        self.board[goal] = player
                    else:
                        self.board[place] = 1
                        self.board[goal] = player
            else:
                if i[1] == goal:
                    self.move(place, i[0])
                    player = self.board[i[0]]
                    self.board[i[0]] = 1
                    self.board[int((i[1] + i[0])/2)] = 1
                    self.board[i[1]] = player

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
    
    def random_play(self):
        self.restart_board()
        turn = 2
        tup = (0, 0)
        counter = 0
        is_tie = False
        while self.check_win() == 1 and counter < 40:
            counter += 1
            if is_tie:
                return 1
            if turn == 2:
                tup = self.random_turn(2)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1])
                turn = 0
            if turn == 0:
                tup = self.random_turn(0)
                if tup == (-1, -1):
                    is_tie = True
                self.move(tup[0], tup[1])
                turn = 2
        return self.check_win()

damka = Damka()
damka.random_play()
# damka.restart_board()
# damka.board[30] = 2
# damka.board[28] = 2
# damka.board[51] = 1
# damka.print_board()
# damka.gen_all_moves(19)
# print(damka.turn)
# damka.move(19, 33)
# damka.print_board()
# tup = damka.random_turn(2)
# print(tup)
# damka.move(tup[0], tup[1])
# damka.print_board()
