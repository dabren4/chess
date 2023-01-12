"""
This parses FEN representation of game state and creates a board object.

https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation




TODO: 
  1) Implement player to move
  2) Implement if players can castle
  3) Implement if en passant is possible

"""

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "

def parse_fen(string: str):

  board = [['' for _ in range(8)] for _ in range(8)]
  rank, file = 0, 0
  
  for char in string:
    if char == ' ': break
    if char.isdigit():
      file += int(char)
    elif char in 'prnbkqPRNBKQ':
      board[rank][file] = char
    elif char == '/':
      file = -1
      rank += 1
    file += 1
  return board

def board_to_fen(board):
  pass

if __name__ == '__main__':

  board = parse_fen(START)

  for rank in board:
    for square in rank:
      print(f"{square} ", end='')
    print("\n", end='')
