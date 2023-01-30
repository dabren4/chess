import board as b
import main as m
import pygame as pg

class ChessPiece:
    def __init__(self, color, pos, symbol=''):
        self.color = color
        self.pos = pos
        self.x = m.SQUARE_SIZE*pos[1] + 5
        self.y = m.SQUARE_SIZE*pos[0] + 5

    def update_pos(self, pos):
        """
        Parameters:
            - pos: Vector representing the row and column of the piece
        """
        self.pos = pos
        self.x = m.SQUARE_SIZE*pos[1] + 5
        self.y = m.SQUARE_SIZE*pos[0] + 5

    def translate_to(self, from_place, to_place):
        """
        Parameters:
            - from_place: (row, col) in terms of row and col the piece comes from
            - to_place: (row, col) in terms of row and col the piece is going to
        Purpose:
            - Convert tuples into "d2d4" which is standard chess move syntax that stockfish uses
        """
        map_letter = {ix: letter for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
        return map_letter[from_place[1]] + str(8-from_place[0]) + map_letter[to_place[1]] + str(8-to_place[0])

    def search_pin(self, board):
        pass

class King(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'K' if color == 'white' else 'k'
        self.moved = False
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def get_possible(self, board, can_attack=False):
        possible = []
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if (self.pos[0] + check[0], self.pos[1] + check[1]) not in board.can_attack:
                    #check if spot is empty, spot is opposite color or we can_attack
                    if not check_obj or check_obj.color != self.color or can_attack:
                        #if empty square or attacking piece and not in attack of a piece
                        possible.append([self.pos + check])
                        check += cur

        #castling rights
        if not self.moved and not board.check: #can't castle if in check
            ix = (0,2)[self.symbol in m.BLACK_PIECES]
            deltas = [(0,1), (0,-1)]
            #extend search horizontally to check if clear
            for i in range(len(deltas)):
                if board.castle[ix + i]: #check if has castling rights first
                    cur = self.pos + deltas[i]
                    count = 1
                    #check if there are no pieces in the way of the castle and that there are no possible attacks in the squares next to the king and where the king lands
                    while not board.board[cur[0]][cur[1]] and (cur not in board.can_attack or count > 2):
                        cur += deltas[i]
                        count += 1
                    if cur[1] == 0 or cur[1] == 7:
                        #append if rows are clear, end indices can't be other than rook becaues self.castle[ix + i] wouldn't be True
                        possible.append([self.pos + ((0,2), (0,-2))[i]])

        #can't move King to sacrifice King
        return possible

class Queen(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'Q' if color == 'white' else 'q'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def get_possible(self, board, can_attack=False):
        possible = []
        if self in board.pinned: return possible
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            l = []
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color:
                    if can_attack: l.append(self.pos + check) #we can attack this piece potentially in next turn (if piece get's taken)
                    break
                l.append(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color: break # break after add because we can overtake black
            possible.append(l)

        if board.check:
            #want to only return squares that protect the King from attack
            check_attack_set = {square for sublist in board.check_attack for square in sublist}
            return [[square] for sublist in possible for square in sublist if square in check_attack_set]
        
        return possible

    def search_pin(self, board):
        deltas = [(1,-1), (1, 1), (-1, 1), (-1, -1), (0,-1), (0, 1), (-1, 0), (1, 0)]
        while deltas:
            poss = None
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                check += cur # check the next square
                if check_obj and type(check_obj) != King and check_obj.color != self.color:
                    poss = check_obj
                    break # break after add because we can overtake black
                elif check_obj:
                    break
            if poss:
                while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                    check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                    if check_obj:
                        if type(check_obj) == King and check_obj.color != self.color: #seeing if we're attacking the opposing king
                            board.pinned.add(poss)
                        break #go to the next delta if this is the case
                    check += cur # check the next square

class Bishop(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'B' if color == 'white' else 'b'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def get_possible(self, board, can_attack=False):
        possible = []
        if self in board.pinned: return possible
        deltas = [(1,-1), (1, 1), (-1, -1), (-1, 1)]
        while deltas:
            l = []
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color:
                    if can_attack: l.append(self.pos + check) #we can attack this piece potentially in next turn (if piece get's taken)
                    break
                l.append(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color: break # break after add because we can overtake black
            possible.append(l)
        if board.check:
            #want to only return squares that protect the King from attack
            check_attack_set = {square for sublist in board.check_attack for square in sublist}
            return [[square] for sublist in possible for square in sublist if square in check_attack_set]
        return possible

    def search_pin(self, board):
        deltas = [(1,-1), (1, 1), (-1, 1), (-1, -1)]
        while deltas:
            poss = None
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and type(check_obj) != King and check_obj.color != self.color:
                    poss = check_obj
                    break # break after add because we can overtake black
                elif check_obj:
                    break
                check += cur # check the next square
            if poss:
                while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                    check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                    if check_obj:
                        if type(check_obj) == King and check_obj.color != self.color: #seeing if we're attacking the opposing king
                            board.pinned.add(poss)
                        break #go to the next delta if this is the case
                    check += cur # check the next square

class Rook(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'R' if color == 'white' else 'r'
        self.moved = False
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def get_possible(self, board, can_attack=False):
        possible = []
        #condition if this piece is a pinned piece
        if self in board.pinned: return possible
        deltas = [(0,-1), (0, 1), (-1, 0), (1, 0)]
        while deltas:
            l = []
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color:
                    if can_attack: l.append(self.pos + check) #we can attack this piece potentially in next turn (if piece get's taken)
                    break
                l.append(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color:
                    break # break after add because we can overtake black
            #add the ray of squares to possible move set
            possible.append(l)
        if board.check:
            #want to only return squares that protect the King from attack
            check_attack_set = {square for sublist in board.check_attack for square in sublist}
            return [[square] for sublist in possible for square in sublist if square in check_attack_set]
        return possible

    def search_pin(self, board):
        """
        This method checks if the Rook is pinning an opponents piece
        """
        deltas = [(0,-1), (0, 1), (-1, 0), (1, 0)]
        while deltas:
            poss = None
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and type(check_obj) != King and check_obj.color != self.color:
                    poss = check_obj
                    break # break after add because we can overtake black
                elif check_obj:
                    break
                check += cur # check the next square
            if poss:
                while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                    check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                    if check_obj:
                        if type(check_obj) == King and check_obj.color != self.color: #seeing if we're attacking the opposing king
                            board.pinned.add(poss)
                        break #go to the next delta if this is the case
                    check += cur # check the next square

class Knight(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'N' if color == 'white' else 'n'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def get_possible(self, board, can_attack=False):
        possible = []
        if self in board.pinned: return
        deltas = [(-1,-2), (-2,-1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (1, -2)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if not check_obj or (check_obj.color != self.color or can_attack): # if square empty or the piece is not our color or we're checking for squares we can attack next turn
                    possible.append([self.pos + check])
                    check += cur
        if board.check:
            #want to only return squares that protect the King from attack
            check_attack_set = {square for sublist in board.check_attack for square in sublist}
            return [[square] for sublist in possible for square in sublist if square in check_attack_set]
        return possible

class Pawn(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'P' if color == 'white' else 'p'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()

    def rep_passant(self):
        return self.translate_to((0, 0), self.pos + ((-1, 0), (1, 0))[self.color == 'white'])[2:]

    def get_possible(self, board, can_attack=False):
        possible = []
        if self in board.pinned: return possible
        white = self.color == 'white'
        #first move forward two squares
        if self.pos[0] == (1, 6)[white]:
            check2 = self.pos + ((2,-2)[white], 0)
            check1 = self.pos + ((1, -1)[white], 0)
            if not board.board[check1[0]][check1[1]] and not board.board[check2[0]][check2[1]] and not can_attack:
                possible.append([check2])

        #regular pawn move
        check = self.pos + ((1,-1)[white], 0)
        if not board.board[check[0]][check[1]] and not can_attack:  #we don't want to add this square when looking for squares that the pawn can attack
            possible.append([check])
            self.passant = False

        #overtake
        l_dag, r_dag = self.pos + ((1,-1)[white], -1), self.pos + ((1,-1)[white], 1)
        if 0 <= l_dag[1] < 8:
            piece = board.board[l_dag[0]][l_dag[1]]
            if piece and (self.color != piece.color or can_attack): possible.append([l_dag])
        if 0 <= r_dag[1] < 8:
            piece = board.board[r_dag[0]][r_dag[1]]
            if piece and (self.color != piece.color or can_attack): possible.append([r_dag])

        #passant
        if board.passant:
            l, r = self.pos + (0, -1), self.pos + (0, 1) #checks if passant is next to the pawn
            if 0 <= l[1] < 8 and board.board[l[0]][l[1]] == board.passant:
                possible.append([l_dag])
            if 0 <= l[1] < 8 and board.board[r[0]][r[1]] == board.passant:
                possible.append([r_dag])

        if board.check:
            #want to only return squares that protect the King from attack
            check_attack_set = {square for sublist in board.check_attack for square in sublist}
            return [[square] for sublist in possible for square in sublist if square in check_attack_set]
        return possible
