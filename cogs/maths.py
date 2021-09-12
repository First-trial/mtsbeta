from appcommands import cog, models
import math
c=[
  models.Choice(name='red'),
  models.Choice(name='green'),
  models.Choice(name='blue')
]

class MathCog(cog.SlashCog):
  def __init__(self, bot):
    self.bot = bot

  @cog.command()
  async def add(self, ctx, firstnumber: float, secondnumber: float):
    await ctx.reply(f'Your answer is {firstnumber + secondnumber}', ephemeral=True)
    
  @cog.command()
  async def subtract(self, ctx, firstnumber: float, secondnumber: float):
    await ctx.reply(f'Your answer is {firstnumber - secondnumber}', ephemeral=True)

  @cog.command()
  async def choose(self, ctx, opt: models.Option(name="thing", choices=c)):
    await ctx.reply(f'You chose {opt}', ephemeral=True)

def setup(bot):
  bot.add_cog(MathCog(bot))
