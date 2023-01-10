"""
The main intention of this file is to hold all the classes and info for each piece
"""

from fen import parse_fen


START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
square_size = 80

piece_images = {
        'P': 'white_pieces/white_pawn.png',
        'N': 'white_pieces/white_knight.png',
        'B': 'white_pieces/white_bishop.png',
        'R': 'white_pieces/white_rook.png',
        'Q': 'white_pieces/white_queen.png',
        'K': 'white_pieces/white_king.png',
        'p': 'black_pieces/black_pawn.png',
        #'n': 'black_pieces/black_knight.png',
        'n': 'black_pieces/imhashem.jpeg',
        'b': 'black_pieces/black_bishop.png',
        'r': 'black_pieces/black_rook.png',
        'q': 'black_pieces/black_queen.png',
        'k': 'black_pieces/black_king.png',
    }


class ChessPiece:
    def __init__(self, symbol, color, pos):
        self.symbol = symbol
        self.color = color
        self.pos = pos
        self.x = square_size*pos[0] + 5
        self.y = square_size*pos[1] + 5
    
    def move(self, board):
        pass

# Two-dimensional list to represent the chessboard
#PLACE PIECES#

board = parse_fen(START)

for j in range(8):
    for i in range(8):
        symbol = board[i][j]
        if not symbol: continue
        board[i][j] = ChessPiece(symbol, 'white' if ord(symbol) > ord('A') else 'black', (j, i))

