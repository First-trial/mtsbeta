from core import MtsBot
import discord
from os import environ as env
import helping
from discord.ext.commands import Cog
from typing import List
from plugins.utils.context import Context
import appcommands, requests
import plugins

shards: List[int] = [0, 1, 2, 3, 4, 5]

import asyncio

class misc(Cog):
  def __init__(self, bot):
    self.bot: MtsBot = bot
    self.bot.help_command.cog: Cog = self

class Games(Cog):
  pass

async def get_pre(bot: MtsBot, msg):
  if msg.author.id == bot.author_id:
    if msg.content.startswith(("Mts ", "mts ")):
      return ("Mts ", "mts ")
    if bot.get_command(msg.content):
      return ""
    if msg.content.startswith("jsk"):
      return ""

  return ("Mts ", "mts ")


import sblpy, config

bot: MtsBot = MtsBot(
  command_prefix=get_pre,
  shard_ids=shards,
  shard_count=6,
  help_command=helping.My,
  intents=discord.Intents.all(),
)


@bot.command(aliases=["src"])
async def source(ctx: Context):
  await ctx.send(
    "I am open source at https://github.com/First-Trial/mtsbeta",
    delete_after=5
  )

@bot.slashcommand(name="source")
async def source_(ctx: appcommands.InteractionContext):
  await ctx.send(
    "I am open source at https://github.com/First-Trial/mtsbeta",
    ephemeral=True
  )


bot.add_cog(misc(bot))
bot.add_cog(Games(bot))

if requests.get("https://smartbots.tk/").status_code==200: # check whether site's alive or dead
  sblpy.SBLCog(bot, config.sbl) # smartbots.tk


for plugin in plugins.all(bot=bot):
  assert isinstance(plugin, plugins.Plugin)
  plugin.load()

bot.init()
