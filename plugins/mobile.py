# plugin: loadable: True

from discord import app_commands
from discord import ui, ButtonStyle
from core import Cog
import discord
from config import Emote

class ApplicationView(ui.View):
  def __init__(self, cog, ctx, msg, par):
    self.cog = cog
    self.ctx = ctx
    self.msg = msg
    self.par = par
    super().__init__(timeout=30)

  async def on_timeout(self):
    await Mobile.send(self.cog, self.ctx, self.msg)

  @classmethod
  async def send(cls, cog, ctx, msg, par):
    self = cls(cog, ctx, msg, par)
    self.par.stop()
    if ctx.response.is_done():
      return await msg.edit(view=self)
    self.msg = await ctx.respond(
      edit=True,
      embed=await self.get_embed(),
      view=self
    ) or msg

  @ui.button(emoji=Emote.BACK, style=ButtonStyle.blurple)
  async def back(self, ctx, button):
    await self.par.__class__.send(self.cog, ctx, self.msg, self.par.par)

class Mobile(ui.View):
  def __init__(self, cog, ctx, msg,):
    self.cog = cog
    self.ctx = ctx
    self.msg = msg
    self.par = None
    super().__init__(timeout=None)

  @ui.button(emoji="⚙️", style=ButtonStyle.blurple)
  async def settings(self, ctx, button):
    from plugins.settings import SettView
    await SettView.send(self.cog, ctx, self.msg, self)

  @classmethod
  async def send(cls, cog, ctx, msg=None, _=None):
    self = cls(cog, ctx, msg)
    meth = ctx.response.edit_message if msg else ctx.send
    if ctx.response.is_done():
      meth = msg.edit
    self.msg = await meth(
      embed=await self.get_embed(),
      view=self
    ) or msg

  async def get_embed(self):
    return discord.Embed(description="...", color=0x00ffff)

class MobCog(Cog):
  def __init__(self,bot):
    self.bot=bot

  @app_commands.command()
  async def mobile(self, ctx):
    await Mobile.send(self, ctx,)

async def setup(bot):
  await bot.add_cog(MobCog(bot))