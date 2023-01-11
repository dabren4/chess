"""
The main intention of this file is to hold all the classes and info for each piece
"""
import pygame as pg
import random as r
from stockfish import Stockfish

"""
INSTANCES
"""
stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
prev_computer = []
prev_player = []
square_size = 80

"""
CREATE PIECES AND PIECE CLASSES
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

board = [[None for i in range(8)] for j in range(8)]

board[7][0] = ChessPiece('R', 'white', (7,0))
board[7][1] = ChessPiece('N', 'white', (7,1))
board[7][2] = ChessPiece('B', 'white', (7,2))
board[7][3] = ChessPiece('Q', 'white', (7,3))
board[7][4] = ChessPiece('K', 'white', (7,4))
board[7][5] = ChessPiece('B', 'white', (7,5))
board[7][6] = ChessPiece('N', 'white', (7,6))
board[7][7] = ChessPiece('R', 'white', (7,7))
for j in range(8):
    board[6][j] = ChessPiece('P', 'white', (6, j))
for j in range(8):
    board[1][j] = ChessPiece('p', 'black', (1, j))
board[0][0]= ChessPiece('r', 'black', (0, 0))
board[0][1]= ChessPiece('n', 'black', (0, 1))
board[0][2]= ChessPiece('b', 'black', (0, 2))
board[0][3]= ChessPiece('q', 'black', (0, 3))
board[0][4]= ChessPiece('k', 'black', (0, 4))
board[0][5]= ChessPiece('b', 'black', (0, 5))
board[0][6]= ChessPiece('n', 'black', (0, 6))
board[0][7]= ChessPiece('r', 'black', (0, 7))

"""
HELPER FUNCTIONS
"""
def draw_board(screen, select_piece, legal_move):
    for i in range(8):
        for j in range(8):
            if select_piece and (i,j) == select_piece.pos:
                if legal_move:
                    color = (100, 200, 100)
                else:
                    color = (255, 0, 0)
            elif (i + j) % 2 == 0:
                color = (144, 238, 144) 
            else: 
                color = (209,245,189)
            pg.draw.rect(screen, color, (j * square_size, i * square_size, square_size, square_size))
            piece = board[i][j]
            if piece is not None:
                screen.blit(pg.transform.scale(pg.image.load(piece_images[piece.symbol]), (70, 70)), (piece.x, piece.y))

def move_piece(select_piece, row, col):
    print(row, col)
    obj = board[row][col]
    #set new position to old and pop select piece position 
    board[row][col] = board[select_piece.pos[0]].pop(select_piece.pos[1])
    #insert None into old spot because will always 
    board[select_piece.pos[0]].insert(select_piece.pos[1], None)
    player_move = translate_to(select_piece.pos, (row, col))
    select_piece.updatePos((row,col))
    return player_move

def translate_to(from_place, to_place):
    map_letter = {ix: letter for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
    return map_letter[from_place[1]] + str(8-from_place[0]) + map_letter[to_place[1]] + str(8-to_place[0])

def translate_from(str):
    map_letter = {letter: ix for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
    return ((8-int(str[1]), map_letter[str[0]]), (8-int(str[3]), map_letter[str[2]]))

def check_quit(event, sys):
    if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

def computer_move(player_move):
    prev_player.append(player_move)
    stockfish.make_moves_from_current_position([prev_computer[-1], prev_player[-1]] if prev_computer else [prev_player[-1]])
    prev_computer.append(stockfish.get_best_move())
    return prev_computer[-1]

    