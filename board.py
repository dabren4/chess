from traitlets import Int
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
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board, self.white_turn, self.castle, self.passant, self.hmove, self.fmove = self.parse_fen(fen)

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

    def parse_fen(self, fen: str) -> list[list[int]]:
        board = [['' for _ in range(8)] for _ in range(8)]
        rank, file, segments = 0, 0, fen.split(' ')
        for segment in range(len(segments)):
            s = segments[segment]
            if segment == 0: # This is the board positioning
                for char in s:
                    if char == ' ': break
                    if char.isdigit():
                        for f in range(int(char)):
                            board[rank][file + f] = None
                        file += int(char)
                    elif char in 'prnbkqPRNBKQ':
                        board[rank][file] = self.create_piece(char, Vector((rank, file)))
                    elif char == '/':
                        file = -1
                        rank += 1
                    file += 1
            elif segment == 1: #To move
                white_turn = s[0] == 'w'
            elif segment == 2: #castling
                castle = [('K' in s, 'Q' in s), ('k' in s, 'q' in s)]
            elif segment == 3: #en passant square
                if s != '-':
                    square = Vector(m.Chess.translate_from('a1'+s)[1]) + ((-1, 0), (1,0))[white_turn]
                    passant = board[square[0]][square[1]]
                else:
                    passant = None
            elif segment == 4: #halfmove counter
                hmove =  int(s)
            elif segment == 5: #fullmove counter
                fmove = int(s)
        return (board, white_turn, castle, passant, hmove, fmove)


    def to_fen(self):
        out = ''
        #board rep
        for row in self.board:
            count = 0
            for val in row:
                if val:
                    if count:
                        out += str(count)
                    out += val.symbol
                    count = 0
                else:
                    count += 1
            if count:
                out += str(count)
            out += '/'
        out = out[:-1]
        out += ' '

        #to move
        out += 'w ' if self.white_turn else 'b '

        #castle
        s = list('KQkq')
        for i in reversed(range(2)):
            for j in reversed(range(2)):
                if not self.castle[i][j]: s.pop(i+j)
        out += ''.join(s) + ' ' if s else '-' + ' '
        
        #passant
        if self.passant: 
            out += self.passant.rep_passant() + ' '
        else: out += '- '
        
        #hmove and full move
        out += str(self.hmove) + ' ' + str(self.fmove) + ' '
        return out
    
    def create_piece(self, symbol, position):
        if not symbol.isalpha():
            return
        color = 'white' if symbol == symbol.upper() else 'black'

        if symbol.lower() == 'p':
            return p.Pawn(color, position)
        elif symbol.lower() == 'r':
            return p.Rook(color, position)
        elif symbol.lower() == 'b':
            return p.Bishop(color, position)
        elif symbol.lower() == 'n':
            return p.Knight(color, position)
        elif symbol.lower() == 'q':
            return p.Queen(color, position)
        elif symbol.lower() == 'k':
            return p.King(color, position)
        else:
            return

if __name__ == '__main__':
    print(Board())
        

    
    
