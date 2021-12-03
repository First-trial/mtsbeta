import discord, config
from discord.ext import commands
from discord import Permissions
from tortoise import Tortoise
from core.cmd import Command
from cogs.utils import context
from core.private import DISCORD
from core.msgmanager import MessageManager
from core.dbmanager import DatabaseManager
import importlib

from discord.ext.commands import CommandNotFound
import inspect, os, time, traceback
from core.gmemanager import GameManager
import appcommands
MAX_MESSAGE_LENGTH = 1900
import asyncio

from core.generic import Scheduler


नन = None

class CustomCont(appcommands.InteractionContext):
  def __init__(self, b, i):
    super().__init__(b,i)
    self.db = self.pool = b.pool
    self.prefix = self.clean_prefix = "/"

class यूजर(discord.ClientUser):
  __डाटा={"आईडी": "id", "नाम": "name","नेम": "name","डिस्क्रिमिनेटर": "discriminator"}
  __slots__=tuple([*["टैग"], *[k for k in __डाटा.keys()]])

  @classmethod
  def इनिट(क्लास, बोट) -> "यूजर":
    सेल्फ = क्लास(
      state=बोट._connection,
      data={"username": बोट.user.name,"id": बोट.user.id,"discriminator": बोट.user.discriminator,"bot": True,"avatar": None}
    )
    for k,v in सेल्फ.__डाटा.items():
      setattr(सेल्फ,k, getattr (सेल्फ,v))

    सेल्फ.टैग = सेल्फ.नेम+"#"+सेल्फ.डिस्क्रिमिनेटर

    return सेल्फ

  def __repr__(सेल्फ):
    return f"<Mtsबोट आईडी={सेल्फ.आईडी} नेम='{सेल्फ.नेम}' डिस्क्रिमिनेटर='{सेल्फ.डिस्क्रिमिनेटर}'>"

class MtsBot(appcommands.AutoShardedBot):
  def __init__(सेल्फ, *args, **kwargs):
    super().__init__(**kwargs)
    DatabaseManager.on_startup(सेल्फ)
    MessageManager.on_startup(सेल्फ)
    Lexicon.on_startup()
    सेल्फ.game_manager = GameManager()
    सेल्फ.scheduler = Scheduler()
    सेल्फ.ready = False
    सेल्फ._author = नन
    सेल्फ.यूजर = नन

  def get_interaction_context(self, interaction):
    return CustomCont(self, interaction)

  async def process_commands(self, message):
    ctx = await self.get_context(message, cls=context.Context)
    if message.author.bot:
      return
    try:
      await self.invoke(ctx)
    finally:
      await ctx.release()

  def init(सेल्फ, *args, **kwargs):
    सेल्फ.loop.run_until_complete(सेल्फ._init())
    सेल्फ.load_commands()
    import hoster
    hoster.host(सेल्फ, os.environ.get("token"))

  @property
  def discord(सेल्फ):
    return "https://discord.gg/zdrSUu98BP"

  @property
  def guild(सेल्फ):
    return सेल्फ.get_guild(731072681688039444)

  @property
  def author_id(सेल्फ):
    return 730454267533459568

  async def _init(सेल्फ):
    await Tortoise.init(config=config.tortoise)
    await Tortoise.generate_schemas(safe=True)


  async def on_connect(सेल्फ):
    सेल्फ.यूजर = यूजर.इनिट(सेल्फ)

  async def on_ready(सेल्फ):
    सेल्फ._author = await सेल्फ.fetch_user(सेल्फ.author_id)

  @property
  def pool(सेल्फ):
    try:
      return Tortoise.get_connection("default")._pool
    except:
      return None

  @property
  def author(सेल्फ):
    return सेल्फ._author

  def get_modules(self, path, module):
    modules = []
    for file in os.listdir(path):
      if file == "__pycache__":
        continue
      if os.path.isdir(os.path.join(path, file)):
        for submodule in self.get_modules(os.path.join(path, file), f"{module}.{file}"):
          modules.append(submodule)
      elif os.path.isfile(os.path.join(path, file)):
        modules.append(f"{module}.{file[:-3]}")

    return modules

  def load_commands(self):
    modules = self.get_modules(os.path.join(os.getcwd(), "cmds"), "cmds")
    self.my_commands = []
    for module in modules:
      imp = importlib.import_module(module)
      for key, cmd in imp.__dict__.items():
        if inspect.isclass(cmd) and issubclass(cmd, Command) and cmd != Command:
          self.my_commands.append(cmd)
          cmd.add_command(self)

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

  async def on_raw_reaction_add(self, payload):
    await MessageManager.on_raw_reaction(payload)

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
    channel = self.get_channel(DISCORD["ERROR_CHANNEL"])
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

  async def routine_updates(self):
    while True:
      await DatabaseManager.update()
      self.remove_old_binaries()
      await asyncio.sleep(60 * 30)

  async def on_restart(self):
    await self.game_manager.on_restart()
    await DatabaseManager.update()

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

  def remove_old_binaries(self):
    direc = os.path.join(os.getcwd(), 'bin')
    now = time.time()
    dt = now - 60 * 60 * 24
    for filename in os.listdir(direc):
      f_path = os.path.join(direc, filename)
      f_created = os.path.getctime(f_path)
      if (filename.endswith(".svg") or filename.endswith(".png")) and f_created < dt:
        os.remove(f_path)

from appcommands import Cog as _Cog
class Cog(_Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = self.bot.pool
    self.author_id = self.bot.author_id

  @property
  def author(self):
    return self.bot.author


from abc import ABC, abstractmethod


class Minigame(ABC):
  @abstractmethod
  def has_won(self):
    raise NotImplementedError

  @abstractmethod
  def has_drawn(self):
    raise NotImplementedError

  @abstractmethod
  def has_lost(self):
    raise NotImplementedError


import json
import random


class Lexicon:
  QUESTIONS = dict()
  WORDS = []

  @classmethod
  def on_startup(cls):
    f = open('assets/questions.json')
    cls.QUESTIONS = json.loads(f.read())
    f.close()

    with open("assets/10k words.txt") as f:
      cls.WORDS = f.readlines()
      f.close()

  @classmethod
  def get_random_word(cls):
    word = cls.WORDS[random.randint(0, len(cls.WORDS) - 1)].rstrip()
    while len(word) < 5:
      word = cls.WORDS[random.randint(0, len(cls.WORDS) - 1)].rstrip()
      return word


class DiscordMinigame(ABC):
  @abstractmethod
  async def start_game(self):
    pass

  @abstractmethod
  async def end_game(self):
    pass

  @abstractmethod
  async def on_player_timed_out(self):
    pass

  @abstractmethod
  def on_start_move(self):
    pass

  @abstractmethod
  def on_end_move(self):
    pass

  @abstractmethod
  def get_board(self):
    pass

  @abstractmethod
  def update_last_seen(self):
    pass

  @abstractmethod
  def clear_reactions(self):
    pass
