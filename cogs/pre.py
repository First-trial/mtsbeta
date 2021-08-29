import discord
from discord.ext import commands

from core import Cog

class pre(Cog):
  @commands.group(aliases=["pre"],invoke_without_command=True)
  async def prefix(self,ctx):
    await ctx.send("Cmd in development.")
    
  @prefix.group(name="mine",aliases=["user"],invoke_without_command=True)
  async def prefix_mine(self,ctx):
    await ctx.send("Cmd in development.")
    
  @prefix_mine.command(name="add")
  async def prefix_mine_add(self,ctx,*,pre="Mts "):
    await ctx.send("Cmd in development.")
    
  @prefix_mine.command(name="remove")
  async def prefix_mine_remove(self,ctx):
    await ctx.send("Cmd in development.")
    
  @prefix.group(name="server",aliases=["guild"],invoke_without_command=True)
  async def prefix_server(self,ctx):
    await ctx.send("Cmd in development.")
    
  @prefix_server.command(name="add")
  async def prefix_server_add(self,ctx,*,pre="Mts "):
    if self.author_id != ctx.author.id:
      return await ctx.send("Cmd in development.")
    guid=f"'{ctx.guild.id}'"
    typ=f"'user'"
    pre=f"'{pre}'"
    await ctx.db.execute(f"DELETE FROM pre WHERE guid = {guid}")
    await ctx.db.execute(f"INSERT INTO pre (guid, type, prefixes) VALUES ({guid},{typ},{pre})")
    await ctx.send("Hui gwa srkar")
    
  @prefix_server.command(name="remove")
  async def prefix_server_remove(self,ctx):
    await ctx.send("Cmd in development.")
    
def setup(bot):
  bot.add_cog(pre(bot))