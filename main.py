import pygame as pg
import sys
import board as b
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

#Text Menu

options = ["Player vs Player", "Player vs CPU", "Board Color", "Exit"]


class Chess:
    def __init__(self, pvp):
        """
        ##################
        IMPORTANT!!!!
        ##################
        We could have stuff like difficulty, mode and other options that we can feed into this constructor
        That way we can initialize different Chess games based on user input
        """
        # Initialize Pygame
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(WINDOW_TITLE)

        self.pvp = pvp
        
    def p_vs_cpu(self, white_turn=True, castle=[(True, True), (True, True)], passant=None, hmove=0, fmove=0):
        # Set the size of each square on the board
        board_obj = b.Board()
        board = board_obj.board
        cpu = c.CPU()
        history = []
        select_piece = None
        possible_moves = None
        drag = None
        highlight_square = None
        
        # Game loop
        while True:
            if self.pvp or white_turn:
                for event in pg.event.get():
                    #get mouse info
                    row, col = pg.mouse.get_pos()[1] // SQUARE_SIZE, pg.mouse.get_pos()[0] // SQUARE_SIZE
                    obj = board[row][col]

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if obj and obj.symbol in (BLACK_PIECES, WHITE_PIECES)[white_turn]:
                            #SELECTING A PIECE
                            select_piece = obj #change select piece into the obj of choice
                            possible_moves = select_piece.get_possible(board, passant) # get possible moves for piece

                    if select_piece:
                        if event.type == pg.MOUSEMOTION:
                            
                            drag = (pg.mouse.get_pos()[1] - 35, pg.mouse.get_pos()[0] - 35)
                            highlight_square = (row, col)

                        elif event.type == pg.MOUSEBUTTONUP:
                            if select_piece and (row, col) in possible_moves: 
                                #MAKING A MOVE
                                move = select_piece.move(board, row, col) # move the selected piece and store info
                                history.append(move[0]) #append translated move info to history
                                board_obj.passant = move[1] # add passant to list if a pawn had start move
                                possible_moves = select_piece = highlight_square = drag = None # set these to None because we're moving onto next turn
                                
                                white_turn = not white_turn #change the turn 
                                board_obj.hmove += 1
                            else:
                                possible_moves = select_piece = highlight_square = drag = None # set these to None because we're moving onto next turn

                    self.check_quit(event, sys)

            elif not self.pvp and not white_turn:
                move = cpu.computer_move(history[-2:] if len(history) > 1 else history)
                history.append(move) #append the translated move to history 
                move = self.translate_from(move)
                board_obj.passant = board[move[0][0]][move[0][1]].move(board, *move[1])[1]
                
                white_turn = not white_turn
                board_obj.hmove += 1
                board_obj.fmove += 1
                
            board_obj.draw_board(self.screen, select_piece, possible_moves, drag, highlight_square)

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
    
    def check_quit(self, event, sys):
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

#Previous Run Function
#if __name__ == "__main__": 
#    Chess(False).p_vs_cpu()


DARK_PURPLE = (112,102,119)
LIGHT_PURPLE = (204,183,174)

DARK_BROWN = (184,139,74)
LIGHT_BROWN = (227,193,111)

WHITE = (255, 255, 255)
LIGHT_GREEN = (183, 255, 183)

color_dark = LIGHT_GREEN
color_light = WHITE

#Game Menu
if __name__ == "__main__": 
    while True:
        print("Please select an option:")
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        choice = input()
        if choice.isnumeric() and int(choice) in range(1, len(options) + 1):
            if options[int(choice) - 1] == "Player vs Player":
                Chess(True).p_vs_cpu()
            elif options[int(choice) - 1] == "Player vs CPU":
                Chess(False).p_vs_cpu()

            elif options[int(choice) - 1] == "Board Color":
                
                


                options_color = ["Purple", "Brown", "Default"]

                print("Which color would you like?: ")
                for i, option_color in enumerate(options_color):
                    print(f"{i + 1}. {option_color}")
                choice_color = input()
                if choice_color.isnumeric() and int(choice_color) in range(1, len(option_color) + 1):
                    if options_color[int(choice_color) - 1] == "Purple":
                        color_dark = DARK_PURPLE 
                        color_light = LIGHT_PURPLE
                        print("The board is now set to Purple!")
                        
                    elif options_color[int(choice_color) - 1] == "Brown":
                        color_dark = DARK_BROWN
                        color_light = LIGHT_BROWN
                        print("The board is now set to Brown!")
                        
                    elif options_color[int(choice_color) - 1] == "Default":
                        color_dark = b.LIGHT_GREEN
                        color_light = b.WHITE
                        print("The board has been reverted to the default colors!")
                        
                    
                    else:
                        print("Invalid")
                        
                    

            elif options[int(choice) - 1] == "Exit":
                print("Exiting! Thanks for playing.")
                sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and", len(options))
