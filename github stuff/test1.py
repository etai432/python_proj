from stockfish import Stockfish
stockfish = Stockfish(path="C:/Users/User/Downloads/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
print(stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"))
print(stockfish.get_best_move())
print(stockfish.get_board_visual())
print(stockfish.get_evaluation())
