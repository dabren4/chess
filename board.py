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

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "

class Board:
    def __init__(self):
        
        self.board = parse_fen(START)

        for i in range(8):
            for j in range(8):
                symbol = self.board[i][j]
                self.board[i][j] = p.create_piece(symbol, Vector((i, j)))

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

def parse_fen(string: str):

  board = [['' for _ in range(8)] for _ in range(8)]
  rank, file = 0, 0

  for char in string:
    if char == ' ': break
    if char.isdigit():
      file += int(char)
    elif char in 'prnbkqPRNBKQ':
      board[rank][file] = char
    elif char == '/':
      file = -1
      rank += 1
    file += 1
  return board

def board_to_fen(board):
  pass

if __name__ == '__main__':

  board = parse_fen(START)

  for rank in board:
    for square in rank:
      print(f"{square} ", end='')
    print("\n", end='')
        

    
    
