#Colors
DARK_GREEN = (135, 212, 135)
LIGHT_YELLOW = (255,255,102)
LIGHT_GREY = (175,175,175)
DARK_PURPLE = (112,102,119)
LIGHT_PURPLE = (204,183,174)
DARK_BROWN = (184,139,74)
LIGHT_BROWN = (227,193,111)
WHITE = (255, 255, 255)
LIGHT_GREEN = (183, 255, 183)

#Game constants
SQUARE_SIZE = 80
WINDOW_SIZE = (640, 640)
WINDOW_TITLE = "Chess"
GAME_OPTIONS = {color: ix+1 for ix, color in enumerate(["Player vs. Player", "Player vs. CPU", "Board Color", "Specify FEN", "Exit"])}

#Piece info
PIECE_IMAGES = {
    'P': 'white_pieces/white_pawn.png',
    'N': 'white_pieces/white_knight.png',
    'B': 'white_pieces/white_bishop.png',
    'R': 'white_pieces/white_rook.png',
    'Q': 'white_pieces/white_queen.png',
    'K': 'white_pieces/white_king.png',
    'p': 'black_pieces/black_pawn.png',
    'n': 'black_pieces/black_knight.png',
    'r': 'black_pieces/black_rook.png',
    'q': 'black_pieces/black_queen.png',
    'k': 'black_pieces/black_king.png',
    'b': 'black_pieces/black_bishop.png',
}
BLACK_PIECES = {'p', 'n', 'r', 'q', 'k', 'b'}
WHITE_PIECES = {'P', 'N', 'B', 'R', 'Q', 'K'}

#Unit Test FENS
UNIT_TEST_FENS = {
    'Castle Pin': "r3k2r/4r3/8/8/8/8/8/R3Q2R w KQkq - 0 1",
    'Pawn Promotion': "8/4P3/8/8/8/8/8/8 w KQkq - 0 1",
    'Default': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}
