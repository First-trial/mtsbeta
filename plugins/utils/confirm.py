import discord

class ConfirmV(discord.ui.View):
  def __init__(self, user: discord.User, message: discord.Message):
    super().__init__(timeout=15)
    self.confirmed: bool = None # None because to detect whether the user clicked or not clicked
    self.user = user
    self.m = message


  @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green,emoji=Emote.tick)
  async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
    self.confirmed=True
    await interaction.response.edit_message(view=discord.ui.View())


  @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey,emoji=Emote.cross)
  async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
    self.confirmed=False
    await interaction.response.edit_message(view=discord.ui.View())


  async def on_timeout(self):
    for child in self.children:
      child.disabled = True

    self.stop()
    await self.m.edit(view=self)


  async def interaction_check(self, interaction: discord.Interaction):
    if self.user.id!=interaction.user.id:
      await interaction.response.send_message("You can't confirm it...", ephemeral=True); return False

    return True
