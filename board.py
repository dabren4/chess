from traitlets import Int
import pieces as p
import main as m
import pygame as pg

LIGHT_RED = (255, 154, 154)
LIGHT_GREEN = (183, 255, 183) 
DARK_GREEN = (135, 212, 135)
WHITE = (255, 255, 255)
LIGHT_YELLOW = (255,255,102)
LIGHT_GREY = (175,175,175)

#Board Colors


class Vector(tuple):
    def __add__(self, a):
        return Vector(x + y for x, y in zip(self, a))

class Board:
    def __init__(self, dark_color, light_color, fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"):
        self.dark_color = dark_color
        self.light_color = light_color
        self.parse_fen(fen)

    def draw_board(self, screen, select_piece, possible_moves, drag: tuple, highlight: tuple):
        """
        Parameters:
            screen: Surface pygame object to be drawn
            select_piece: either NoneType or piece object
            legal_move: Boolean variable that has value determined on whether or not select_piece was able to be moved
        Purpose:
            Draws the board
        """
        square_color = None
        for i in range(8):
            for j in range(8):
                #squares
                if select_piece and (i,j) == select_piece.pos:
                    square_color = DARK_GREEN
                elif drag and (i,j) == highlight: 
                    square_color = LIGHT_YELLOW
                elif (i + j) % 2 == 0:
                    square_color = self.light_color
                else: 
                    square_color = self.dark_color
                pg.draw.rect(screen, square_color, (j * m.SQUARE_SIZE, i * m.SQUARE_SIZE, m.SQUARE_SIZE, m.SQUARE_SIZE))

                #draw piece
                piece = self.board[i][j]
                if piece and piece != select_piece: screen.blit(piece.image, (piece.x, piece.y))
                if select_piece and piece == select_piece and not drag: screen.blit(piece.image, (piece.x, piece.y))

                #possible move dots
                if possible_moves and (i, j) in possible_moves:
                    pg.draw.circle(screen, LIGHT_GREY, (j * m.SQUARE_SIZE + 40, i * m.SQUARE_SIZE + 40), 10)
                
                #draw the dragged object if there is one
                if drag: screen.blit(select_piece.image, (drag[1], drag[0]))

    def move(self, select_piece, row, col):
        """
        Parameters:
            select_piece: piece object that is the selected (previous) piece that will be moved
            row: row to be moved to
            col: column to be moved to
        Purpose:
            Moves select_piece object to (row, col) in the board representation
            Try to see if the move piece creates a check
        """
        # has to be in this order otherwise indexing gets messed up
        s_pos = select_piece.pos
        temp = self.board[s_pos[0]].pop(s_pos[1]) 
        self.board[s_pos[0]].insert(s_pos[1], None)
        self.board[row][col] = temp

        #passant
        if type(self) is p.Pawn and abs(s_pos[0] - row) == 2: 
            self.passant = self #this sets up the passant move 
        else:
            self.passant = None 

        #castling
        if type(select_piece) is p.King:
            ix = "KQkq".find(select_piece.symbol)
            #try to move the rook
            if abs(s_pos[1] - col) > 1: self.move(self.board[row][(0,7)[col > 3]], row, col + (1,-1)[col > 3]) 
            #eliminate castling rights
            self.castle[ix+1] = False 
            self.castle[ix] = False
        elif type(select_piece) is p.Rook:
            #gets rid of castling rights for respective color side
            ix = (0, 2)[select_piece.symbol in m.BLACK_PIECES] + (0, 1)[s_pos[1] == 0]
            self.castle[ix] = False
        
        #Check if we need to change for the king/rook (castling purposes)
        try:
            if not self.moved: self.moved = True
        except:
            pass
        
        #Update piece
        select_piece.update_pos(Vector((row,col)))
                
    def parse_fen(self, fen: str) -> list[list[int]]:
        self.board = [['' for _ in range(8)] for _ in range(8)]
        rank, file, segments = 0, 0, fen.split(' ')
        for segment in range(len(segments)):
            s = segments[segment]
            if segment == 0: # This is the board positioning
                for char in s:
                    print("file is", file, "with value", char)
                    if char == ' ': break
                    if char.isdigit():
                        for f in range(int(char)):
                            self.board[rank][file + f] = None
                        file += int(char)
                    elif char in 'prnbkqPRNBKQ':
                        self.board[rank][file] = self.create_piece(char, Vector((rank, file)))
                        file += 1
                    elif char == '/':
                        file = 0
                        rank += 1
            elif segment == 1: #To move
                self.white_turn = s[0] == 'w'
            elif segment == 2: #castling
                self.castle = ['K' in s, 'Q' in s, 'k' in s, 'q' in s]
            elif segment == 3: #en passant square
                if s != '-':
                    square = Vector(m.Chess.translate_from('a1'+s)[1]) + ((-1, 0), (1,0))[self.white_turn]
                    self.passant = self.board[square[0]][square[1]]
                else:
                    self.passant = None
            elif segment == 4: #halfmove counter
                self.hmove =  int(s)
            elif segment == 5: #fullmove counter
                self.fmove = int(s)

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
        castle_rep = 'KQkq'
        no_castle = True
        for ix in range(len(castle_rep)):
            if self.castle[ix]: 
                out += castle_rep[ix]
                no_castle = False
        if no_castle: out += '-'
        out += ' '
        
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


    
    
