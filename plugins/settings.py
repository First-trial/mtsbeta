# plugin: loadable: True

import discord
import appcommands
from core import Cog
from config import languages


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


#   async def settings_language_edit(ctx, language: str):
# Soon™

def setup(bot):
  bot.add_cog(Settings(bot))
