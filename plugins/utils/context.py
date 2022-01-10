from discord.ext import commands
import asyncio
import discord
import io
from plugins.utils import ConfirmV
from config import languages
from models import GLanguage

class BaseCont:
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def confirm(self, *args, switch_color: bool = False, language = None, **kwargs):
    language=(language) or (await self.get_lang())
    msg = await self.send(*args, **kwargs)
    view = ConfirmV(self.author, msg, language=language)
    if switch_color: view.switch_color()
    await msg.edit(view=view)
    await view.wait()
    confirmed = view.confirmed
    if confirmed is False: await msg.edit(content=language.plugins.utils.context.err.req_cancel)
    return confirmed

  async def get_lang(self):
    ctx = self
    gid=(ctx.guild.id if ctx.guild else ctx.channel.id)

    sett = await GLanguage.get_or_none(gid=gid)
    if sett: return languages.get(sett.language)
    await GLanguage.create(gid=gid)
    return languages.get("english")



class Context(BaseCont, commands.Context):
  def __init__(self,*args, **kwargs):
    super().__init__(*args, **kwargs)
    self.pool = self.bot.pool
    self._db = None

  
  async def entry_to_code(self, entries):
    width = max(len(a) for a, b in entries)
    output = ['```']
    for name, entry in entries:
      output.append(f'{name:<{width}}: {entry}')
    output.append('```')
    await self.send('\n'.join(output))

  async def indented_entry_to_code(self, entries):
    width = max(len(a) for a, b in entries)
    output = ['```']
    for name, entry in entries:
      output.append(f'\u200b{name:>{width}}: {entry}')
    output.append('```')
    await self.send('\n'.join(output))

  def __repr__(self):
    return '<Context>'

  @discord.utils.cached_property
  def replied_reference(self):
    ref = self.message.reference
    if ref and isinstance(ref.resolved, discord.Message):
      return ref.resolved.to_reference()
    return None

  async def disambiguate(self, matches, entry):
    if len(matches) == 0:
      raise ValueError('No results found.')

    if len(matches) == 1:
      return matches[0]

    await self.send(
        'There are too many matches... Which one did you mean? **Only say the number**.'
    )
    await self.send('\n'.join(f'{index}: {entry(item)}'
                              for index, item in enumerate(matches, 1)))

    def check(m):
      return m.content.isdigit(
      ) and m.author.id == self.author.id and m.channel.id == self.channel.id

    await self.release()

    # only give them 3 tries.
    try:
      for i in range(3):
        try:
          message = await self.bot.wait_for('message',
                                            check=check,
                                            timeout=30.0)
        except asyncio.TimeoutError:
          raise ValueError('Took too long. Goodbye.')

        index = int(message.content)
        try:
          return matches[index - 1]
        except:
          await self.send(
              f'Please give me a valid number. {2 - i} tries remaining...'
          )

      raise ValueError('Too many tries. Goodbye.')
    finally:
      pass

  @property
  def db(self):
    return self._db if self._db else self.pool

  async def safe_send(self, content, *, escape_mentions=True, **kwargs):
    """Same as send except with some safe guards.

        1) If the message is too long then it sends a file with the results instead.
        2) If ``escape_mentions`` is ``True`` then it escapes mentions.
        """
    if escape_mentions:
      content = discord.utils.escape_mentions(content)

    if len(content) > 2000:
      fp = io.BytesIO(content.encode())
      kwargs.pop('file', None)
      return await self.send(file=discord.File(
          fp, filename='message_too_long.txt'),
                             **kwargs)
    else:
      return await self.send(content)
