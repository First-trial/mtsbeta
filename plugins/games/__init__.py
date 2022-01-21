import discord
import random


class GameButton(discord.ui.Button):
  def __init__(self,user,emoji,**kwargs):
    super().__init__(emoji=emoji,**kwargs)
    self.user = user
    self.emoji_=emoji

  async def callback(self, interaction):
    await _GBase.dispatch(interaction, self.emoji_)

class _GBase(discord.ui.View):
  events = {}
  def add_event(self, emoji, user, handler, *args):
    self.__class__.events[(self.msg.id, emoji, user)] = (handler, args)

  def add_button(self, emoji,user,**kwargs):
    self.add_item(GameButton(user,emoji=emoji,**kwargs))

  def add_button_event(self,emoji,user,handler,*args,**kwargs):
    self.add_button(emoji,user,**kwargs)
    self.add_event(emoji,user,handler,*args)

  @classmethod
  async def dispatch(cls, payload,emoji):
    container = (payload.message.id, emoji, payload.user.id)
    if container in cls.events.keys():
      (handler, args) = cls.events[container]
      await handler(*args, payload)

  async def update(self, inter):
    brd = self.get_board() or self.msg.content
    await interaction.response.edit_message(content=brd,view=self)

  def get_board(): return ""

class ElfView(_GBase):
  def __init__(message, parent, **kw):
    super().__init__(**kw)
    self.parent = parent
    self.msg = message

  async def fully_end(self):
    for child in self.children: child.disabled = True
    self.stop()
    await self.msg.edit(view=self)

class Game(_GBase):
  def __init__(self, message, *players, timeout=15.0):
    self.running = False
    self.players = players
    self._childs = []
    self.msg = message
    self.elf = None
    super().__init__(timeout=timeout)

  async def create_elf(self, msg):
    self.elf = ElfView(msg, self, timeout=self.timeout)
    return self.elf

  async def on_timeout(self):
    self.end_game()
    if self.elf: await self.fully_end()
    await self.msg.edit(view=self)

  async def start(self):
    self.running = True
    for player in self.players: player.play();player.game=self
    for child in self._childs: super().add_item(child)
    await self.msg.edit(view=self)
    await self.start_game()
    return self

  async def start_game(self): pass

  def end_game(self):
    self.running = False
    for player in self.players: player.stop();player.game=None
    for child in self.children: child.disabled = True
    self.stop()
    return self

  def add_item(self, item):
    if not self.running: self._childs.append(item)
    else: super().add_item(item)

  def __await__(self):
    async def _(): return self
    return _().__await__()

  def __call__(self): return self


class LogicBase:
  def __await__(self):
    async def _(): return self
    return _().__await__()

  def __call__(self): return self

  def get_random_word(self): return random.choice(" ".join(open("assets/words.txt").read().splitlines()).split(" "))


class Player:
  WON      =  1
  PLAYING  =  0
  LOST     = -1

  def __init__(self, name: str = "ai", ai: bool = False):
    self.name, self.ai = name, ai
    self.won = False
    self.lost = False
    self.playing = False
    self.game = None

  def play(self): self.playing = True; return self
  def stop(self): self.playing = False; return self
  def win(self): self.won,self.lost = True,False; return self
  def lose(self): self.won,self.lost = False, True; return self

  __eq__ = (lambda self, other: other==self.name)
  __ne__ = (lambda self, other: not self.__eq__(other))

  __repr__ = __str__ = (lambda self: self.name)

class SinglePlayer(Game):
  def __init__(self, m, p, timeout=30.0):
    super().__init__(m, Player(p), timeout=timeout)
    self.player = self.players[0]
    self.player.id = p
    self.won = False
    self.lost = False
    self.drew = False

  def win(self): self.end_game();self.won=True;self.player.win()
  def lose(self): self.end_game();self.lost=True;self.player.lose()
  def draw(self): self.end_game();self.drew=True
    
class AiPlayer(Game):
  def __init__(self, msg, player: Player, timeout=30.0):
    super().__init__(msg, player, Player(ai=True), timeout=timeout)

class MultiPlayer(Game): pass


# Utils


def CopyView(view, disable: bool = False):
  v = discord.ui.View()
  for child in view.children:
    v.add_item(
      discord.ui.Button(
        label=child.label,
        emoji=child.emoji,
        url=child.url,
        disabled=disable or child.disabled,
        custom_id=child.custom_id,
        style=child.style,
        row=child.row
      )
    )

  return v
