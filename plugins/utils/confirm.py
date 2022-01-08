import discord
from config import Emote, languages


class Button(discord.ui.Button):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.__lattr = self.label
    self.__language = languages.english

  @property
  def language(self):
    return self.__language

  @language.setter
  def language(self, lang):
    self._underlying.label = getattr(lang.plugins.utils.confirm, self.label,)
    self.__language = lang

def button(**kwargs):
  def decor(f):
    f = discord.ui.button(**kwargs)(f)
    f.__discord_ui_model_type__ = Button
    return f
  return decor


class ConfirmV(discord.ui.View):
  def __init__(self, user: discord.User, message: discord.Message, *, timeout: int = 15, language = languages.english):
    super().__init__(timeout=timeout)
    self.confirmed: bool = None # None because to detect whether the user clicked or not clicked
    self.user = user
    self.m = message
    for child in self.children:
      child.language = language


  @button(label='confirm', style=discord.ButtonStyle.green,emoji=Emote.tick)
  async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
    self.confirmed=True
    await interaction.response.edit_message(view=discord.ui.View())


  @button(label='cancel', style=discord.ButtonStyle.danger, emoji=Emote.cross)
  async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
    self.confirmed=False
    await interaction.response.edit_message(view=discord.ui.View())


  async def on_timeout(self):
    if self.confirmed: return

    for child in self.children:
      child.disabled = True

    self.stop()
    await self.m.edit(view=self)

  def switch_color(self):
    for child in self.children:
      child.style = discord.ButtonStyle.green if child.style is discord.ButtonStyle.green else discord.ButtonStyle.danger

  async def interaction_check(self, interaction: discord.Interaction):
    if self.user.id!=interaction.user.id:
      await interaction.response.send_message("You can't confirm it...", ephemeral=True); return False

    return True
