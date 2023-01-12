from stockfish import Stockfish

class CPU:
    def __init__(self):
        self.stockfish = Stockfish(path="/usr/games/stockfish")
    
    def computer_move(self, history):
        """
        Parameters:
            - player_move: in the form ((from coordinate), (to coordinate))
        Purpose:
            - Generate a best move for the CPU to play using a history of user and CPU moves
        """
        self.stockfish.make_moves_from_current_position(history)
        return self.stockfish.get_best_move()