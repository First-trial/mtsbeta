from core import MtsBot
import discord
from os import environ as env
import appcommands
from discoutils import MinimalEmbedHelp as Meh
from discord.ext.commands import Cog

shards = [0, 1, 2, 3, 4, 5]


class Myh(Meh):
	def add_bot_commands_formatting(self, commands, heading):
		if commands:
			joined = ',\u2002'.join("`" + c.name + "`" for c in commands)
			self.paginator.add_line(f'__**{heading}**__')
			self.paginator.add_line(joined)

	def add_subcommand_formatting(self, command):
		fmt = '{0}{1} \N{EN DASH} `{2}`' if command.brief else '{0}{1} \N{EN DASH} `No description`'
		self.paginator.add_line(
		    fmt.format(self.context.clean_prefix, command.qualified_name,
		               command.short_doc))


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

bot = MtsBot(command_prefix=get_pre,
             shard_ids=shards,
             shard_count=6,
             help_command=Myh(color=0x00ffff),
intents=discord.Intents.all(),slashlog=True)
bot.add_cog(misc(bot))
sblpy.SBLCog(bot, env.get("sbl_tok"))


@bot.event
async def on_guild_join(guild):
	print("hi")


es = [
    "cogs.anim", "cogs.dbl", "cogs.eco", "cogs.games", "cogs.ipc",
    "cogs.newfile", "cogs.r", "cogs.ttt", "jishaku"
]
for e in es:
	bot.load_extension(e)

bot.run(env.get("token"))
