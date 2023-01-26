import pieces as p
import main as m
import pygame as pg

DARK_GREEN = (135, 212, 135)
LIGHT_YELLOW = (255,255,102)
LIGHT_GREY = (175,175,175)

class Vector(tuple):
    def __add__(self, a):
        return Vector(x + y for x, y in zip(self, a))

class Board:
    def __init__(self, dark_color: tuple, light_color: tuple, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.white_turn = True
        self.dark_color = dark_color
        self.light_color = light_color



        self.parse_fen(fen) #sets variables 
        self.check_all() # This method creates all instances of possible attacking squares and pinned pieces
        
        for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if isinstance(piece, p.Rook):
                        self.castle[(0, 2)[piece.symbol in m.BLACK_PIECES] + (0, 1)[j == 0]] = piece.moved
                    elif isinstance(piece, p.King):
                        self.castle[(0, 2)[piece.symbol in m.BLACK_PIECES]] = piece.moved

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
                if (i, j) in self.can_attack: pg.draw.circle(screen, (255, 0, 0), (j * m.SQUARE_SIZE + 40, i * m.SQUARE_SIZE + 40), 10)
                
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
        self.board[row][col] = select_piece
        select_piece.pos = (row, col)

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
        
        #Check if we need to change for the king/rook (castling purposes)
        select_piece.moved = True #set to true regardless of the try-except block.
        
        #Update piece
        select_piece.update_pos(Vector((row,col)))

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
        self.can_attack = self.check_attack = self.pinned = set()
        self.check = self.checkmate = False

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                obj = self.board[row][col]
                #want to find opposite of whose turn it is (want to find possible attack from opponent)
                if obj and obj.symbol in (m.BLACK_PIECES, m.WHITE_PIECES)[not self.white_turn]: 
                    #We are checking List of rays (List of Vectors representing squares extending from the piece) of possible movement for the piece
                    print(obj)
                    for ray in obj.get_possible(self, True):
                        for square in ray:
                            #add the square to can_attack
                            self.can_attack.add(square)
                            #check if the square we are checking contains the opponent king
                            if isinstance(self.board[square[0]][square[1]], p.King) and obj.symbol in (m.BLACK_PIECES, m.WHITE_PIECES)[self.white_turn]: 
                                #if it is then we need to realize that we are in check
                                self.check = True
                                #need to add array of squares that lead to the check
                                self.check_attack.add(ray) 
                    #we need to check if the opponent is pinning one of our pieces (shouldn't be able to move pinned piece)
                    obj.search_pin(self) 
        
        #WE WOULD ONLY RUN THIS CHECKER IF KING IS UNDER
        #checkmate checker
        #we need to determine if all empty squares adjacent to King are under attack
        #IF ALL EMPTY SQUARES ADJ TO KING ARE UNDER ATTACK
            #Look at trying to take out attacking pieces/blocking their attacks
            #Check the length of check_attack (if > 1 then we know checkmate!)
            #IF NOT AND LENGTH OF CHECK_ATTACK == 1
                #Check where your opponents pieces can move after your move (potential overtake or block)
                #WAYS TO BLOCK: KILL ATTACKER WITH KING, KILL ATTACKER WITH OTHER PIECE, BLOCK ATTACKER WITH OTHER PIECE
                    #BLOCK OR KILL ATTACKER WITH OTHER PIECE (check whether possible moves can kill or block attacking piece, if they can, then add to possible moves)
                        #This requires the set of lists of rays
                    #KILL ATTACKER WITH KING (check whether the piece it is trying to kill can be attacked by another piece, if not add to possible moves) #THIS WILL REQUIRE HAVING BOOLEAN CONDITION ON get_possible (check_condition)

    def parse_fen(self, fen: str) -> None:
        self.board = [['' for _ in range(8)] for _ in range(8)]
        rank, file, segments = 0, 0, fen.split(' ')

        #need to initialize castling before we initialize pieces to give possible move set
        print(segments)
        s = segments
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


    
    