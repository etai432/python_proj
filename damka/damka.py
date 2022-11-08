class Damka:
    def __init__(self):
        self.board = []
        self.moves = []
        self.kills = []
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

    def gen_moves(self, player, place):
        self.moves = []
        if player == 0:
            if place % 8 != 0 and self.board[place + 7] == 1:
                self.moves.append(place+7)
            if place % 8 != 7 and self.board[place + 9] == 1:
                self.moves.append(place+9)
        if player == 2:
            if place % 8 != 0 and self.board[place - 7] == 1:
                self.moves.append(place+7)
            if place % 8 != 7 and self.board[place - 9] == 1:
                self.moves.append(place+9)
    
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
damka.print_board()
