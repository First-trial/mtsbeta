from discord import Interaction
from discord.ext import commands
import discord
from plugins.utils import ConfirmV
from config import languages
from models import UserLanguage
from discord.utils import cached_property

class BaseContext:
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.pool = self.bot.pool if hasattr(self, "bot") else self.client.pool
    self._db = None

  @property
  def db(self):
    return self._db if self._db else self.pool

  async def confirm(
    self,
    *args,
    user: discord.User = None,
    switch_color: bool = False,
    language = None,
    **kwargs
  ):
    language = language or (await self.get_lang())
    msg = await self.send(*args, **kwargs)
    view = ConfirmV(
      (user or self.author),
      msg,
      language=language
    )
    if switch_color: view.switch_color()
    await msg.edit(view=view)
    await view.wait()
    confirmed = view.confirmed
    if confirmed is False:
      await msg.edit(
        content = language.plugins.utils.context.err.req_cancel
      )
    return confirmed

  async def get_lang(self):
    sett = await UserLanguage.get_or_none(
      uid=self.author.id
    )
    if sett:
      return languages.get(
        sett.language
      ) or languages.english
    await UserLanguage.create(
      uid=self.author.id
    )
    return languages.get("english")

class Context(BaseContext, commands.Context):
  pass

class InteractionCtx(BaseContext,Interaction):
  def __init__(self, *a, **kw):
    super().__init__(*a, **kw)
    if not self.message:
      self.message = property(self.msg)

  @cached_property
  def bot(self):
    return self.client

  def msg(self):
    return self.interaction._original_message

  @property
  def author(self):
    return self.user

  @property
  def send(self):
    if not self.response.is_done():
      return self.respond

    return self.channel.send

  @property
  def edit(self):
    return self.edit_original_message

  async def respond(self, *args, edit: bool = False, **kwargs):
    meth = self.response.edit_message if edit else self.response.send_message
    await meth(*args, **kwargs)
    return self.message if edit else await self.original_response()

  reply = respond