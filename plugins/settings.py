# plugin: loadable: True

import discord
import appcommands
from core import Cog
from config import languages
from models import GLanguage


class Settings(Cog):
  settings = appcommands.slashgroup(name="settings", description="Settings",guild_ids=[803824283897823253])

  language = settings.subcommandgroup(name="language", description="Language Settings!")

  @language.subcommand(name="view", description="Get Language of your server")
  async def settings_language_view(self, ctx):
    language = await ctx.get_lang()
    await ctx.send(
      "There is currently `{language.__display__}` (`{language.__name__}`) language in this server"
    )

  @language.subcommand(name="list", description="Get a list of available languages")
  async def settings_language_list(self, ctx):
    await ctx.send(embed=discord.Embed("\n".join(list(languages.languages.keys()))))


  @language.subcommand(name="edit", description="Edit language of current server")
  async def settings_language_edit(self, ctx, language: str):
    if not languages.get(language): return await ctx.send(f"Language {language} not found!", ephemeral=True)
    lang = languages.get(language)
    language = await ctx.get_language()
    if not ctx.guild:
      if await ctx.confirm(f"Are you sure to change language from `{language.__name__}` to `{lang.__name__}`"):
        await GLanguage.edit(ctx.channel.id, lang.__name__)
        await ctx.send(f"You have successfully changed the language from `{language.__name__}` to `{lang.__name__}`")
      return

    await ctx.send("Soon™", ephemeral=True)


def setup(bot):
  bot.add_cog(Settings(bot))
