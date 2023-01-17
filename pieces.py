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
    

class King(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'K' if color == 'white' else 'k'
        self.moved = False
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()
    
    def get_possible(self, board, can_attack=False):
        possible = set()
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if not check_obj or check_obj.color != self.color: 
                    possible.add(self.pos + check)
                    check += cur

        #castling rights
        #TO DO MAKE SURE LINE OF SIGHT IS CLEAR OFCAN ATTACK
        if not self.moved:
            ix = (0,2)[self.symbol in m.BLACK_PIECES]
            deltas = [(0,1), (0,-1)]

            #extend search horizontally to check if clear
            for i in range(len(deltas)):
                if board.castle[ix + i]:
                    cur = self.pos + deltas[i]
                    while not board.board[cur[0]][cur[1]]:
                        cur += deltas[i]
                    if cur[1] == 0 or cur[1] == 7:
                        possible.add(self.pos + ((0,2), (0,-2))[i]) #add if rows are clear, end indices can't be other than rook becaues self.castle[ix + i] wouldn't be True

        return possible

class Queen(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'Q' if color == 'white' else 'q'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()
    
    def get_possible(self, board, can_attack=False):
        possible = set()
        if self in board.pinned: return possible
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color: break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color: break # break after add because we can overtake black
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
                print(poss)
                while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                    check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                    print("check", check_obj)
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
        if self in board.pinned: return possible
        deltas = [(1,-1), (1, 1), (-1, -1), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color: break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color: break # break after add because we can overtake black
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
        possible = set()
        if self in board.pinned: return possible
        deltas = [(0,-1), (0, 1), (-1, 0), (1, 0)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == self.color: 
                    break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color != self.color: 
                    break # break after add because we can overtake black
        return possible

    def search_pin(self, board):
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
    
    def get_possible(self, board):
        possible = set()
        if self in board.pinned: return 
        deltas = [(-1,-2), (-2,-1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (1, -2)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board.board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if not check_obj or check_obj.color != self.color: 
                    possible.add(self.pos + check)
                    check += cur

class Pawn(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'P' if color == 'white' else 'p'
        self.image = pg.transform.scale(pg.image.load(m.PIECE_IMAGES[self.symbol]), (70, 70)).convert_alpha()
    
    def rep_passant(self):
        return self.translate_to((0, 0), self.pos + ((-1, 0), (1, 0))[self.color == 'white'])[2:]

    def get_possible(self, board, can_attack=False):
        possible = set()
        if self in board.pinned: return possible
        white = self.color == 'white'
        #first move forward two squares
        if self.pos[0] == (1, 6)[white]: 
            check2 = self.pos + ((2,-2)[white], 0)
            check1 = self.pos + ((1, -1)[white], 0)
            if not board.board[check1[0]][check1[1]] and not board.board[check2[0]][check2[1]] and not can_attack: 
                possible.add(check2)
        
        #regular pawn move
        check = self.pos + ((1,-1)[white], 0)
        if not board.board[check[0]][check[1]] and not can_attack:  #we don't want to add this square when looking for squares that the pawn can attack
            possible.add(check)
            self.passant = False

        #overtake 
        l_dag, r_dag = self.pos + ((1,-1)[white], -1), self.pos + ((1,-1)[white], 1)
        if 0 <= l_dag[1] < 8:
            piece = board.board[l_dag[0]][l_dag[1]]
            if piece and self.color != piece.color: possible.add(l_dag)
        if 0 <= r_dag[1] < 8:
            piece = board.board[r_dag[0]][r_dag[1]]
            if piece and self.color != piece.color: possible.add(r_dag)

        #passant
        if board.passant:
            l, r = self.pos + (0, -1), self.pos + (0, 1) #checks if passant is next to the pawn
            if 0 <= l[1] < 8 and board.board[l[0]][l[1]] == board.passant: 
                possible.add(l_dag)
            if 0 <= l[1] < 8 and board.board[r[0]][r[1]] == board.passant: 
                possible.add(r_dag)
        
        return possible
        