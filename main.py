import pygame as pg
import sys
import pieces as p
import copy as c

def print_board(board):
    print([[p.symbol if p else "" for p in board[r]] for r in range(len(board))])


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
    select_piece = None

    # Game loop
    while True:
        for event in pg.event.get():
            row, col = pg.mouse.get_pos()[1] // square_size, pg.mouse.get_pos()[0] // square_size
            obj = p.board[row][col]


            if event.type == pg.MOUSEBUTTONDOWN:
                if not select_piece:
                    if obj:
                        select_piece = obj
                elif select_piece.can_move(p.board, (row, col)):
                    #set new position to old
                    p.board[row][col] = p.board[select_piece.pos[0]].pop(select_piece.pos[1])
                    p.board[select_piece.pos[0]].insert(select_piece.pos[1], None)
                    select_piece.updatePos((row,col))
                    select_piece = None

            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # Draw the board
        for i in range(8):
            for j in range(8):
                if select_piece and (i, j) == select_piece.pos:
                    color = (100, 200, 100) 
                elif (i + j) % 2 == 0:
                    color = (144, 238, 144) 
                else: 
                    color = (209,245,189)
                
                pg.draw.rect(screen, color, (j * square_size, i * square_size, square_size, square_size))
                piece = p.board[i][j]
                if piece is not None:
                    screen.blit(pg.transform.scale(pg.image.load(p.piece_images[piece.symbol]), (70, 70)), (piece.x, piece.y))

        # Update the display
        pg.display.flip()


            


if __name__ == "__main__":
    play_chess()

    """elif event.type == pg.MOUSEBUTTONUP:
        # Check if a piece is selected
        if selected_piece is not None:
            # Check if the piece can move to the destination square
            if selected_piece.can_move(mouse_square):
                # Move the piece to the destination square
                board[][mouse_square[1]] = selected_piece
                board[selected_piece_initial_pos[0]][selected_piece_initial_pos[1]] = None
                # Deselect the piece
                selected_piece = None
                selected_piece_initial_pos = None
            else:
                # Deselect the piece
                selected_piece = None
                selected_piece_initial_pos = None"""