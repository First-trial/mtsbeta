from core import MtsBot
import discord
from os import environ as env
import appcommands,ristpy as pyrist
# +@ helping @+ Myh
from discord.ext.commands import Cog

shards = [0, 1, 2, 3, 4, 5]


import web, asyncio

class misc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.help_command.cog = self


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
  help_command=helping!.Myh(color=0x00ffff),
  intents=discord.Intents.all(),
  slashlog=True
)
print(Math.floor(45.67))
pprint!.pprint({"h": {"e": "l", "l": "o"}, "w": {"o": "r", "l": "d"}})
bot.add_cog(misc(bot))
sblpy.SBLCog(bot, env.get("sbl_tok"))


@bot.event
async def on_guild_join(guild):
	print("hi")


es = [
    "cogs.anim", "cogs.dbl", "cogs.eco", "cogs.games", "cogs.ipc",
    "cogs.newfile", "cogs.r", "cogs.ttt", "jishaku", "cogs.maths"
]
for e in es:
	bot.load_extension(e)

bot.run(env.get("token"))