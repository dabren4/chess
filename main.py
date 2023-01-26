import pygame as pg
import sys
import board as b
import pieces as p
import cpu as c

SQUARE_SIZE = 80
WINDOW_SIZE = (640, 640)
WINDOW_TITLE = "Chess"
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


DARK_PURPLE = (112,102,119)
LIGHT_PURPLE = (204,183,174)

DARK_BROWN = (184,139,74)
LIGHT_BROWN = (227,193,111)

WHITE = (255, 255, 255)
LIGHT_GREEN = (183, 255, 183)

GAME_OPTIONS = {color: ix+1 for ix, color in enumerate(["Player vs. Player", "Player vs. CPU", "Board Color", "Specify FEN", "Exit"])}

class Chess:
    def __init__(self):
        #default values
        self.pvp = True
        self.color_dark = LIGHT_GREEN
        self.color_light = WHITE
        self.fen="r3k2r/4r3/8/8/8/8/8/R3Q2R w KQkq - 0 1" #default value

        #Set options
        while True:
            for k ,v in GAME_OPTIONS.items():
                print(f"{v}. {k}")
            choice = int(input("Enter your choice: "))
            if GAME_OPTIONS["Player vs. Player"] == choice:
                self.pvp = True
                break
            elif GAME_OPTIONS["Player vs. CPU"] == choice:
                self.pvp = False
                break
            elif GAME_OPTIONS["Board Color"] == choice:

                options_color = {color: ix+1 for ix, color in enumerate(["Purple", "Brown", "Default"])}
                print("Which color would you like?: ")
                for i, option_color in enumerate(options_color):
                    print(f"{i + 1}. {option_color}")
                choice_color = int(input("Enter your color choice: "))

                if options_color["Purple"] == choice_color:
                    self.color_dark = DARK_PURPLE 
                    self.color_light = LIGHT_PURPLE
                    print("The board is now set to Purple!")
                elif options_color["Brown"] == choice_color:
                    self.color_dark = DARK_BROWN
                    self.color_light = LIGHT_BROWN
                    print("The board is now set to Brown!")
                elif options_color["Default"] == choice_color:
                    self.color_dark = LIGHT_GREEN
                    self.color_light = WHITE
                    print("The board has been reverted to the default colors!")
                else:
                    print("Invalid")

            elif GAME_OPTIONS["Specify FEN"] == choice:
                self.fen = input("Enter FEN string: ")
            elif GAME_OPTIONS["Exit"] == choice:
                print("Exiting! Thanks for playing.")
                sys.exit()

        # Initialize Pygame
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(WINDOW_TITLE)
        self.p_vs_cpu()
            
    def p_vs_cpu(self) -> None:
        # Set the size of each square on the board
        board = b.Board(self.color_dark, self.color_light, self.fen)
        cpu = c.CPU()
        history = []
        select_piece = possible_moves = drag_pos = highlight_square =  None

        # Game loop
        while True:
            if self.pvp or board.white_turn:
                for event in pg.event.get():
                    #get mouse info
                    row, col = pg.mouse.get_pos()[1] // SQUARE_SIZE, pg.mouse.get_pos()[0] // SQUARE_SIZE
                    if event.type == pg.MOUSEBUTTONDOWN:
                        obj = board.board[row][col]
                        if obj and obj.symbol in (BLACK_PIECES, WHITE_PIECES)[board.white_turn]:
                            #SELECTING A PIECE
                            #change select piece into the obj of choice
                            select_piece = obj 
                            #flatten the list of lists into just list of tuples
                            possible_moves = [square for sublist in select_piece.get_possible(board) for square in sublist]
                    if select_piece:
                        if event.type == pg.MOUSEMOTION:
                            #DRAGGING A PIECE
                            #identify where mouse is and shift back 35 pixels to obtain center 
                            drag_pos = (pg.mouse.get_pos()[1] - 35, pg.mouse.get_pos()[0] - 35) 
                            highlight_square = (row, col)
                        elif event.type == pg.MOUSEBUTTONUP:
                            if select_piece and (row, col) in possible_moves: 
                                #MAKING A MOVE
                                #store previous position info
                                prev_pos = select_piece.pos
                                # move the selected piece
                                board.move(select_piece, row, col) 
                                #append translated move info to history for stockfish
                                history.append(select_piece.translate_to(prev_pos, (row, col))) 
                                #change turns
                                board.white_turn = not board.white_turn 
                                #check and all possible moves opponent can make and check if player to move is in check or checkmate
                                board.check_all() 
                                #count the half move
                                board.hmove += 1
                                #count the full move 
                                if board.white_turn: board.fmove += 1
                            # set these to None because we're moving onto next turn
                            possible_moves = select_piece = highlight_square = drag_pos = None 
                    self.check_quit(event, sys)
            elif not self.pvp and not white_turn:
                
                #send the history to the cpu
                move = cpu.computer_move(history[-2:] if len(history) > 1 else history)
                #append the FEN move to history 
                history.append(move) 
                # translate the FEN to ((row, col), (row, col)) tuple
                move = self.translate_from(move) 
                #move the cpu's piece
                board.move(board.board[move[0][0]][move[0][1]], move[1][0], move[1][1]) 
                #reverse the turn
                white_turn = not white_turn 
                board.hmove += 1
                board.fmove += 1
            
            board.draw_board(self.screen, select_piece, possible_moves, drag_pos, highlight_square)
            pg.display.flip()

    def translate_from(self, str):
        """
        Parameters:
            - str: In the format "d2d4" which represents coordinate from which a piece is from to where its moving in chessboard coords
        Purpose:
            - Return a tuple that gives ((row, col), (row, col)) in terms of row col the piece comes from and is going to
        """
        map_letter = {letter: ix for ix, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])}
        return ((8-int(str[1]), map_letter[str[0]]), (8-int(str[3]), map_letter[str[2]]))
    
    def check_quit(self, event, sys) -> None:
        """
        Parameters:
            - event: Event object generated by Pygame (action performed by user(mouseclick, mouse movement, button, etc..))
            - sys: Sys object which controls script
        Purpose:
            - Check the event type for quit and exit the program
        """
        if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

if __name__ == "__main__": 
    Chess()
