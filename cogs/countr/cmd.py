import discord, json
from discord.ext import commands
from discord.ext.commands import MissingPermissions, BadArgument

class countr(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.group(name="countr", invoke_without_command=True)
  @commands.guild_only()
  async def countr_cmd(self, ctx):
    Mts = ctx.prefix
    cb = ctx.command
    emb = discord.Embed()
    emb.add_field(name=f"{Mts}{cb} abc enable `<#channel>`", value="enables alphabet counting for mentioned channel")
    emb.add_field(name=f"{Mts}{cb} abc disable `<#channel>`", value="disables alphabet for mentioned channel")
    emb.add_field(name="Requirements", value="`administrator` permission")
    await ctx.send(embed=emb)
    
  
  @countr_cmd.group(name="abc", invoke_without_command=True)
  async def abc(self, ctx):
    await ctx.send("kk")
  
  @abc.command(name="disable")
  @commands.has_permissions(administrator=True)
  async def abc_disable(self, ctx, ch: discord.TextChannel=None):
    with open("data/countr/abc.json", "r") as f:
      heli = json.load(f)
      
      
    if ch == None:
      u: discord.TextChannel = ctx.channel
    else:
      u: discord.TextChannel = ch
      
    noad = f"{u.mention} is not added"
      
    if str(u.id) in heli:
      hclic = heli[str(u.id)]
      if hclic == "y":
        
        heli[str(ctx.guild.id)] = {
          
        }
        heli[str(ctx.guild.id)][str(u.id)] = "n"
        
        with open("data/countr/abc.json","w") as f:
          json.dump(heli,f, indent=2)
          
        await ctx.send(f"successfully removed {u.mention}")
      else:
        await ctx.send(noad)
    else:
      await ctx.send(noad)
			
  @abc.command(name="enable")
  @commands.has_permissions(administrator=True)
  async def abc_enable(self, ctx, ch: discord.TextChannel=None):
    with open("data/countr/abc.json", "r") as f:
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
      
    heli[str(ctx.guild.id)] = {
      
    }
    heli[str(ctx.guild.id)][str(u.id)] = "y"
    
    with open("data/countr/abc.json","w") as f:
      json.dump(heli,f, indent=2)
      
    await ctx.send(f"successfully added {u.mention}")
    
  @abc_disable.error
  async def dis_error(self, ctx, exc):
    print(exc)
    if isinstance(exc, MissingPermissions):
      await ctx.send("`Administrator` permission is missing")
      return

    if isinstance(exc, BadArgument):
      await ctx.send("please mention a channel to remove")
      return
      
  @abc_enable.error
  async def en_error(self, ctx, exc):
    print(exc)
    if isinstance(exc, MissingPermissions):
      await ctx.send("`Administrator` permission is missing")
      return

    if isinstance(exc, BadArgument):
      await ctx.send("please mention a channel to add")
      return
    
def setup(bot):
  bot.add_cog(countr(bot))
  