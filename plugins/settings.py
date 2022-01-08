# plugin: loadable: False

import appcommands
from core import Cog
from config import languages


class Settings(Cog):
  settings = appcommands.slashgroup(name="settings", description="Settings")

  language = settings.subcommandgroup(name="language", description="Language Settings!")

  @language.subcommand(name="view", description="Get Language of your server")
  async def settings_language_view(ctx):
    await ctx.send("Your current server language is `{}`".format(await ctx.get_lang()))

  @language.subcommand(name="list", description="Get a list of available languages")
  async def settings_language_list(ctx):
    await ctx.send("\n".join(languages.all()))


#   async def settings_language_edit(ctx, language: str
