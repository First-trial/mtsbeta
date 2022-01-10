# plugin: loadable: True

import appcommands
from core import Cog
from config import languages


class Settings(Cog):
  settings = appcommands.slashgroup(name="settings", description="Settings",guild_ids=[803824283897823253])

  language = settings.subcommandgroup(name="language", description="Language Settings!")

  @language.subcommand(name="view", description="Get Language of your server")
  async def settings_language_view(self, ctx):
    await ctx.send((await ctx.get_lang()).settings.language.view)

  @language.subcommand(name="list", description="Get a list of available languages")
  async def settings_language_list(self, ctx):
    await ctx.send("\n".join(list(languages.languages.keys())))


#   async def settings_language_edit(ctx, language: str):
# Soon™

def setup(bot):
  bot.add_cog(Settings(bot))
