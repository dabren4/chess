from soupsieve import select
import pieces as p
import main as m
import pygame as pg
from final_constants import *


class Vector(tuple):
    def __add__(self, a):
        return Vector(x + y for x, y in zip(self, a))

class Board:
    def __init__(self, dark_color: tuple, light_color: tuple, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.white_turn = True
        self.dark_color = dark_color
        self.light_color = light_color
        self.fifty_move = 0
        self.checkmate = self.stalemate = False 

        self.parse_fen(fen) #sets variables 
        self.check_all() # This method creates all instances of possible attacking squares and pinned pieces

    def draw_board(self, screen: pg.surface, select_piece, possible_moves: set, drag: tuple, highlight: tuple) -> None:
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
                
                # can attack squares
                """if (i, j) in self.can_attack: 
                    pg.draw.circle(screen, (255, 0, 0), (j * m.SQUARE_SIZE + 40, i * m.SQUARE_SIZE + 40), 10)"""
                
                #draw the dragged object if there is one
                if drag: screen.blit(select_piece.image, (drag[1], drag[0]))

    def move(self, select_piece, row: int, col: int) -> None:
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
        #used instead of the pop and insert method previously used
        self.board[s_pos[0]][s_pos[1]] = None 
        #if capture or pawn movement 50 move rule is reset
        if self.board[row][col] or isinstance(select_piece, p.Pawn): self.fifty_move = 0
        self.fifty_move += 1
        #replace with selected piece
        self.board[row][col] = select_piece
        #Update piece
        select_piece.update_pos(Vector((row,col)))

        #passant
        if type(self) is p.Pawn and abs(s_pos[0] - row) == 2: 
            self.passant = self #this sets up the passant move 
        else:
            self.passant = None 

        #castling
        if isinstance(select_piece, p.King): #used to check the type of the select_piece variable instead of type(select_piece) is p.King
            ix = "KQkq".find(select_piece.symbol)
            # try to move the rook
            if abs(s_pos[1] - col) > 1:
                rook_col = (0, 7)[col > 3]
                rook = self.board[row][rook_col]
                self.move(rook, row, col + (1, -1)[col > 3]) 
            # eliminate castling rights
            self.castle[ix + 1] = False 
            self.castle[ix] = False
        elif type(select_piece) is p.Rook:
            #gets rid of castling rights for respective color side
            ix = (0, 2)[select_piece.symbol in m.BLACK_PIECES] + (0, 1)[s_pos[1] == 0]
            self.castle[ix] = False
        
        #pawn promotion
        if isinstance(select_piece, p.Pawn):
            #check if the pawn is on the last rank
            if select_piece.pos[0] == (0, 7)[select_piece.color == 'black']:
                selection = input("What piece would you like to replace your pawn with? \nOptions: \n   1. Queen \n   2. Rook \n   3. Bishop \n   4. Knight \nEnter: ")
                while selection not in {'1', '2', '3', '4'}:
                    selection = input("Invalid selection, please try again: ")
                if selection == '1':
                    self.board[row][col] = p.Queen(select_piece.color, Vector((row, col)))
                elif selection == '2':
                    self.board[row][col] = p.Rook(select_piece.color, Vector((row, col)))
                elif selection == '3':
                    self.board[row][col] = p.Bishop(select_piece.color, Vector((row, col)))
                else:
                    self.board[row][col] = p.Knight(select_piece.color, Vector((row, col)))

        #Check if we need to change for the king/rook (castling purposes)
        select_piece.moved = True #set to true regardless of the try-except block.
        
    def check_all(self) -> None:
        """
        This function checks the board for all possible moves for a specified color AFTER each move 
        RETURNS SET OF (ROW, COL) THAT SQUARES THAT CURRENT PLAYER CAN ATTACK AND SET OF PINNED PIECES 
        TO DO Consolidate searches for all pieces so that we don't have two similar blocks 

        can_attack: set of squares where the opponent can move and attack from current board position
        check_attack: set of squares which includes both the squares of the pieces that are attacking the king and their ray of attacking squares (Rook, Queen, Bishop)
            - The idea with this is to form an idea of where to move pieces in order to save the king
        checkmate: a conditional based on possible moves from proponent's position in response to a check
        """
        self.can_attack = self.pinned = set()
        self.check_attack = []
        self.check = self.checkmate = self.king = False

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                obj = self.board[row][col]
                #want to find opposite of whose turn it is (want to find possible attack from opponent)
                if obj and obj.symbol in (m.BLACK_PIECES, m.WHITE_PIECES)[not self.white_turn]: 
                    #We are checking List of rays (List of Vectors representing squares extending from the piece) of possible movement for the piece
                    for ray in obj.get_possible(self, True):
                        for square in ray:
                            #add the square to can_attack
                            self.can_attack.add(square)
                            #check if the square we are checking contains the opponent king
                            if isinstance(self.board[square[0]][square[1]], p.King) and self.board[square[0]][square[1]].symbol in (m.BLACK_PIECES, m.WHITE_PIECES)[self.white_turn]: 
                                #if it is then we need to realize that we are in check
                                self.check = True
                                self.king = self.board[square[0]][square[1]]
                                #need to add array of squares that lead to the check including the piece itself (we should be able to kill a piece to protect the King!)
                                self.check_attack.append(ray + [obj.pos]) 
                    #we need to check if the opponent is pinning one of our pieces (shouldn't be able to move pinned piece)
                    obj.search_pin(self) 
        
        #checkmate check
        if self.check:
            # check if adjacent squares can be moved to
            if not self.king.get_possible(self):
                if len(self.check_attack) > 1:
                    # cannot defend more than two pieces attacking at once and also no squares for King to move to
                    self.checkmate = True
                elif len(self.check_attack) == 1:
                    #need to check all of our pieces to make sure it blocks the ray
                    ray_check = set(self.check_attack[0])
                    checkmate_flag = True
                    for row in range(len(self.board)):
                        for col in range(len(self.board[0])):
                            obj = self.board[row][col]
                            #check if obj is a piece and the color is the player to play
                            if obj and obj.symbol in (m.BLACK_PIECES, m.WHITE_PIECES)[self.white_turn]:
                                for ray in obj.get_possible(self):
                                    for square in ray:
                                        if square in ray_check:
                                            checkmate_flag = False
                    if checkmate_flag:
                        self.checkmate = True
                else:
                    self.stalemate = True
                
    def parse_fen(self, fen: str) -> None:
        self.board = [['' for _ in range(8)] for _ in range(8)]
        rank, file, segments = 0, 0, fen.split(' ')

        #need to initialize castling before we initialize pieces to give possible move set
        s = segments[2]
        print("CASTLE FEN", s)
        self.castle = ['K' in s, 'Q' in s, 'k' in s, 'q' in s]

        for segment in range(len(segments)):
            s = segments[segment]
            if segment == 0: # This is the board positioning
                for char in s:
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

    def to_fen(self) -> str:
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
        print("Castling rights are ", self.castle)
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


    
    