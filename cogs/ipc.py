from discord.ext import commands
from core import Cog
import ipc


class Ipc(Cog):
	def __init__(self, bot):
		self.bot = bot

	@ipc.server.route()
	async def get_member_count(self, data):
		guild = self.bot.get_guild(data.guild_id)
		return guild.member_count

	@ipc.server.route()
	async def create_scrim(self, payload):
		return dict()

	@ipc.server.route()
	async def get_server_name(self, data):
		guild = self.bot.get_guild(data.guild_id)
		return str(guild.name)

	@commands.Cog.listener()
	async def on_ipc_error(self, *args, **kwargs):
		print(args)
		print(kwargs)


def setup(bot):
	bot.add_cog(Ipc(bot))
