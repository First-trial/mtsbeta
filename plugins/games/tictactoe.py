import copy
import enum
import math

import discord
from plugins.games import Player, AiPlayer, MultiPlayer, CopyView

class TicTacToeButton(discord.ui.Button['TicTacToe']):
  def __init__(self, x: int, y: int):
    super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=x)
    self.x = y
    self.y = x


  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: TicTacToe = self.view
    state = view.board[self.y][self.x]
    cp,c=view.current_player,None
    is_ai_playing = (view.o.ai)

    if not is_ai_playing:
      gg=view.x if cp==view.X else view.o
    else: gg = view.x

    if f"<@!{interaction.user.id}>" not in (view.x,view.o):
      c="You aren't playing in this match!"
    elif f"<@!{interaction.user.id}>" != gg:
      c="It's not your turn."
    if c:
      return await interaction.response.send_message(c, ephemeral=True)
    if state in (view.X, view.O):
      return

    if view.current_player == view.X:
      self.style = discord.ButtonStyle.danger
      self.label = 'X'
      self.disabled = True
      view.board[self.y][self.x] = view.X
      if is_ai_playing: view.board[self.y][self.x] = GameState.player

      content = "It's {O}\u200b's turn now!"
      if is_ai_playing: content=content.replace("{O}","{X}")
    else:
      self.style = discord.ButtonStyle.success
      self.label = 'O'
      self.disabled = True
      view.board[self.y][self.x] = view.O
      content = "It's {X}\u200b's turn now!"

    if is_ai_playing:
      await interaction.response.edit_message(
        content="Processing...",
        view=CopyView(view, disable=True)
      )
      view.process_turn()
      respond = interaction.edit_original_message
    else: view.switch_player(); respond = interaction.response.edit_message

    winner = view.check_board_winner()
    if winner is not None:
      if winner == view.X:
        content = '{X} Won!'
        view.x.win()
        view.o.lose()
      elif winner == view.O:
        content = '{O} Won!'
        view.o.win()
        view.x.lose()
      else:
        content = "It's a draw!"

      view.end_game()


    await respond(
      content=content.format(X=view.x.name,O=view.o.name),
      view=view
    )


class TicTacToe_Base:
  X = -1
  O = 1
  Tie = 2

  def check_board_winner(self):
    for across in self.board:
      value = sum(across)
      if value == 3:
        return self.O
      elif value == -3:
        return self.X

    # Check vertical
    for line in range(3):
      value = self.board[0][line] + self.board[1][line] + self.board[2][line]
      if value == 3:
        return self.O
      elif value == -3:
        return self.X

    # Check diagonals
    diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
    if diag == 3:
      return self.O
    elif diag == -3:
      return self.X

    diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
    if diag == 3:
      return self.O
    elif diag == -3:
      return self.X

    # If we're here, we need to check if a tie was made
    if all(i != 0 for row in self.board for i in row):
      return self.Tie

    return None

  def switch_player(self):
    if self.current_player==self.X: self.current_player=self.O
    elif self.current_player==self.O: self.current_player=self.X

class TicTacToe(TicTacToe_Base, MultiPlayer):
  def __init__(self, msg, XN, ON):
    x,o = Player(f"<@!{XN}>"), Player(f"<@!{ON}>")
    super().__init__(msg, x, o, timeout=30.0)
    self.current_player = self.X

    self.x = x
    self.o = o

    self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for x in range(3):
      for y in range(3):
        self.add_item(TicTacToeButton(x, y))

  async def interaction_check(self): return True

# Ai

class GameState(enum.IntEnum):
    empty = 0
    player = -1
    ai = +1

class TicTacToe_Ai(TicTacToe_Base, AiPlayer):
  def __init__(self, msg, player):
    super().__init__(msg,Player(f"<@!{player}>"), timeout=30.0)
    self.x,self.o = self.players
    self.current_player = self.X

    self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for x in range(3):
      for y in range(3):
        self.add_item(TicTacToeButton(x, y))

  def determine_possible_positions(self, board: list = None):
    board = board or self.board
    possible_positions = []
    for i in range(3):
      for x in range(3):
        if board[i][x] == GameState.empty: possible_positions.append([i, x])
    return possible_positions

  def min_max(self, board: list, depth: int, player: GameState):
    def determine_win_state(board_, player):
      win_states = [
        [board_[0][0], board_[0][1], board_[0][2]],
        [board_[1][0], board_[1][1], board_[1][2]],
        [board_[2][0], board_[2][1], board_[2][2]],
        [board_[0][0], board_[1][0], board_[2][0]],
        [board_[0][1], board_[1][1], board_[2][1]],
        [board_[0][2], board_[1][2], board_[2][2]],
        [board_[0][0], board_[1][1], board_[2][2]],
        [board_[2][0], board_[1][1], board_[0][2]],
      ]
      return [player, player, player] in win_states

    def evaluate(board_):
      if determine_win_state(board_, GameState.ai):
        score = +1
      elif determine_win_state(board_, GameState.player):
        score = -1
      else:
        score = 0

      return score

    best = [-1, -1, -math.inf]
    if player == GameState.player: best[-1] = +math.inf

    if (
      depth == 0
      or determine_win_state(board, GameState.ai)
      or determine_win_state(board, GameState.player)
    ): return [-1, -1, evaluate(board)]

    for cell in self.determine_possible_positions(board):
      x, y = cell[0], cell[1]
      board[x][y] = player
      score = self.min_max(board, depth - 1, -player)
      board[x][y] = GameState.empty
      score[0], score[1] = x, y
      if player == GameState.ai:
        if score[2] > best[2]:
          best = score
      else:
        if score[2] < best[2]:
          best = score

    return best

  def process_turn(self,):
    if self.check_board_winner(): return
    depth = len(self.determine_possible_positions())
    if depth == 0: return
    move = self.min_max(copy.deepcopy(self.board), depth, GameState.ai)
    row, col = move[0], move[1]
    self.board[row][col] = self.O
    _=[[],[],[]]

    for child in self.children:
      if child.row < 3: _[child.row].append(child)

    button = _[row][col]
    button.label = "O"
    button.disabled = True
    button.style = discord.ButtonStyle.success

  async def interaction_check(self): return True
