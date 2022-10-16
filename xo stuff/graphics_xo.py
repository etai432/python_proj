import random
import kivy.uix.label
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import xo
import time


class Model:
    def __init__(self):
        pass


class Cell(Button):
    def __init__(self, graphBoard, line, col):
        Button.__init__(self)
        self.line = line
        self.col = col
        self.font_size = 80
        self.font_size = 150
        self.text = " "
        self.gb = graphBoard

    def on_press(self):
        self.text = "o"
        self.disabled = True
        self.gb.react(self)


class Board(GridLayout):

    def __init__(self):
        self.buttons_arr = []
        self.game_board = xo.reset_board()
        self.dict = xo.load_dict()
        self.turns = 0
        GridLayout.__init__(self)
        self.cols = 3
        self.addCellsToBoatd()
        self.myModel = Model()


    def addCellsToBoatd(self):
        for line in range(3):
            for col in range(3):
                self.buttons_arr.append(Cell(self, line, col))
                self.add_widget(self.buttons_arr[line * 3 + col])
        computer_turn = random.randint(0, 8)
        self.game_board[computer_turn] = 2
        self.buttons_arr[computer_turn].text = "x"
        self.buttons_arr[computer_turn].disabled = True

    def win(self, winner):
        for i in self.buttons_arr:
            self.remove_widget(i)
        if winner == "tie":
            my_label = kivy.uix.label.Label(text="its a tie!", font_size='120sp', color="green")
        else:
            my_label = kivy.uix.label.Label(text="the winner is the " + winner + "!", font_size='60sp', color="green")
        self.add_widget(my_label)

    def react(self, choosenButton):
        self.game_board[choosenButton.line * 3 + choosenButton.col] = 0
        self.turns += 1
        if xo.check_win(self.game_board, choosenButton.line * 3 + choosenButton.col, 0) == 0:
            self.win("player")
        else:
            computer_turn = xo.choose_next_move(self.game_board, self.dict)
            self.game_board[computer_turn] = 2
            self.buttons_arr[computer_turn].text = "x"
            self.buttons_arr[computer_turn].disabled = True
            self.turns += 1
            if xo.check_win(self.game_board, computer_turn, 2) == 2:
                self.win("computer")
            if xo.is_empty(self.game_board):
                self.win("tie")


class MyPaintApp(App):
    def build(self):
        return Board()


MyPaintApp().run()
