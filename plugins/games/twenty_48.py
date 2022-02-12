# Logic

import random

from config import Emote


class Logic_2048:
  def __init__(self, size: int = 4):
    self.board = [[0 for _ in range(size)] for _ in range(size)]
    self.size = size
    _={}
    for i in [2,4,8,16,32,64,256,512,1024,2048,4096]:_[str(i)]=getattr(Emote,"2048_"+str(i))

    self._conversion = {"0": Emote.2048_empty,**_}
    self.board[random.randrange(4)][random.randrange(4)] = 2
    self.board[random.randrange(4)][random.randrange(4)] = 2

  def reverse(self, board):
    new_board = []
    for i in range(self.size):
      new_board.append([])
      for j in range(self.size):
        new_board[i].append(board[i][(self.size - 1) - j])

    return new_board

  def transp(self, board):
    new_board = [[0 for _ in range(self.size)] for _ in range(self.size)]
    for i in range(self.size):
      for j in range(self.size):
        new_board[i][j] = board[j][i]
    return new_board

  def merge(self, board):
    for i in range(self.size):
      for j in range(self.size - 1):
        if board[i][j] == board[i][j + 1] and board[i][j] != 0:
          board[i][j] += board[i][j]
          board[i][j + 1] = 0

    return board

  def compress(self, board):
    new_board = [[0 for _ in range(self.size)] for _ in range(self.size)]
    for i in range(self.size):
      pos = 0
      for j in range(self.size):
        if board[i][j] != 0:
          new_board[i][pos] = board[i][j]
          pos += 1

    return new_board

  def MoveLeft(self):
    stage = self.compress(self.board)
    stage = self.merge(stage)
    stage = self.compress(stage)
    self.board = stage

  def MoveRight(self):
    stage = self.reverse(self.board)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.reverse(stage)
    self.board = stage

  def MoveUp(self):
    stage = self.transp(self.board)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.transp(stage)
    self.board = stage

  def MoveDown(self):
    stage = self.transp(self.board)
    stage = self.reverse(stage)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.reverse(stage)
    stage = self.transp(stage)
    self.board = stage

  def spawn_new(self):
    board = self.board
    zeroes = [
      (j, i) for j, sub in enumerate(board) for i, el in enumerate(sub) if el == 0
    ]
    if not zeroes:
      return False

    i, j = random.choice(zeroes)
    board[i][j] = 2
    return True

  def number_to_emoji(self):
    board = self.board
    GameString = ""
    emoji_array = [[self._conversion[str(l)] for l in row] for row in board]
    for row in emoji_array:
      GameString += "".join(row) + "\n"

    return GameString
