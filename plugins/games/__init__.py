import discord
import random

from models import UserLanguage
from config import languages
from plugins.mobile import ApplicationView


class GameButton(discord.ui.Button):
  def __init__(self,user,emoji,**kwargs):
    super().__init__(emoji=emoji,**kwargs)
    self.user = user
    self.emoji_=emoji

  async def callback(self, interaction):
    await Game.dispatch(interaction, self.emoji_)


class Page:
  def __init__(self, par):
    self.par,self.msg=par,par.msg
    self.cont=[]
    self.backup=[]

  async def show(self, inter=None, cont=[]):
    self.backup=[]
    self.backup.extend(self.par.children)
    self.par.clear_items()
    for i in (cont or self.cont): self.par.add_item(i)
    meth = (self.msg.edit if not inter else inter.response.edit_message)
    await meth(view=self.par)

class Game(ApplicationView):
  def __init__(self, *args, players, timeout=15.0):
    self.running = False
    self.players = players
    self._childs = []
    self.pages = []
    super().__init__(*args, timeout=timeout, add_back_button=False)

  events = {}

  def create_page(self):
    pg = Page(self)
    self.pages.append(pg)
    return pg

  def add_event(self, emoji, user, handler, *args):
    self.__class__.events[(self.msg.id, emoji, user)] = (handler, args)

  def add_button(self, emoji, user, page=None, **kwargs):
    if not page: meth = self.add_item
    else: meth = page.cont.append
    meth(GameButton(user,emoji=emoji,**kwargs))

  def add_button_event(self,emoji,user,handler,*args,**kwargs):
    self.add_button(emoji,user,**kwargs)
    self.add_event(emoji,user,handler,*args)

  @classmethod
  async def dispatch(cls, payload, emoji):
    container = (payload.message.id, emoji, payload.user.id)
    if container in cls.events.keys():
      (handler, args) = cls.events[container]
      await handler(*args, payload)

  async def update(self, ctx):
    brd = (await self.get_board()) or self.msg.content
    await ctx.respond(content=brd, edit=True, view=self)

  async def get_board(): return ""

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
  def __init__(self, *args, player, timeout=30.0):
    super().__init__(*args[:4], player=[Player(player)], timeout=timeout)
    self.player = player
    self.won = False
    self.lost = False
    self.drew = False

  def win(self): self.end_game();self.won=True;self.players[0].win()
  def lose(self): self.end_game();self.lost=True;self.players[0].lose()
  def draw(self): self.end_game();self.drew=True

  async def interaction_check(self, ctx):
    if ctx.user.id==self.player: return True
    if not ctx.response.is_done(): await ctx.send("You aren't authorised to use this menu!", ephemeral=True)
    return False

  async def get_lang(self):
    lang = await UserLanguage.get_or_none(uid=self.player)
    if lang: return languages.get(lang.language) or languages.english
    return languages.english


class MultiPlayer(Game): pass
class AiPlayer(SinglePlayer, MultiPlayer): pass


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
