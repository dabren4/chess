import pygame as pg
from stockfish import Stockfish
import board as b
import main as m


class ChessPiece:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.x = m.SQUARE_SIZE*pos[1] + 5
        self.y = m.SQUARE_SIZE*pos[0] + 5
        
                
    def update_pos(self, pos):
        self.pos = pos
        self.x = m.SQUARE_SIZE*pos[1] + 5
        self.y = m.SQUARE_SIZE*pos[0] + 5
    
    def move(self, board, row, col, passant):
        """
        Parameters:
            select_piece: piece object that is the selected (previous) piece that will be moved
            row: row to be moved to
            col: column to be moved to
        Purpose:
            Moves select_piece object to (row, col) in the board representation
        """
        passant = False #If deciding to move a piece, this removes the passant possibility (unless we are making 2v2)
        board[row][col] = board[self.pos[0]].pop(self.pos[1])
        board[self.pos[0]].insert(self.pos[1], None)
        if type(self) is Pawn and abs(self.pos[0] - row) == 2: passant = self #this sets up the passant move 
        player_move = self.translate_to(self.pos, b.Vector((row, col)))
        self.update_pos(b.Vector((row,col)))
        return player_move
    
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
    
    def get_possible(self, board, passant):
        possible = set()
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if not check_obj or check_obj.color == 'black': 
                    possible.add(self.pos + check)
                    check += cur
        return possible


class Queen(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'Q' if color == 'white' else 'q'
    
    def get_possible(self, board, passant):
        possible = set()
        deltas = [(1,0), (1,-1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == 'white': break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color == 'black': break # break after add because we can overtake black
        return possible

class Bishop(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'B' if color == 'white' else 'b'
    
    def get_possible(self, board, passant):
        possible = set()
        deltas = [(1,-1), (1, 1), (-1, -1), (-1, 1)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == 'white': break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color == 'black': break # break after add because we can overtake black
        return possible

class Rook(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'R' if color == 'white' else 'r'
    
    def get_possible(self, board, passant):
        possible = set()
        deltas = [(0,-1), (0, 1), (-1, 0), (1, 0)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            while 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if check_obj and check_obj.color == 'white': break
                possible.add(self.pos + check)
                check += cur
                if check_obj and check_obj.color == 'black': break # break after add because we can overtake black
        return possible

class Knight(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = 'N' if color == 'white' else 'n'
    
    def get_possible(self, board, passant):
        possible = set()
        deltas = [(-1,-2), (-2,-1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (1, -2)]
        while deltas:
            cur = b.Vector(deltas.pop(0)) # have to cast to vector so addition works element-wise
            check = cur
            if 0 <= self.pos[0] + check[0] < 8 and 0 <= self.pos[1] + check[1] < 8: #check bounds with compound
                check_obj = board[self.pos[0] + check[0]][self.pos[1] + check[1]]
                if not check_obj or check_obj.color == 'black': 
                    possible.add(self.pos + check)
                    check += cur
        return possible

class Pawn(ChessPiece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.passant = False
        self.symbol = 'P' if color == 'white' else 'p'
    
    def get_possible(self, board, passant):
        possible_moves = set()
        if self.color == 'white':
            #first move forward two squares
            if self.pos[0] == 6: 
                check = self.pos + (-2, 0)
                if not board[check[0]][check[1]]: 
                    possible_moves.add(check)
            
            #regular pawn move
            check = self.pos + (-1, 0)
            if not board[check[0]][check[1]]: 
                possible_moves.add(check)
                self.passant = False

            #overtake 
            l_dag, r_dag = self.pos + (-1, -1), self.pos + (-1, 1)
            piece = board[l_dag[0]][l_dag[1]]
            if piece and self.color != piece.color: possible_moves.add(l_dag)
            piece = board[r_dag[0]][r_dag[1]]
            if piece and self.color != piece.color: possible_moves.add(r_dag)

            #passant
            if passant:
                l, r = self.pos + (0, -1), self.pos + (0, 1) #checks if passant is next to the pawn
                if board[l[0]][l[1]] == passant: possible_moves.add(l_dag)
                if board[r[0]][r[1]] == passant: possible_moves.add(l_dag)
            
            return possible_moves












    