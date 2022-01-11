# plugin: loadable: True

import aiohttp, os, config
import discord
from discord.ext import commands, tasks


class DBL(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.auth = config.top_gg
    self.headers = dict(Authorization=self.auth)
    self.session = aiohttp.ClientSession()
    self.ep = "https://top.gg/api/"
    self.updatestats.start()

  def cog_unload(self):
    if self.session:
      self.bot.loop.run_until_complete(self.session.close())

  @tasks.loop(minutes=30)
  async def updatestats(self):
    """Updates the bot's guild / shard count on top.gg every 30 minutes"""
    await self.bot.wait_until_ready()

    guilds = len(self.bot.guilds)
    shards = None
    if isinstance(self.bot, commands.AutoShardedBot):
      shards = len(self.bot.shards)

    url = "{}bots/{}/stats".format(self.ep, self.bot.user.id)

    data = dict(server_count=guilds)
    if shards:
      data['shard_count'] = shards

    response = await self.session.post(url=url,
                                       headers=self.headers,
                                       data=data)

    if response.status != 200:
      raise Exception(
          "During DBL update loop received code {}: {}".format(
              response.status, response.reason))

  @appcommands.command(description="Check whether you or someone has voted for me or not!")
  async def votecheck(self, ctx, member: discord.Member = None):
    """Checks the voting status of a specified member. Defaults to author."""
    if not member:
      member = ctx.author
    language = (await ctx.get_lang()).dbl.votecheck

    # This is the constructed endpoint for the user check
    url = "{}bots/{}/check".format(self.ep, ctx.me.id)

    # Define our request parameters
    params = dict(userId=member.id)

    # Perform our GET request with the API
    response = await self.session.get(url=url,
                                      headers=self.headers,
                                      params=params)

    if response.status != 200:
      return await ctx.send("Received code {}: {}".format(
          response.status, response.reason))

    data = await response.json()
    voted = bool(data['voted'])
    resp = language.has_not if not voted else language.has

    return await ctx.send(resp.format(user=member.display_name))


def setup(bot):
  bot.add_cog(DBL(bot))
