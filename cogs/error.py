import discord
from discord.ext import commands
from main import NQNenable as ena, NQNdisable as dis

class error(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @ena.error
  async def ena_error(self, ctx, exc):
    if isinstance(exc, commands.MissingPermissions):
      await ctx.send("You don't have `administrator` perm for this")
      
  @dis.error
  async def dis_error(self, ctx, exc):
    if isinstance(exc, commands.MissingPermissions):
      await ctx.send("You don't have `administrator` perm for this")
      
def setup(bot):
  bot.add_cog(error(bot))
  