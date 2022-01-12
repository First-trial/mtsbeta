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
  def __init__(self, message, *players):
    self.running = False
    self.players = players
    self.msg = message
    super().__init__()

  def add_event(self, emoji, user, handler, *args):
    self.__class__.events[(self.msg.id, emoji, user)] = (handler, *args)

  def add_button(self, emoji,user):
    self.add_item(GameButton(user,emoji=emoji))

  def add_button_event(self,emoji,user,handler,*args):
    self.add_button(emoji,user)
    self.add_event(emoji,user,handler,*args)

  @classmethod
  async def dispatch(cls, payload,emoji):
    container = (payload.message.id, emoji, payload.user.id)
    if container in cls.events.keys():
      (handler, args) = cls.events[container]
      await handler(*args, payload)

  async def start_game(self):
    self.running = True
    for player in self.players: player.play()
    return self

  async def end_game(self):
    self.running = False
    for player in self.players: player.stop()
    self.stop()
    return self
    

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

class SinglePlayer(Game): pass

class AiPlayer(SinglePlayer):
  def __init__(self, player: Player):
    super().__init__(player, Player(ai=True))

class MultiPlayer(Game): pass
  
