import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the window size and title
window_size = (640, 640)
window_title = "Chess"
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_title)

# Load the images for the chess pieces
piece_images = {
    'P': pygame.image.load('/home/darren/Documents/projects/chess/white_pawn.png'),
    'N': pygame.image.load('/home/darren/Documents/projects/chess/white_knight.png'),
    'B': pygame.image.load('/home/darren/Documents/projects/chess/white_bishop.png'),
    'R': pygame.image.load('/home/darren/Documents/projects/chess/white_rook.png'),
    'Q': pygame.image.load('/home/darren/Documents/projects/chess/white_queen.png'),
    'K': pygame.image.load('/home/darren/Documents/projects/chess/white_king.png'),
    'p': pygame.image.load('/home/darren/Documents/projects/chess/black_pawn.png'),
    'n': pygame.image.load('/home/darren/Documents/projects/chess/black_knight.png'),
    'b': pygame.image.load('/home/darren/Documents/projects/chess/black_bishop.png'),
    'r': pygame.image.load('/home/darren/Documents/projects/chess/black_rook.png'),
    'q': pygame.image.load('/home/darren/Documents/projects/chess/black_queen.png'),
    'k': pygame.image.load('/home/darren/Documents/projects/chess/black_king.png'),
}

# Set the size of each square on the board
square_size = 80

#Chees Piece Class
class ChessPiece:
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color

# Two-dimensional list to represent the chessboard
board = [[None for i in range(8)] for j in range(8)]

# Place the chess pieces
board[0][0] = ChessPiece('R', 'white')
board[0][1] = ChessPiece('N', 'white')
board[0][2] = ChessPiece('B', 'white')
board[0][3] = ChessPiece('Q', 'white')
board[0][4] = ChessPiece('K', 'white')
board[0][5] = ChessPiece('B', 'white')
board[0][6] = ChessPiece('N', 'white')
board[0][7] = ChessPiece('R', 'white')
for j in range(8):
    board[1][j] = ChessPiece('P', 'white')
board[7][0] = ChessPiece('r', 'black')
board[7][1] = ChessPiece('n', 'black')
board[7][2] = ChessPiece('b', 'black')
board[7][3] = ChessPiece('q', 'black')
board[7][4] = ChessPiece('k', 'black')
board[7][5] = ChessPiece('b', 'black')
board[7][6] = ChessPiece('n', 'black')
board[7][7] = ChessPiece('r', 'black')
for j in range(8):
    board[6][j] = ChessPiece('p', 'black')

# Set the initial position of the selected piece
selected_piece = None
selected_piece_initial_pos = None

# Set the initial position of the mouse
mouse_pos = None

# Game loop
while True:
    # Handle events

    for event in pygame.event.get():
        #Quits if pressed escape
        if event.type == pygame.QUIT:
            # Quit the program when the close button is clicked
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Quit the program when the escape key is pressed
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Convert the mouse position to a square on the board
            mouse_square = (mouse_pos[1] // square_size, mouse_pos[0] // square_size)
            # Check if there is a piece at the mouse position
            if board[mouse_square[0]][mouse_square[1]] is not None:
                # Select the piece
                selected_piece = board[mouse_square[0]][mouse_square[1]]
                selected_piece_initial_pos = mouse_square
        elif event.type == pygame.MOUSEBUTTONUP:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
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
                    selected_piece_initial_pos = None
    # Draw the board
    for i in range(8):
        for j in range(8):
            color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (j * square_size, i * square_size, square_size, square_size))
            piece = board[i][j]
            if piece is not None:
                screen.blit(piece_images[piece.symbol], (j * square_size, i * square_size))
    # Update the display
    pygame.display.flip()
