# plugin: loadable: False

import appcommands
from core import Cog


class Settings(Cog):
  settings = appcommands.slashgroup(name="settings", description="Settings")

  language = settings.subcommandgroup(name="language", description="Language Settings!")

  @language.sucommand(name="view", description="Get Language of your server")
  async def settings_language_view(ctx):
    await ctx.send("Your current guild language is `{}`".format(await ctx.get_lang()))

#  async def settings_language_edit(ctx, language: str
