from appcommands import cog
import math

class MathCog(cog.SlashCog):
  def __init__(self, bot):
    self.bot = bot

  @cog.command()
  async def add(self, ctx, firstnumber: float, secondnumber: float):
    await ctx.reply(f'Your answer is {firstnumber + secondnumber}', ephemeral=True)
    
  @cog.command()
  async def subtract(self, ctx, firstnumber: float, secondnumber: float):
    await ctx.reply(f'Your answer is {firstnumber - secondnumber}', ephemeral=True)
