# plugin: loadable: True

from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import discord,pytz
from datetime import datetime
import os, typing


class Snap(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  @commands.is_owner()
  async def snap(self, ctx, member: discord.Member, *, message):
    colour = {
      "time": (114, 118, 125),
      "content": (220, 221, 222)
   }

    size = {
      "title": 20,
      "time": 13
    }

    font = 'assets/fonts/Whitney-Medium.ttf'

    if not member:
      member = ctx.author

    img = Image.new('RGB', (500, 115), color = (54,57,63))
    titlefnt = ImageFont.truetype(font, size["title"])
    timefnt = ImageFont.truetype(font, size["time"])
    d = ImageDraw.Draw(img)
    txt = member.display_name
    if ctx.guild:
      color = member.color.to_rgb()
    else:
      color = (0,0,0)
    if color == (0, 0, 0):
      color = (255,255,255)
    d.text((90, 20), txt, font=titlefnt, fill=color)
    h, w = d.textsize(txt, font=titlefnt)
    time = datetime.now(tz=pytz.timezone("Asia/Kolkata")).strftime("Today at %I:%M %p")
    d.text((90+h+10, 25), time, font=timefnt, fill=colour["time"])
    d.text((90, 25+w), message, font=titlefnt, fill=colour["content"])

    img.save(f"{member.id}.png")
    if member.avatar.is_animated():
      await member.avatar.save(f"{member.id}p.gif")
      f2 = Image.open(f"{member.id}p.gif")
    else:
      await member.avatar.save(f"{member.id}p.png")
      f2 = Image.open(f"{member.id}p.png")
    f1 = Image.open(f"{member.id}.png")
    f2.thumbnail((50, 55))
    f2.save(f"{member.id}p.png")

    f2 = Image.open(f"{member.id}p.png").convert("RGB")

    mask = Image.new("L", f2.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, f2.size[0], f2.size[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0))

    result = f2.copy()
    result.putalpha(mask)

    result.save(f'{member.id}p.png')

    f2 = Image.open(f"{member.id}p.png")

    f3 = f1.copy()
    f3.paste(f2, (20, 20), f2)
    f3.save(f"{member.id}.png")
    file = discord.File(f"{member.id}.png")

    try:
      try:
        os.remove(f"{member.id}p.gif")
      except:
        pass

      os.remove(f"{member.id}p.png")
      os.remove(f"{member.id}.png")
      try:
        await ctx.send(file=file)
      except:
        pass
    except Exception as e:
      print(e)

async def setup(bot):
  await bot.add_cog(Snap(bot))

