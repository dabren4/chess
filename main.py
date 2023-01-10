import pygame as pg
import sys
import pieces as p


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

    # Game loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            mouse_pos = pg.mouse.get_pos()
            print(mouse_pos)

        # Draw the board
        for i in range(8):
            for j in range(8):
                color = (144, 238, 144) if (i + j) % 2 == 0 else (209,245,189)
                pg.draw.rect(screen, color, (j * square_size, i * square_size, square_size, square_size))
                piece = p.board[i][j]
                if piece is not None:
                    screen.blit(pg.transform.scale(pg.image.load(p.piece_images[piece.symbol]), (70, 70)), (piece.x, piece.y))
        # Update the display
        pg.display.flip()


if __name__ == "__main__":
    play_chess()

"""elif event.type == pg.MOUSEBUTTONDOWN:
        # Get the mouse position
        
        
        # Convert the mouse position to a square on the board
        mouse_square = (mouse_pos[1] // square_size, mouse_pos[0] // square_size)
        print(mouse_square)
        # Check if there is a piece at the mouse position
        if board[mouse_square[0]][mouse_square[1]] is not None:
            # Select the piece
            selected_piece = board[mouse_square[0]][mouse_square[1]]
            selected_piece_initial_pos = mouse_square
    elif event.type == pg.MOUSEBUTTONUP:
        # Get the mouse position
        mouse_pos = pg.mouse.get_pos()
        # Convert the mouse position to a square on the board
        mouse_square = (mouse_pos[1] // square_size, mouse_pos[0] // square_size)
        # Check if a piece is selected
        if selected_piece is not None:
            # Check if the piece can move to the destination square
            if selected_piece.can_move(mouse_square):
                # Move the piece to the destination square
                board[mouse_square[0]][mouse_square[1]] = selected_piece
                board[selected_piece_initial_pos[0]][selected_piece_initial_pos[1]] = None
                # Deselect the piece
                selected_piece = None
                selected_piece_initial_pos = None
            else:
                # Deselect the piece
                selected_piece = None
                selected_piece_initial_pos = None"""
