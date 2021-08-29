"""
A basic cog example for communicating with a verified Discord
bot on top.gg. Feel free to use without restrictions. This example
does NOT use webhooks, which may be necessary for usage on large
bots with over 1000 votes per month. These will be highlighted.

This assumes you already have a bot file with this file being
loaded as a cog.

Uses:
- aiohttp
- discord.py [including ext.tasks]
"""

import aiohttp, os
import discord
from discord.ext import commands, tasks


# This is our cog instance, you can name it however
# you please as long as you redefine the setup function.
class DBL(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		# This is your DBL bot-specific authorization token.
		# Obtained from https://top.gg/api/docs#mybots
		self.auth = os.environ.get("db_aut")

		# Since all requests utilise the same headers,
		# we create a headers variable for ease.
		self.headers = dict(Authorization=self.auth)

		# aiohttp client session used for making requests to the API.
		self.session = aiohttp.ClientSession()

		# The base API endpoint
		self.ep = "https://top.gg/api/"

		# Begin our update loop
		self.updatestats.start()

	# Upon our cog becoming unloaded, we want to make sure
	# we do not leave any unclosed aiohttp client sessions.
	def cog_unload(self):
		if self.session:
			self.bot.loop.run_until_complete(self.session.close())
		#time.sleep(5)

	@tasks.loop(minutes=30)
	async def updatestats(self):
		"""Updates the bot's guild / shard count on top.gg every 30 minutes"""
		# Wait until ready to prevent faulty readings
		await self.bot.wait_until_ready()

		# Collect guild / shard counts
		guilds = len(self.bot.guilds)
		shards = None
		if isinstance(self.bot, commands.AutoShardedBot):
			shards = len(self.bot.shards)

		# This is the constructed endpoint for the user check
		url = "{}bots/{}/stats".format(self.ep, self.bot.user.id)

		# Define our request data
		data = dict(server_count=guilds)
		if shards:
			data['shard_count'] = shards

		# Perform our POST request with the API
		response = await self.session.post(url=url,
		                                   headers=self.headers,
		                                   data=data)

		# If the response is not OK, raise
		if response.status != 200:
			raise Exception(
			    "During DBL update loop received code {}: {}".format(
			        response.status, response.reason))

	@commands.command(aliases=['vote_check'])
	async def votecheck(self, ctx, member: discord.Member = None):
		"""Checks the voting status of a specified member. Defaults to author."""
		if not member:
			member = ctx.author

		# This is the constructed endpoint for the user check
		url = "{}bots/{}/check".format(self.ep, ctx.me.id)

		# Define our request parameters
		params = dict(userId=member.id)

		# Perform our GET request with the API
		response = await self.session.get(url=url,
		                                  headers=self.headers,
		                                  params=params)

		# If the response is not OK, don't continue
		if response.status != 200:
			return await ctx.send("Received code {}: {}".format(
			    response.status, response.reason))

		# Parse True / False from response json
		data = await response.json()
		voted = bool(data['voted'])
		status = 'has' if voted else 'has not'

		# Let the user know
		return await ctx.send("{} {} voted!".format(member.display_name,
		                                            status))


def setup(bot):
	bot.add_cog(DBL(bot))
