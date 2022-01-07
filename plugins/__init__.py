import os


class Plugin(object):
  __slots__ = ("bot","name")
  def __init__(self, name, bot = None):
    self.bot  = bot
    self.name = name[:-3]
    super().__init__()

  __repr__ = lambda self: self.name
  __str__  = lambda self: self.name
  
  def load(self, bot=None):
    if not self.bot and not bot: raise RuntimeError
    if bot: self.bot = bot

    self.bot.load_extension(self.full_name)

  @property
  def full_name(self):
    return self.__class__.__module__ + "." + self.name
    
def all(bot=None):
  for filename in os.listdir("plugins"):
    if filename.endswith(".py") and open("plugins/"+filename, "r").read().splitlines()[0] == "# plugin: loadable: True":
      yield Plugin(filename, bot)
