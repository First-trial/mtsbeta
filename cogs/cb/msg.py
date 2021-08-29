import discord, json, requests, os
from discord.ext import commands
from urllib.parse import urlencode

class Cb_msg(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, msg):
    with open("data/cb.json", "r")as f:
      hi = json.load(f)
      
    if str(msg.channel.id) in hi:
      if hi[str(msg.channel.id)] == "y":
        pass
      else:
        return
    else:
      return
    
    if msg.author.bot:
      return
    
    message = msg.content
    _1=message[0].capitalize()
    message=_1+message[::-1][:-1][::-1]
    base = os.environ.get("url")
    url = f'{base}{urlencode({"message": message})}'
    r = requests.get(url).json()
    try:
      r = r["response"]
    except:
      r = "Something unexpected happened.\nPlease contact support by `Mts support` or report this bug by `Mts reportbug cb not working`"
    await msg.reply(r, mention_author=False)
  
def setup(bot):
  bot.add_cog(Cb_msg(bot))
  