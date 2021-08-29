import discord, json
from discord.ext import commands
from discord.ext.commands import MissingPermissions, BadArgument

class CB(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.group(aliases=["Cb", "CB","cB"], name="cb", invoke_without_command=True)
  async def cb(self, ctx):
    emb = discord.Embed()
    emb.add_field(name="Mts cb enable `<#channel>`", value="enables chatbot in the mentioned channel")
    emb.add_field(name="Mts cb disable `<#channel>`", value="disables chatbot in the mentioned channel")
    emb.add_field(name="Requirements", value="`administrator` permission")
    await ctx.send(embed=emb)
    
  @cb.command(name="disable")
  @commands.has_permissions(administrator=True)
  async def disable(self, ctx, ch: discord.TextChannel=None):
    with open("data/cb.json", "r") as f:
      heli = json.load(f)
      
      
    if ch == None:
      u: discord.TextChannel = ctx.channel
    else:
      u: discord.TextChannel = ch
      
    noad = f"{u.mention} is not added"
      
    if str(u.id) in heli:
      hclic = heli[str(u.id)]
      if hclic == "y":
        
        heli[str(u.id)] = "n"
        
        with open("data/cb.json","w") as f:
          json.dump(heli,f, indent=2)
          
        await ctx.send(f"successfully removed {u.mention}")
      else:
        await ctx.send(noad)
    else:
      await ctx.send(noad)
			
  @cb.command(name="enable")
  @commands.has_permissions(administrator=True)
  async def enable(self, ctx, ch: discord.TextChannel=None):
    with open("data/cb.json", "r") as f:
      heli = json.load(f)
      
      
    if ch == None:
      u: discord.TextChannel = ctx.channel
    else:
      u: discord.TextChannel = ch
      
    noad = f"{u.mention} is already added"
    
    if str(u.id) in heli:
      hclic = heli[str(u.id)]
      if hclic == "y":
        await ctx.send(noad)
        return
      else:
        pass
    else:
      pass
      
    heli[str(u.id)] = "y"
    
    with open("data/cb.json","w") as f:
      json.dump(heli,f, indent=2)
      
    await ctx.send(f"successfully added {u.mention}")
    
  @disable.error
  async def dis_error(self, ctx, exc):
    print(exc)
    if isinstance(exc, MissingPermissions):
      await ctx.send("you don't have `Administrator` permission for this")
      return

    if isinstance(exc, BadArgument):
      await ctx.send("please mention a channel to remove")
      return
      
  @enable.error
  async def en_error(self, ctx, exc):
    print(exc)
    if isinstance(exc, MissingPermissions):
      await ctx.send("you don't have `Administrator` permission for this")
      return

    if isinstance(exc, BadArgument):
      await ctx.send("please mention a channel to add")
      return
    
def setup(bot):
  bot.add_cog(CB(bot))
  