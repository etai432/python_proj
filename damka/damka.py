class Damka:
    def __init__(self):
        self.board = []
        self.moves = []
        self.kills = []
        self.turn = []
        self.dict = {}
    
    def restart_board(self):
        self.board = [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1]

    def check_win(self):
        for i in range(8):
            if self.board[i] == 2:
                return 2
            if self.board[63-i] == 0:
                return 0
        return 1

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
            if place % 8 != 0 and place % 8 != 1 and self.board[place + 7] == 2 and self.board[place + 14] == 1:
                self.kills.append(place + 14)
            if place % 8 != 7 and place * 8 != 6 and self.board[place + 9] == 2 and self.board[place + 18] == 1:
                self.kills.append(place + 18)
        if self.board[place] == 2:
            if place % 8 != 0 and place % 8 != 1 and self.board[place - 9] == 0 and self.board[place - 18] == 1:
                self.kills.append(place - 18)
            if place % 8 != 7 and place % 8 != 6 and self.board[place - 7] == 0 and self.board[place - 14] == 1:
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


damka = Damka()
damka.restart_board()
damka.board[30] = 2
damka.board[28] = 2
damka.board[51] = 1
damka.print_board()
damka.gen_all_moves(19)
print(damka.turn)