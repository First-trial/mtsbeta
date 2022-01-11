import discord, config
from discord.ext import commands
from discord import Permissions
from tortoise import Tortoise
from plugins.utils import context
import importlib

from discord.ext.commands import CommandNotFound
import inspect, os, time, traceback
import appcommands
MAX_MESSAGE_LENGTH = 1900
import asyncio


class CustomCont(context.BaseCont, appcommands.InteractionContext):
  def __init__(self, b, i):
    super().__init__(b,i)
    self.db = self.pool = b.pool
    self.prefix = self.clean_prefix = "/"

  def respond(self,*a,**kw):
    self.message = super().respond(*a,**kw)
    return self.message

class MtsBot(appcommands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.scheduler = Scheduler()
    self.ready = False
    self._author = None
    self._BotBase__cogs = commands.core._CaseInsensitiveDict()

  def get_interaction_context(self, interaction):
    return CustomCont(self, interaction)

  async def process_commands(self, message):
    ctx = await self.get_context(message, cls=context.Context)
    if message.author.bot:
      return
    try:
      await self.invoke(ctx)
    finally:
      pass

  def init(self, *args, **kwargs):
    self.loop.run_until_complete(self._init())
    import hoster
    hoster.host(self, config.token)

  @property
  def discord(self):
    return config.DISCORD_JOIN_URL

  @property
  def guild(self):
    return self.get_guild(self.guild_id)

  @property
  def author_id(self):
    return config.AUTHOR_ID

  @property
  def guild_id(self):
    return config.DISCORD_GUILD_ID

  async def _init(self):
    await Tortoise.init(config=config.tortoise)
    await Tortoise.generate_schemas(safe=True)

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

  def get_missing_permissions(self, context):
    permissions: Permissions = context.channel.permissions_for(
      context.channel.guild.me
    )
    missing_permissions = list()
    if not permissions.manage_messages:
      missing_permissions.append("Manage messages")
    if not permissions.read_message_history:
      missing_permissions.append("Add reactions")
    if not permissions.use_external_emojis:
      missing_permissions.append("Use external emojis")
    if not permissions.attach_files:
      missing_permissions.append("Attach files")
    return missing_permissions

  async def send_missing_permissions(self, context, missing_permissions):
    if len(missing_permissions) == 0:
      return
    content = "I am missing the following permissions in this channel. Please enable these so the bot can work properly:\n"
    for missing_permission in missing_permissions:
      content += f"- {missing_permission}\n"
    await context.send(content)

  async def send(self, content, channel_id=None):
    if content.startswith("```"):
      await self.send_formatted(content, channel_id)
      return
    max_length = 1900
    message_length = len(content)
    j = 0

    if channel_id is not None:
      channel = await self.fetch_channel(channel_id)
    else:
      channel = self.ctx.channel

    while max_length < message_length:
      await channel.send(content[j * max_length:(j + 1) * max_length])
      message_length -= max_length
      j += 1

    await channel.send(content[j * max_length:])

  async def send_formatted(self, content, channel_id=None):
    message_length = len(content)
    j = 0
    content = content[3:-3]

    if channel_id is not None:
      channel = await self.fetch_channel(channel_id)
    else:
      channel = self.ctx.channel

    while MAX_MESSAGE_LENGTH < message_length:
      await channel.send("```\n" + content[j * MAX_MESSAGE_LENGTH:(j + 1) * MAX_MESSAGE_LENGTH] + "\n```")
      message_length -= MAX_MESSAGE_LENGTH
      j += 1

    await channel.send("```\n" + content[j * MAX_MESSAGE_LENGTH:] + "\n```")

  async def send_error(self, content):
    channel = self.get_channel(config.ERROR_LOG_CHANNEL)
    contents = content.split("\n")
    content = ""
    for part in contents:
      temp = content + "\n" + part
      if len(temp) > MAX_MESSAGE_LENGTH:
        await channel.send("```\n" + content + "\n```")
        content = part
      else:
        content = temp
    await channel.send("```\n" + content + "\n```")

  async def on_error(self, event_method, *args, **kwargs):
    error = "Time: {0}\n\nIgnoring exception in command {1}:\n\nargs: {2}\n\n" \
            "kwargs: {3}\n\n" \
            "e: {4}\n\n" \
            .format(time.strftime("%b %d %Y %H:%M:%S"), event_method, args, kwargs, traceback.format_exc())
    await self.send_error(error)

  async def on_command_error(self, context, exception):
    if isinstance(exception, CommandNotFound):
      return
    if self.extra_events.get('on_command_error', None):
      return
    if hasattr(context.command, 'on_error'):
      return
    if isinstance(exception, commands.errors.MemberNotFound):
      return await context.reply("Try that command again and this time, with a real user!")
    cog = context.cog
    if cog and Cog._get_overridden_method(cog.cog_command_error) is not None:
      return

    original_error = getattr(exception, 'original', exception)
    if isinstance(original_error, discord.Forbidden):
      await self.send_missing_permissions(context, self.get_missing_permissions(context))
      error = "Time: {0}\n\nIgnoring exception in command {1}:\n\nException: \n\n{2}"\
      .format(time.strftime("%b %d %Y %H:%M:%S"), context.command, ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))
      await self.send_error(error)

from appcommands import Cog as _Cog

class Cog(_Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = self.bot.pool
    self.author_id = self.bot.author_id

  @property
  def author(self):
    return self.bot.author
