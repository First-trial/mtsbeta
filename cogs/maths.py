from appcommands import cog
import math

class MathCog(cog.SlashCog):
  def __init__(self, bot):
    self.bot = bot

  @cog.command()
  async def add(self,ctx):
    pass
