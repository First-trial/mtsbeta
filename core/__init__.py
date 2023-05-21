import discord, config
from discord.ext import commands
from discord import Permissions
from tortoise import Tortoise
import importlib

from discord.ext.commands import CommandNotFound
import inspect, os, time, traceback
MAX_MESSAGE_LENGTH = 1900
import asyncio

from .state import State
from .context import Context

class MtsBot(commands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.ready = False
    self._author = None
    self._BotBase__cogs = commands.core._CaseInsensitiveDict()


  async def setup_hook(self):
    await self.tree.sync()
    await Tortoise.init(config=config.tortoise)
    await Tortoise.generate_schemas(safe=True)

  async def process_commands(self, message):
    ctx = await self.get_context(message, cls=Context)
    if message.author.bot:
      return
    try:
      await self.invoke(ctx)
    finally:
      pass

  def init(self, *args, **kwargs):
    import hoster
    hoster.host(self, config.token)

  @property
  def discord(self):
    return config.DISCORD_JOIN_URL

  @property
  def economy(self):
    return self.get_cog("economy")

  @property
  def guild(self):
    return self.get_guild(self.guild_id)

  @property
  def author_id(self):
    return config.AUTHOR_ID

  @property
  def guild_id(self):
    return config.DISCORD_GUILD_ID


  async def on_ready(self):
    await asyncio.sleep(2) # wait for bot to detect all useful data
    await config.generate(self)
    self._author = await self.fetch_user(self.author_id)
    print(self.user, " started!")

  @property
  def pool(self):
    try:
      return Tortoise.get_connection("default")._pool
    except:
      return None

  @property
  def author(self):
    return self._author

  def _get_state(self, **options):
    return State(
      dispatch=self.dispatch,
      handlers=self._handlers,
      hooks=self._hooks,
      http=self.http,
      **options
    )

from discord.ext.commands import Cog as _Cog

class Cog(_Cog):
  def __init__(self, bot):
    self.bot = bot

  @property
  def db(self): return self.bot.pool

  @property
  def author_id(self): return self.bot.author_id

  @property
  def author(self): return self.bot.author
