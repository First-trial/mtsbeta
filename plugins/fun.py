# plugin: loadable: True

import discord
import asyncio
from discord.ext import commands
import appcommands
from core import Cog

class Fun(Cog):
  fun = appcommands.slashgroup(name="fun", description="Fun Commands!")

  animation = fun.subcommandgroup(name="animation", description="Animation Commands!")

  @animation.subcommand(name="cathi", description="Make a cat say something")
  async def cathi(self, ctx, text: str = "Hi..."):
    ctx=await ctx.reply("starting")
    list = (
        """ຸ 　　　＿＿_＿＿
　　／　／　  ／|"
　　|￣￣￣￣|　|
　　|　　　　|／
　　￣￣￣￣""",
        f"""ຸ 　　　{text}
 　   　 ∧＿∧＿_
　　／(´･ω･`)  ／＼
　／|￣￣￣￣|＼／
　　|　　　　|／
　　￣￣￣￣""",
    )
    for i in range(3):
      for cat in list:
        await ctx.edit(content=cat)
        await asyncio.sleep(1)
        

  @animation.subcommand(name="flop", description="...")
  async def flop(self, ctx):
    m = await ctx.send("Starting...")
    list = (
        "(   ° - °) (' - '   )",
        "(\\\° - °)\ (' - '   )",
        "(—°□°)— (' - '   )",
        "(╯°□°)╯(' - '   )",
        "(╯°□°)╯︵(\\\ .o.)\\",
    )
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(1.5)

  @animation.subcommand(name="poof", description="...")
  async def poof(self, ctx):
    m = await ctx.send("...")
    list = ("(   ' - ')", "' - ')", "- ')", "')", ")", "*poofness*")
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(1.5)

  @animation.subcommand(name="virus", description="Insert a virus to yourself or someone else")
  async def virus(self, ctx, user: discord.Member = None, virus: str = "trojan"):
    m = await ctx.send("...")
    user = user or ctx.author
    list = (
        f"`[▓▓▓                    ] / {virus}-virus.exe Packing files.`",
        f"`[▓▓▓▓▓▓▓                ] - {virus}-virus.exe Packing files..`",
        f"`[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {virus}-virus.exe Packing files..`",
        f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {virus}-virus.exe Packing files..`",
        f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {virus}-virus.exe Packing files..`",
        f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {virus}-virus.exe Packing files..`",
        f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {virus}-virus.exe Packing files..`",
        f"`Successfully downloaded {virus}-virus.exe`",
        "`Injecting virus.   |`",
        "`Injecting virus..  /`",
        "`Injecting virus... -`",
        f"`Successfully Injected {virus}-virus.exe into {user.name}`",
    )
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(0.8)

  @animation.subcommand(name="boom", description="Booms a message!")
  async def boom(self, ctx):
    m = await ctx.send("THIS MESSAGE WILL SELFDESTRUCT IN 5")
    await asyncio.sleep(1)
    list = (
        "THIS MESSAGE WILL SELFDESTRUCT IN 4",
        "THIS MESSAGE WILL SELFDESTRUCT IN 3",
        "THIS MESSAGE WILL SELFDESTRUCT IN 2",
        "THIS MESSAGE WILL SELFDESTRUCT IN 1",
        "THIS MESSAGE WILL SELFDESTRUCT IN 0",
        "💣","💥")
    for i in list:
      await asyncio.sleep(1)
      await m.edit(content=i)
      
  @animation.subcommand(name="table", description="Se a table.")
  async def table(self, ctx):
    m = await ctx.send("`(\°-°)\  ┬─┬`")
    lst = ("`(\°□°)\  ┬─┬`",
      "`(-°□°)-  ┬─┬`",
      "`(╯°□°)╯    ]`",
      "`(╯°□°)╯     ┻━┻`",
      "`(╯°□°)╯       [`",
      "`(╯°□°)╯          ┬─┬`",
      "`(╯°□°)╯                 ]`",
      "`(╯°□°)╯                  ┻━┻`",
      "`(╯°□°)╯                         [`",
      "`(\°-°)\                               ┬─┬`")

    for k in lst:
      await asyncio.sleep(0.5)
      await ctx.edit(content=k)

  @animation.subcommand(name="warning", description="...")
  async def warning(self, ctx):
    await ctx.send("...")
    list = (
      "`LOAD !! WARNING !! SYSTEM OVER`",
      "`OAD !! WARNING !! SYSTEM OVERL`",
      "`AD !! WARNING !! SYSTEM OVERLO`",
      "`D !! WARNING !! SYSTEM OVERLOA`",
      "`! WARNING !! SYSTEM OVERLOAD !`",
      "`WARNING !! SYSTEM OVERLOAD !!`",
      "`ARNING !! SYSTEM OVERLOAD !! W`",
      "`RNING !! SYSTEM OVERLOAD !! WA`",
      "`NING !! SYSTEM OVERLOAD !! WAR`",
      "`ING !! SYSTEM OVERLOAD !! WARN`",
      "`NG !! SYSTEM OVERLOAD !! WARNI`",
      "`G !! SYSTEM OVERLOAD !! WARNIN`",
      "`!! SYSTEM OVERLOAD !! WARNING`",
      "`! SYSTEM OVERLOAD !! WARNING !`",
      "`SYSTEM OVERLOAD !! WARNING !!`",
      "`IMMINENT SHUT-DOWN IN 0.5 SEC!`",
      "`WARNING !! SYSTEM OVERLOAD !!`",
      "`IMMINENT SHUT-DOWN IN 0.2 SEC!`",
      "`SYSTEM OVERLOAD !! WARNING !!`",
      "`IMMINENT SHUT-DOWN IN 0.01 SEC!`",
      "`SHUT-DOWN EXIT ERROR ¯\\(｡･益･)/¯`",
      "`CTRL + R FOR MANUAL OVERRIDE...`",
    )

    for i in list:
      await ctx.message.edit(content=i)
      await asyncio.sleep(0.3)

def setup(bot):
  bot.add_cog(Fun(bot))
