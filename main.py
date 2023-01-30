import pygame as pg
import sys
import board as b
from cpu import CPU
from final_constants import *




class Chess:
    def __init__(self):
        #default values
        self.pvp = True
        self.color_dark = LIGHT_GREEN
        self.color_light = WHITE

        self.options = ["Player vs. Player", "Player vs. CPU", "Board Color", "Specify FEN", "Exit"]
        self.color_options = {color: ix+1 for ix, color in enumerate(["Purple", "Brown", "Default"])}
        self.screen_width = 640

        self.fen= UNIT_TEST_FENS['Checkmate R']

        # Initialize Pygame
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.font = pg.font.Font(None, 32)
        pg.display.set_caption(WINDOW_TITLE)
        self.menu()


    def menu(self):

        pg.init()
        pg.display.set_caption("Menu")
        font = pg.font.Font(None, 32)
        selected_index = 0


        while True:
          # Handle events
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_UP:
                      # Move the selection up
                      selected_index = max(0, selected_index - 1)
                  elif event.key == pg.K_DOWN:
                      # Move the selection down
                      selected_index = min(len(self.options) - 1, selected_index + 1)
                  elif event.key == pg.K_RETURN:
                      # Handle the selected option
                      if self.options[selected_index] == "Player vs. Player":
                          self.p_vs_cpu()
                          self.pvp = True
                          break
                      elif self.options[selected_index] == "Player vs. CPU":
                          self.p_vs_cpu()
                          self.pvp = False
                          break
                      elif self.options[selected_index] == "Board Color":
                          self.board_color_menu()
                      elif self.options[selected_index] == "Specify FEN":
                          # Do something for the "Specify FEN" option
                          pass
                      elif self.options[selected_index] == "Exit":
                          # Exit the game
                          pg.quit()
                          sys.exit()

          self.screen.fill((0, 0, 0))

          # Draw the menu options
          for i, option in enumerate(self.options):
              text = font.render(option, True, (255, 255, 255))
              x = (self.screen.get_width() - text.get_width()) // 2
              y = (self.screen.get_height() - len(self.options) * text.get_height()) // 2 + i * text.get_height()
              if i == selected_index:
                  # Draw the selected option in a different color
                  text = font.render(option, True, (255, 0, 0))
              self.screen.blit(text, (x, y))

          # Update the display
          pg.display.update()

    def board_color_menu(self):
        pg.init()
        pg.display.set_caption("Board Color")
        font = pg.font.Font(None, 32)
        color_selected_index = 0
        while True:
            for color_event in pg.event.get():
                if color_event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif color_event.type == pg.KEYDOWN:
                    if color_event.key == pg.K_UP:
                        color_selected_index = max(0, color_selected_index - 1)
                    elif color_event.key == pg.K_DOWN:
                        color_selected_index = min(len(self.color_options) - 1, color_selected_index + 1)
                    elif color_event.key == pg.K_RETURN:
                        if self.color_options[color_selected_index] == "Purple":
                            self.color_dark = DARK_PURPLE
                            self.color_light = LIGHT_PURPLE
                            break
                        elif self.color_options[color_selected_index] == "Brown":
                            self.color_dark = DARK_BROWN
                            self.color_light = LIGHT_BROWN
                            break
                        elif self.color_options[color_selected_index] == "Default":
                            self.color_dark = LIGHT_GREEN
                            self.color_light = WHITE
                            break
            # Render the color options
            for i, option_color in enumerate(self.color_options):
                if i == color_selected_index:
                    text = font.render(option_color, True, (255, 255, 255))
                else:
                    text = font.render(option_color, True, (100, 100, 100))
                self.screen.blit(text, (100, 100 + i * 50))

##TO DO: Make code simpler and more concise:
#   Check 50 move rule
#   Make sure that we're not in check (Check all function)
#   
#   Ifin check (do the check all)
#       - We are checking our opponents possible moves
#       - If in check, check if in checkmate
#   If we are not in check
#       - Check all of our possible moves
#           - Relate in dictionary the unique piece object to a list of list of possible squares that it could move to
#       - If that list is empty we are in a stalemate
#   Then we make our move and repeat list




    def p_vs_cpu(self) -> None:
        # Set the size of each square on the board
        board = b.Board(self.color_dark, self.color_light, self.fen)
        cpu = CPU()
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
                            possible_moves = [square for sublist in select_piece.get_possible(board, False) for square in sublist]
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
                                print(board.to_fen())
                                #if checkmate, then stop the game
                                if board.checkmate:

                                    # Load a font
                                    font = pg.font.Font(None, 36)

                                    # Render the text "checkmate"
                                    text = font.render("checkmate", True, (255, 255, 255))

                                    #Center the text
                                    text_rect = text.get_rect()
                                    text_rect.center = (640 / 2, 640 / 2)

                                    # Blit the text onto the screen
                                    self.screen.blit(text, text_rect)

                                    # Update the display
                                    pg.display.update()

                                    print(f"Checkmate! {('White', 'Black')[board.white_turn]} wins!")

                                elif board.stalemate:
                                    print("Draw! Stalemate!")
                                # 50 move rule (100 here because we count half rules)
                                elif board.fifty_move > 100:
                                    print("Draw! 50 move rule limit reached!")

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

            #draw board
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
