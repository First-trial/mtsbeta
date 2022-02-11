# plugin: loadable: True

import discord
import appcommands
from core import Cog
from config import languages
from models import UserLanguage


# Note: No language for settings because for people to understand
#       what is written!

class Settings(Cog):
  settings = appcommands.slashgroup(name="settings", description="Settings")

  language = settings.subcommandgroup(name="language", description="Language Settings!")

  @language.subcommand(name="view", description="Get Language of your")
  async def settings_language_view(self, ctx):
    language = await ctx.get_lang()
    await ctx.send(
      f"There is currently `{language.__display__}` (`{language.__name__}`) language for you"
    )

  @language.subcommand(name="list", description="Get a list of available languages")
  async def settings_language_list(self, ctx):
    await ctx.send(embed=discord.Embed(color=0x00ffff,description="\n".join(list(languages.languages.keys()))))

  @language.subcommand(name="edit", description="Edit language of yours")
  async def settings_language_edit(self, ctx, language: str):
    language=language.lower()
    if not languages.get(language): return await ctx.send(f"Language `{language}` not found! (`{ctx.prefix}settings languages list`)", ephemeral=True)
    lang = languages.get(language)
    english = languages.english

    language = await ctx.get_lang()
    if lang is language: return await ctx.send(f"There is already {lang.__name__} for you!", ephemeral=True)
    if await ctx.confirm(f"Are you sure to change language from `{language.__name__}` to `{lang.__name__}`", language=english):
      await UserLanguage.edit(ctx.author.id, lang.__name__)
      await ctx.edit(content=f"You have successfully changed the language from `{language.__name__}` to `{lang.__name__}`")


def setup(bot):
  bot.add_cog(Settings(bot))
