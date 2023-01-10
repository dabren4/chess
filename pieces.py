"""
The main intention of this file is to hold all the classes and info for each piece
"""

square_size = 80

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
    def __init__(self, symbol, color, pos):
        self.symbol = symbol
        self.color = color
        self.pos = pos
        self.x = square_size*pos[1] + 5
        self.y = square_size*pos[0] + 5
    
    def can_move(self, board, place):
        return True

    def updatePos(self, pos):
        self.pos = pos
        self.x = square_size*pos[1] + 5
        self.y = square_size*pos[0] + 5

#PLACE PIECES#
board = [[None for i in range(8)] for j in range(8)]

board[0][0] = ChessPiece('R', 'white', (0, 0))
board[0][1] = ChessPiece('N', 'white', (0, 1))
board[0][2] = ChessPiece('B', 'white', (0, 2))
board[0][3] = ChessPiece('Q', 'white', (0, 3))
board[0][4] = ChessPiece('K', 'white', (0, 4))
board[0][5] = ChessPiece('B', 'white', (0, 5))
board[0][6] = ChessPiece('N', 'white', (0, 6))
board[0][7] = ChessPiece('R', 'white', (0, 7))
for j in range(8):
    board[1][j] = ChessPiece('P', 'white', (1, j))
for j in range(8):
    board[6][j] = ChessPiece('p', 'black', (6, j))
board[7][0] = ChessPiece('r', 'black', (7,0))
board[7][1] = ChessPiece('n', 'black', (7,1))
board[7][2] = ChessPiece('b', 'black', (7,2))
board[7][3] = ChessPiece('q', 'black', (7,3))
board[7][4] = ChessPiece('k', 'black', (7,4))
board[7][5] = ChessPiece('b', 'black', (7,5))
board[7][6] = ChessPiece('n', 'black', (7,6))
board[7][7] = ChessPiece('r', 'black', (7,7))




        
