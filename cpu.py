from stockfish import Stockfish

class CPU:
    def __init__(self):
        self.prev_moves = []
        self.stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
    
    def computer_move(self, player_move):
        """
        Parameters:
            - player_move: in the form ((from coordinate), (to coordinate))
        Purpose:
            - Generate a best move for the CPU to play using a history of user and CPU moves
        """
        self.prev_moves.append(player_move)
        self.stockfish.make_moves_from_current_position(self.prev_moves[-2:] if len(self.prev_moves) > 1 else [self.prev_moves[-1]])
        self.prev_moves.append(self.stockfish.get_best_move())
        return self.prev_moves[-1]