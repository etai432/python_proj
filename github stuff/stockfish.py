from stockfish import Stockfish
import time

def init_stockfish(windows=True):
    if windows:
        return Stockfish(path="C:/Users/User/Downloads/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
    else:
        return Stockfish(path="/home/itay/Downloads/stockfish_15.1_linux_x64_bmi2/stockfish_15.1_x64_bmi2")

def get_eval(stockfish, fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_evaluation()

start = time.time()
stockfish = init_stockfish()
print(get_eval(stockfish, "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1."))
print(stockfish.get_board_visual())
print(time.time() - start)
