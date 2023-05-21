import discord
from discord import app_commands, ui, ButtonStyle
from core import Cog
from config import languages, Emote
from models import UserLanguage
from plugins.mobile import ApplicationView

# Note: No language for settings because for people to understand
#       what is written!

class LangView(ApplicationView):
  @ui.select(
    options = [
      discord.SelectOption(
        label = f"{lang.__display__} ({lang.__name__})",
        value = lang.__name__
      ) for lang in languages.all(True)
    ],
    placeholder = "Select a language...",
    row = 0
  )
  async def choose(self, ctx, select):
    if (await self.ctx.get_lang()).__name__ != select.values[0]:
      self.save.disabled = False
      self.save.style = ButtonStyle.green
    else:
      self.save.disabled = True
      self.save.style = ButtonStyle.red

    self.value = select.values[0]
    lang = languages.get(self.value)
    select.placeholder = f"{lang.__display__} ({lang.__name__})"
    await ctx.respond(
      edit = True,
      view = self
    )

  @ui.button(label="Save Changes", style=ButtonStyle.red, disabled=True)
  async def save(self, ctx, button):
    await UserLanguage.edit(
      ctx.user.id,
      self.value
    )
    await LangView.send(self.cog, ctx, self.msg, self.par)

  async def get_embed(self):
    l=await self.ctx.get_lang()
    return discord.Embed(
      title = "Language",
      description = f"`{l.__display__}` (`{l.__name__}`)",
      color = 0x00ffff
    )

class SettView(ApplicationView):
  @ui.button(label="language", style=ButtonStyle.blurple)
  async def language(self, ctx, button):
    await LangView.send(self.cog, ctx, self.msg, self)

  async def get_embed(self):
    e=discord.Embed(title="⚙️ Settings", color=0x00ffff)
    l=await self.ctx.get_lang()
    e.add_field(
      name="Language",
      value=f"`{l.__display__}` (`{l.__name__}`)"
    )
    return e