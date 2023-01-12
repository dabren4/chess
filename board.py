import pieces as p
import main as m
import pygame as pg

LIGHT_RED = (255, 154, 154)
LIGHT_GREEN = (183, 255, 183) 
DARK_GREEN = (135, 212, 135)
WHITE = (255, 255, 255)
LIGHT_RED = (255, 136, 136)

class Vector(tuple):
    def __add__(self, a):
        return Vector(x + y for x, y in zip(self, a))

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        """
        self.board[7][0] = p.Rook('white', Vector((7,0)))
        self.board[7][1] = p.Knight('white', Vector((7,1)))
        self.board[7][2] = p.Bishop('white', Vector((7,2)))
        self.board[7][3] = p.Queen('white', Vector((7,3)))
        self.board[7][4] = p.King('white', Vector((7,4)))
        self.board[7][5] = p.Bishop('white',Vector((7,5)))
        self.board[7][6] = p.Knight('white', Vector((7,6)))
        self.board[7][7] = p.Rook('white', Vector((7,7)))
        for j in range(8):
            self.board[6][j] = p.Pawn('white', Vector((6, j)))
        for j in range(8):
            self.board[1][j] = p.Pawn('black', Vector((1, j)))
        self.board[0][0]= p.Rook('black', Vector((0, 0)))
        self.board[0][1]= p.Knight('black', Vector((0, 1)))
        self.board[0][2]= p.Bishop('black', Vector((0, 2)))
        self.board[0][3]= p.Queen('black', Vector((0, 3)))
        self.board[0][4]= p.King('black', Vector((0, 4)))
        self.board[0][5]= p.Bishop('black', Vector((0, 5)))
        self.board[0][6]= p.Knight('black', Vector((0, 6)))
        self.board[0][7]= p.Rook('black', Vector((0, 7)))
        """
        self.board[4][3] = p.Pawn('black', Vector((4, 3)))
        self.board[6][4] = p.Pawn('white', Vector((6, 4)))
        self.board[5][5] = p.Pawn('white', Vector((5, 5)))
        

    def draw_board(self, screen, select_piece, possible_moves):
        """
        Parameters:
            screen: Surface pygame object to be drawn
            select_piece: either NoneType or piece object
            legal_move: Boolean variable that has value determined on whether or not select_piece was able to be moved
        Purpose:
            Draws the board
        """
        color = None
        for i in range(8):
            for j in range(8):
                if select_piece and (i,j) == select_piece.pos:
                    color = DARK_GREEN
                elif possible_moves and (i,j) in possible_moves:
                    color = LIGHT_RED
                elif (i + j) % 2 == 0:
                    color = LIGHT_GREEN
                else: 
                    color = WHITE
                pg.draw.rect(screen, color, (j * m.SQUARE_SIZE, i * m.SQUARE_SIZE, m.SQUARE_SIZE, m.SQUARE_SIZE))
                piece = self.board[i][j]
                if piece is not None:
                    screen.blit(pg.transform.scale(pg.image.load(m.PIECE_IMAGES[piece.symbol]), (70, 70)), (piece.x, piece.y))
