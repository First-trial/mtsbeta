from appcommands import cog
import math

class MathCog(cog.SlashCog):
  def __init__(self, bot):
    self.bot = bot

  @cog.command()
  async def add(self, ctx, number: float, to: float):
    await ctx.reply(f'Your answer is {number + number}', ephemeral=True)
    
  @cog.command()
  async def subtract(self, ctx, by: float, number: float):
    await ctx.reply(f'Your answer is {by - number}', ephemeral=True)

  @cog.command()
  async def multiply(self, ctx, number: float, by: float):
    await ctx.reply(f'Your answer is {number * by}', ephemeral=True)

  @cog.command()
  async def divide(self, ctx, number: float, by: float):
    await ctx.reply(f'Your answer is {number/by}', ephemeral=True)

  @cog.command()
  async def square(self, ctx, number: float):
    await ctx.reply(f'Your answer is {number * number}', ephemeral=True)

  @cog.command()
  async def square_root(self, ctx, number: float):
    await ctx.reply(f'Your answer is {math.sqrt(number)}', ephemeral=True)

def setup(bot):
  bot.add_cog(MathCog(bot))
