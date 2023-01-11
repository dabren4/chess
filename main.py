import pygame as pg
import sys
import pieces as p

def play_chess():
    """
    Purpose:
        - Initialize chess game
    """
    # Initialize Pygame
    pg.init()

    square_size = 80

    # Set the window size and title
    window_size = (640, 640)
    window_title = "Chess"
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption(window_title)

    # Set the size of each square on the board
    select_piece = player_move = None
    player_turn = True
    possible_moves = None
    
    # Game loop
    while True:
        if player_turn:
            for event in pg.event.get():
                row, col = pg.mouse.get_pos()[1] // square_size, pg.mouse.get_pos()[0] // square_size
                obj = p.board[row][col]

                if event.type == pg.MOUSEBUTTONDOWN:
                    if obj and obj.symbol in p.white_pieces: # check if piece is white
                        select_piece = obj
                    elif select_piece.can_move(p.board, (row, col)): # this condition is if we select an empty square or black piece
                        player_move = p.move_piece(select_piece, row, col)
                        select_piece = None
                        player_turn = False
                        
                p.check_quit(event, sys)
        else:
            # This is the computer's turn
            move = p.translate_from(p.computer_move(player_move)) 
            piece = p.board[move[0][0]][move[0][1]]
            p.move_piece(piece, *move[1])
            player_turn = True

        p.draw_board(screen, select_piece, possible_moves)
        pg.display.flip()

if __name__ == "__main__":
    play_chess()
    

"""
def can_move(self, from_square, to_square, board):
    # Get the rows and columns of the squares
    from_row, from_col = from_square
    to_row, to_col = to_square

    # Check if the piece is trying to move to its own square
    if from_square == to_square:
        return False

    # Check if the destination square is out of bounds
    if not (0 <= to_row < 8) or not (0 <= to_col < 8):
        return False

    # Check if pieces can move to the destination square or not
    if self.symbol == 'P':
        # Pawns can only move forward
        if self.color == 'white':
            if from_row > to_row:
                return False
        else:
            if from_row < to_row:
                return False
        # Pawns can move one square forward or capture diagonally
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
    elif self.symbol == 'N':
        # Knights can move in an L-shape
        return abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1
    elif self.symbol == 'B':
        # Bishops can move diagonally
        return abs(from_row - to_row) == abs(from_col - to_col)
    elif self.symbol == 'R':
        # Rooks can move horizontally or vertically
        return from_row == to_row or from_col == to_col
    elif self.symbol == 'Q':
        # Queens can move horizontally, vertically, or diagonally
        return from_row == to_row or from_col == to_col or abs(from_row - to_row) == abs(from_col - to_col)
    elif self.symbol == 'K':
        # Kings can move one square in any direction
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
    else:
        # If there's a bug and it selects an unrecognized piece
        return False
"""