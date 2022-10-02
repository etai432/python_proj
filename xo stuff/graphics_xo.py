from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import xo


class Model:
    def __init__(self):
        pass


class Board(GridLayout):

    def __init__(self):
        GridLayout.__init__(self)
        self.cols = 3
        self.addCellsToBoatd()
        self.myModel = Model()

    def addCellsToBoatd(self):
        for line in range(3):
            for col in range(3):
                temp_cell = Cell(self, line, col)
                self.add_widget(temp_cell)

    def react(self, chooseButton):
        print(chooseButton.col)


class Cell(Button):
    def __init__(self, graphBoard, line, col):
        Button.__init__(self)
        self.line = line
        self.col = col
        self.font_size = 80
        self.color = "red"
        self.text = "?"
        self.gb = graphBoard

    def on_press(self):
        self.text = "x"
        self.gb.react(self)


class MyPaintApp(App):

    def build(self):
        return Board()


def main():
    print("hi")


if __name__ == "__main__":
    main()
