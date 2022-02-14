# Logic

import random

from config import Emote


class Logic_2048:
  def __init__(self, size: int = 4, par = None):
    assert par is not None
    self.board = [[0 for _ in range(size)] for _ in range(size)]
    self.size = size
    _={}
    for i in [2,4,8,16,32,64,128,256,512,1024,2048,4096]:_[str(i)]=getattr(Emote,"_2048_"+str(i))
    _["0"]=Emote._2048_empty
    self._conversion = _
    self.has_empty = True
    self.board[random.randrange(4)][random.randrange(4)] = 2
    self.board[random.randrange(4)][random.randrange(4)] = 2
    self.par = par

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
    self.spawn_new()

  def MoveRight(self):
    stage = self.reverse(self.board)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.reverse(stage)
    self.board = stage
    self.spawn_new()

  def MoveUp(self):
    stage = self.transp(self.board)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.transp(stage)
    self.board = stage
    self.spawn_new()

  def MoveDown(self):
    stage = self.transp(self.board)
    stage = self.reverse(stage)
    stage = self.compress(stage)
    stage = self.merge(stage)
    stage = self.compress(stage)
    stage = self.reverse(stage)
    stage = self.transp(stage)
    self.board = stage
    self.spawn_new()

  def spawn_new(self):
    board = self.board
    zeroes = [
      (j, i) for j, sub in enumerate(board) for i, el in enumerate(sub) if el == 0
    ]
    if not zeroes:
      self.has_empty = False
      return

    i, j = random.choice(zeroes)
    board[i][j] = 2
    self.has_empty = True

    if [i for i in self.board if 0 not in i]:
      self.has_empty = False

  def number_to_emoji(self):
    board = self.board
    GameString = ""
    emoji_array = [[self._conversion[str(l)] for l in row] for row in board]
    for row in emoji_array:
      GameString += "".join(row) + "\n"

    return GameString

  def process(self):
    if self.has_empty:
      return

    board = [[b for b in i] for i in self.board]
    restore = lambda: setattr(self,"board",boarf)

    self.MoveUp()
    if self.board != board: return restore()
    self.MoveDown()
    if self.board != board: return restore()
    self.MoveLeft()
    if self.board != board: return restore()
    self.MoveRight()
    if self.board != board: return restore()
    self.par.lost = True

# Game

import discord

from plugins.games import SinglePlayer


class Game_2048(SinglePlayer):
  def __init__(self, size: int = 4, *args):
    super().__init__(*args, timeout=300)
    self.logic, self.lost = Logic_2048(size, self), False
    self.add_item(discord.ui.Button(label="\u200b", disabled=True))
    self.add_button_event(Emote.ARROW_UP, self.player, self.on_up,)
    self.add_item(discord.ui.Button(label="\u200b", disabled=True))
    self.add_button_event(Emote.ARROW_LEFT, self.player, self.on_left,row=2)
    self.add_button_event(Emote.STOP, self.player, self.on_quit,row=2)
    self.add_button_event(Emote.ARROW_RIGHT, self.player, self.on_right,row=2)
    self.add_item(discord.ui.Button(label="\u200b", disabled=True,row=3))
    self.add_button_event(Emote.ARROW_DOWN, self.player, self.on_down,row=3)
    self.add_item(discord.ui.Button(label="\u200b", disabled=True,row=3))

  async def on_up(self,i): self.logic.MoveUp(); self.logic.process(); await self.update(i)
  async def on_left(self,i): self.logic.MoveLeft(); self.logic.process(); await self.update(i)
  async def on_down(self,i): self.logic.MoveDown(); self.logic.process(); await self.update(i)
  async def on_right(self,i): self.logic.MoveRight(); self.logic.process(); await self.update(i)
  async def on_quit(self,i): self.lost=True; await self.update(i)

  async def get_board(self):
    e=discord.Embed(description=self.logic.number_to_emoji(),color=0x00ffff)
    if self.lost:
      lang=(await self.get_lang()).plugins.games
      e.add_field(name="Result", value=f"```\n{lang.lost}```")
      for c in self.children: c.disabled=True
      self.stop()
    return e

  async def start_game(self):
    await self.msg.edit(content=None,embed=discord.Embed(description=self.logic.number_to_emoji(),color=0x00ffff))

  async def update(self, interaction):
    b=await self.get_board()
    try:
      await interaction.response.edit_message(embed=b,view=self)
    except: await self.msg.edit(embed=b,view=self)
