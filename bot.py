from core import MtsBot
import discord
from os import environ as env
import helping
from discord.ext.commands import Cog
from typing import List

shards: List[int] = [0, 1, 2, 3, 4, 5]


import web, asyncio

class misc(Cog):
  def __init__(self, bot):
    self.bot: MtsBot = bot
    self.bot.help_command.cog: Cog = self


async def get_pre(bot: MtsBot, msg):
  if msg.author.id == bot.author_id:
    if msg.content.startswith(("Mts ", "mts ")):
      return ("Mts ", "mts ")
    if bot.get_command(msg.content):
      return ""
    if msg.content.startswith("jsk"):
      return ""

  return ("Mts ", "mts ")


import sblpy

bot = MtsBot(
  command_prefix=get_pre,
  shard_ids=shards,
  shard_count=6,
  help_command=helping.My,
  intents=discord.Intents.all(),
)

bot.add_cog(misc(bot))
sblpy.SBLCog(bot, env.get("sbl_tok"))

es: List[str] = [
    "cogs.anim", "cogs.dbl", "cogs.eco",
    "cogs.newfile", "cogs.snap", "jishaku", "cogs.maths"
]

for e in es:
  bot.load_extension(e)

bot.init()
