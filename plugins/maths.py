# plugin: loadable: True

from core import Cog
import appcommands
import math

class MathCog(Cog):
  def __init__(self, bot):
    self.bot = bot

  math = appcommands.slashgroup(name="math",)
  math_square = math.subcommandgroup(name="sqaure",)

  @math.subcommand(description="Add two numbers")
  async def math_add(self, ctx, number: float, into: float):
    await ctx.reply(f'{number}+{into} = `{number + into}`', ephemeral=True)
    
  @math.subcommand(description="Subtract two numbers")
  async def math_subtract(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}-{by} = `{number - by}`', ephemeral=True)

  @math.subcommand(description="Multiply Two numbers")
  async def math_multiply(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}x{by} = `{number * by}`', ephemeral=True)

  @math.subcommand(description="Divide two numbers")
  async def math_divide(self, ctx, number: float, by: float):
    await ctx.reply(f'{number}/{by} = `{number/by}`', ephemeral=True)

  @math_square.subcommand(name="of", description="Square of a number")
  async def math_square_of(self, ctx, number: float):
    await ctx.reply(f'{number}*{number} = `{number * number}`', ephemeral=True)

  @math_square.subcommand(name="root", description="Square root of a number")
  async def math_square_root(self, ctx, number: float):
    await ctx.reply(f'{number}/{math.sqrt(number)} = `{math.sqrt(number)}`', ephemeral=True)

def setup(bot):
  bot.add_cog(MathCog(bot))
