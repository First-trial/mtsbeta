# plugin: loadable: True

from core import Cog
import appcommands
import math

class MathCog(Cog):
  def __init__(self, bot):
    self.bot = bot

  square = appcommands.slashgroup(name="sqaure",)

  @appcommands.command(description="Add two numbers")
  async def add(self, ctx, number: float, into: float):
    await ctx.reply(f'{number}+{into} = `{number + into}`', ephemeral=True)
    
  @appcommands.command(description="Subtract two numbers")
  async def subtract(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}-{by} = `{number - by}`', ephemeral=True)

  @appcommands.command(description="Multiply Two numbers")
  async def multiply(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}x{by} = `{number * by}`', ephemeral=True)

  @appcommands.command(description="Divide two numbers")
  async def divide(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}/{by} = `{number/by}`', ephemeral=True)

  @square.subcommand(name="of", description="Square of a number")
  async def square_of(self, ctx, number: float):
    await ctx.reply(f'{number}*{number} = `{number * number}`', ephemeral=True)

  @square.subcommand(name="root", description="Square root of a number")
  async def square_root(self, ctx, number: float):
    await ctx.reply(f'{number}/{math.sqrt(number)} = `{math.sqrt(number)}`', ephemeral=True)

def setup(bot):
  bot.add_cog(MathCog(bot))
