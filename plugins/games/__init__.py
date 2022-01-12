import discord


class GameButton(discord.ui.Button):
  def __init__(self,msg,user,*args,**kwargs):
    super().__init__(**kwargs)
    self.handler = handler
    self.args = args

  async def callback(self, interaction):
    await MessageManager.dispatch(interaction, self.emoji)

class MessageManager():
  events = {}
  def __init__(self, message):
    self.msg = message

  async def add_event(self, emoji, user, handler, *args):
    self.__class__.events[(self.msg.id, emoji, user)] = (handler, *args)

  @classmethod
  async def dispatch(cls, payload,emoji):
    container = (payload.message.id, emoji, payload.user.id)
    if container in cls.events.keys():
      (handler, args) = cls.events[container]
      await handler(*args, payload)
    

class Player:
  WON      =  1
  PLAYING  =  0
  LOST     = -1

  def __init__(self, name: str = "ai", ai: bool = False):
    self.name, ai = name, ai
    self.won = False
    self.lose = False
    self.playing = False

  def play(self): self.playing = True; return self
  def stop(self): self.playing = False; return self
  def win(self): self.won,self.lose = True,False; return self
  def lose(self): self.won,self.lose = False, True; return self

class Game:
  def __init__(self, *players):
    self.players = players

  async def start_game(self):
   for player in self.players: player.play()
   return self

  async def end_game(self):
   for player in self.players: player.stop()
    return self

class SinglePlayer(Game): pass

class AiPlayer(SinglePlayer):
  def __init__(self, player: Player):
    super().__init__(player, Player(ai=True))

class MultiPlayer(Game): pass
  
