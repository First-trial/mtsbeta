import os


class Plugin(str):
  def __init__(self, name, /, *, bot=None):
    self.bot = bot
    self.name = name
    super().__init__(name)


  def load(self, bot=None):
    if not self.bot and not bot: raise RuntimeError
    if bot: self.bot = bot

    self.bot.load_extension(self)


def all(bot=None):
  for filename in os.listdir("."):
    if filename.endswith(".py") and open(filename, "r").read().splitlines()[0] == "# plugin: loadable: True":
      yield Plugin(filename, bot=bot)
