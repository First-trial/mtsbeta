import discord


class GameButton(discord.ui.Button):
  def __init__(self,user,**kwargs):
    super().__init__(**kwargs)
    self.user = user

  async def callback(self, interaction):
    await MessageManager.dispatch(interaction, self.emoji)

  async def interaction_check(self, interaction):
    if interaction.user.id==self.user.id: return True
    await interaction.response.send_message("You aren't authorised to use this menu!", ephemeral=True)
    return False


class Game(discord.ui.View):
  events = {}
  def __init__(self, message, *players, timeout=15.0):
    self.running = False
    self.players = players
    self._child = []
    self.msg = message
    super().__init__(timeout=timeou)

  async def on_timeout(self):
    self.end_game()
    await self.msg.edit(view=self)

  def add_event(self, emoji, user, handler, *args):
    self.__class__.events[(self.msg.id, emoji, user)] = (handler, *args)

  def add_button(self, emoji,user,**kwargs):
    self.add_item(GameButton(user,emoji=emoji,**kwargs))

  def add_button_event(self,emoji,user,handler,*args,**kwargs):
    self.add_button(emoji,user)
    self.add_event(emoji,user,handler,*args,**kwargs)

  @classmethod
  async def dispatch(cls, payload,emoji):
    container = (payload.message.id, emoji, payload.user.id)
    if container in cls.events.keys():
      (handler, args) = cls.events[container]
      await handler(*args, payload)

  def start_game(self):
    self.running = True
    for player in self.players: player.play();player.game=self
    for child in self._childs: self.children.append(child)
    return self

  def end_game(self):
    self.running = False
    for player in self.players: player.stop();player.game=None
    for child in self.children: child.disabled = True
    self.stop()
    return self

  def add_item(self, item): self._child.append(item)

class Player:
  WON      =  1
  PLAYING  =  0
  LOST     = -1

  def __init__(self, name: str = "ai", ai: bool = False):
    self.name, ai = name, ai
    self.won = False
    self.lose = False
    self.playing = False
    self.game = None

  def play(self): self.playing = True; return self
  def stop(self): self.playing = False; return self
  def win(self): self.won,self.lose = True,False; return self
  def lose(self): self.won,self.lose = False, True; return self

  __eq__ = (lambda self, other: other==self.name)
  __ne__ = (lambda self, other: not self.__eq__(other))

  __repr__ = __str__ = (lambda self: self.name)

class SinglePlayer(Game): pass

class AiPlayer(SinglePlayer):
  def __init__(self, msg, player: Player, timeout=15.0):
    super().__init__(msg, player, Player(ai=True), timeout=timeout)

class MultiPlayer(Game): pass
  
