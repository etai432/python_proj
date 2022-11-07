class Damka:
    def __init__(self):
        self.board = []
        self.moves = []
        self.kills = []
        self.dict = {}
    
    def restart_board1(self):
        self.board = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def check_win(self):
        for i in range(8):
            if self.board[i] == 2:
                return 2
            if self.board[63-i] == 0:
                return 0
        return 1

    def gen_moves(player, place):
        self.moves = []
        if player == 0:
            if place % 8 != 0 and self.board[place + 7] == 1:
                self.moves.append(place+7)
            if place % 8 != 7 and self.boards[place + 9] == 1:
                self.moves.append(place+9)
        if player == 2:
            if place % 8 != 0 and self.board[place - 7] == 1:
                self.moves.append(place+7)
            if place % 8 != 7 and self.boards[place - 9] == 1:
                self.moves.append(place+9)
        
    
    
