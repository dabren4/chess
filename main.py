from fnmatch import translate
import pygame as pg
import sys
import pieces as p
import copy as c
from stockfish import Stockfish

def play_chess():
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
    legal_move = True
    player_turn = True
    
    # Game loop
    while True:
        if not legal_move:
            select_piece = None
        legal_move = True

        if player_turn:
            for event in pg.event.get():
                row, col = pg.mouse.get_pos()[1] // square_size, pg.mouse.get_pos()[0] // square_size
                obj = p.board[row][col]

                if event.type == pg.MOUSEBUTTONDOWN:
                    if not select_piece:
                        if obj and obj.symbol.upper() == obj.symbol: #check if piece is white
                            select_piece = obj
                    elif select_piece.can_move(p.board, (row, col)):
                        player_move = p.move_piece(select_piece, row, col)
                        select_piece = None
                        player_turn = False
                    else:
                        legal_move = False
                p.check_quit(event, sys)
        else:
            move = p.translate_from(p.computer_move(player_move))
            piece = p.board[move[0][0]][move[0][1]]
            p.move_piece(piece, *move[1])
            player_turn = True

        p.draw_board(screen, select_piece, legal_move)
        pg.display.flip()

if __name__ == "__main__":
    play_chess()
    
