"""
The main intention of this file is to hold all the classes and info for each piece
"""

piece_images = {
        'P': 'white_pieces/white_pawn.png',
        'N': 'white_pieces/white_knight.png',
        'B': 'white_pieces/white_bishop.png',
        'b': 'black_pieces/black_bishop.png',
        'R': 'white_pieces/white_rook.png',
        'Q': 'white_pieces/white_queen.png',
        'K': 'white_pieces/white_king.png',
        'p': 'black_pieces/black_pawn.png',
        'n': 'black_pieces/black_knight.png',
        'r': 'black_pieces/black_rook.png',
        'q': 'black_pieces/black_queen.png',
        'k': 'black_pieces/black_king.png',
    }

class ChessPiece:
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
    
    def move(self, board):
        pass

# Two-dimensional list to represent the chessboard
board = [[None for i in range(8)] for j in range(8)]

# Place the chess pieces
board[0][0] = ChessPiece('R', 'white')
board[0][1] = ChessPiece('N', 'white')
board[0][2] = ChessPiece('B', 'white')
board[0][3] = ChessPiece('Q', 'white')
board[0][4] = ChessPiece('K', 'white')
board[0][5] = ChessPiece('B', 'white')
board[0][6] = ChessPiece('N', 'white')
board[0][7] = ChessPiece('R', 'white')
for j in range(8):
    board[1][j] = ChessPiece('P', 'white')
board[7][0] = ChessPiece('r', 'black')
board[7][1] = ChessPiece('n', 'black')
board[7][2] = ChessPiece('b', 'black')
board[7][3] = ChessPiece('q', 'black')
board[7][4] = ChessPiece('k', 'black')
board[7][5] = ChessPiece('b', 'black')
board[7][6] = ChessPiece('n', 'black')
board[7][7] = ChessPiece('r', 'black')
for j in range(8):
    board[6][j] = ChessPiece('p', 'black')



        
