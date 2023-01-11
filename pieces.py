"""
The main intention of this file is to hold all the classes and info for each piece
"""
import pygame as pg
from stockfish import Stockfish

"""
INSTANCES
"""
stockfish = Stockfish(path="/usr/games/stockfish")
prev_moves = []
square_size = 80

"""
CREATE PIECES AND PIECE CLASSES
"""
piece_images = {
        'P': 'white_pieces/white_pawn.png',
        'N': 'white_pieces/white_knight.png',
        'B': 'white_pieces/white_bishop.png',
        'R': 'white_pieces/white_rook.png',
        'Q': 'white_pieces/white_queen.png',
        'K': 'white_pieces/white_king.png',
        'p': 'black_pieces/black_pawn.png',
        'n': 'black_pieces/black_knight.png',
        'r': 'black_pieces/black_rook.png',
        'q': 'black_pieces/black_queen.png',
        'k': 'black_pieces/black_king.png',
        'b': 'black_pieces/black_bishop.png',
    }

black_pieces = {'p', 'n', 'r', 'q', 'k', 'b'}
white_pieces = {'P', 'N', 'B', 'R', 'Q', 'K'}

class ChessPiece:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.x = square_size*pos[1] + 5
        self.y = square_size*pos[0] + 5
        
    def updatePos(self, pos):
        self.pos = pos
        self.x = square_size*pos[1] + 5
        self.y = square_size*pos[0] + 5

class King(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'K' if color == 'white' else 'k'
    
    def get_possible(self):
        pass

class Queen(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'Q' if color == 'white' else 'q'
    
    def get_possible(self):
        pass

class Bishop(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'B' if color == 'white' else 'b'
    
    def get_possible(self):
        pass

class Rook(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'R' if color == 'white' else 'r'
    
    def get_possible(self):
        pass

class Knight(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'N' if color == 'white' else 'n'
    
    def get_possible(self):
        pass

class Pawn(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'P' if color == 'white' else 'p'
    
    def get_possible(self, pos, depth):
        x, y = pos
        legal_move = []
        if depth == 0:
            if x == 1:
                # If the pawn is in the starting position 
                legal_move.append((x - 2, y))
                legal_move.append((x - 1, y))
            
            elif x > 0:
                # If the pawn is not in the starting position or at the end of the board
                legal_move.append((x - 1, y))
                if y > 0 and board[x - 1][y - 1] != "piece": # Need to fix "piece" to represent if there's a piece there
                    legal_move.append((x - 1, y - 1))
                if y < 7 and board[x - 1][y + 1] != "piece": # ^^
                    legal_move.append((x - 1, y + 1))



board = [[None for _ in range(8)] for _ in range(8)]

board[7][0] = Rook('white', (7,0))
board[7][1] = Knight('white', (7,1))
board[7][2] = Bishop('white', (7,2))
board[7][3] = Queen('white', (7,3))
board[7][4] = King('white', (7,4))
board[7][5] = Bishop('white', (7,5))
board[7][6] = Knight('white', (7,6))
board[7][7] = Rook('white', (7,7))
for j in range(8):
    board[6][j] = Pawn('white', (6, j))
for j in range(8):
    board[1][j] = Pawn('black', (1, j))
board[0][0]= Rook('black', (0, 0))
board[0][1]= Knight('black', (0, 1))
board[0][2]= Bishop('black', (0, 2))
board[0][3]= Queen('black', (0, 3))
board[0][4]= King('black', (0, 4))
board[0][5]= Bishop('black', (0, 5))
board[0][6]= Knight('black', (0, 6))
board[0][7]= Rook('black', (0, 7))

"""
HELPER FUNCTIONS
"""
def draw_board(screen, select_piece, possible_moves):
    """
    Parameters:
        screen: Surface pygame object to be drawn
        select_piece: either NoneType or piece object
        legal_move: Boolean variable that has value determined on whether or not select_piece was able to be moved
    Purpose:
        Draws the board
    """
    for i in range(8):
        for j in range(8):
            if select_piece:
                if (i,j) == select_piece.pos:
                    color = (255, 0, 0)
                elif (i,j) in possible_moves:
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
    """
    Parameters:
        select_piece: piece object that is the selected (previous) piece that will be moved
        row: row to be moved to
        col: column to be moved to
    Purpose:
        Moves select_piece object to (row, col) in the board representation
    """
    #set new position to old and pop select piece position 
    board[row][col] = board[select_piece.pos[0]].pop(select_piece.pos[1])
    #insert None into old spot because will always 
    board[select_piece.pos[0]].insert(select_piece.pos[1], None)
    player_move = translate_to(select_piece.pos, (row, col))
    select_piece.updatePos((row,col))
    return player_move

def translate_to(from_place, to_place):
    """
    Parameters:
        - from_place: (row, col) in terms of row and col the piece comes from 
        - to_place: (row, col) in terms of row and col the piece is going to
    Purpose:
        - Convert tuples into "d2d4" which is standard chess move syntax that stockfish uses
    """
    map_letter = {ix: letter for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
    return map_letter[from_place[1]] + str(8-from_place[0]) + map_letter[to_place[1]] + str(8-to_place[0])

def translate_from(str):
    """
    Parameters:
        - str: In the format "d2d4" which represents coordinate from which a piece is from to where its moving in chessboard coords
    Purpose:
        - Return a tuple that gives ((row, col), (row, col)) in terms of row col the piece comes from and is going to
    """
    map_letter = {letter: ix for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
    return ((8-int(str[1]), map_letter[str[0]]), (8-int(str[3]), map_letter[str[2]]))

def check_quit(event, sys):
    """
    Parameters:
        - event: Event object generated by Pygame (action performed by user(mouseclick, mouse movement, button, etc..))
        - sys: Sys object which controls script
    Purpose:
        - Check the event type for quit and exit the program
    """
    if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

def computer_move(player_move):
    """
    Parameters:
        - player_move: in the form ((from coordinate), (to coordinate))
    Purpose:
        - Generate a best move for the CPU to play using a history of user and CPU moves
    """
    prev_moves.append(player_move)
    stockfish.make_moves_from_current_position([prev_computer[-1], prev_player[-1]] if prev_computer else [prev_player[-1]])
    prev_computer.append(stockfish.get_best_move())
    return prev_computer[-1] 

    