import enum

from discord import ButtonStyle
from plugins.games import Player, AiGame, MultiPlayer

class TicTacToeButton(discord.ui.Button['TicTacToe']):
  def __init__(self, x: int, y: int):
    super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
    self.x = x
    self.y = y


  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: TicTacToe = self.view
    state = view.board[self.y][self.x]
    cp,c=view.current_player,None
    gg=view.x if cp==view.X else view.o
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
      content = "It's {O}\u200b's turn now!"
    else:
      self.style = discord.ButtonStyle.success
      self.label = 'O'
      self.disabled = True
      view.board[self.y][self.x] = view.O
      content = "It's {X}\u200b's turn now!"

    view.switch_player()

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


    await interaction.response.edit_message(
      content=content.format(X=view.x.name,O=view.o.name),
      view=view
    )


class TicTacToe(MultiPlayer):
  children: List[TicTacToeButton]
  X = -1
  O = 1
  Tie = 2

  def __init__(self, msg, XN, ON):
    x,o = Player(f"<@!{XN}>"), Player(f"<@!{ON}>")
    super().__init__(msg, x, o)
    self.current_player = self.X

    self.x = x
    self.o = o

    self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for x in range(3):
      for y in range(3):
        self.add_item(TicTacToeButton(x, y))

  def switch_player(self):
    if self.current_player==self.X: self.current_player=self.O
    elif self.current_player==self.O: self.current_player=self.X

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

