# plugin: loadable: True

import json
import config
import discord
import asyncio, random
from discord.ext import commands
import appcommands
from core import Cog

from models import balance

from plugins.games.hangman import Hangman
from plugins.games.blackjack import Blackjack
from plugins.games.twenty_48 import Game_2048
from plugins.games.tictactoe import TicTacToe, TicTacToe_Ai


coins_opt = appcommands.Option("_", "Bet How many coins? (You can lose them also)", required=False, type=appcommands.OptionType.INTEGER)

class Fun(Cog):
  play = appcommands.slashgroup(name="play", description="Game commands!")
  fun  = appcommands.slashgroup(name="fun", description="Fun Commands!")

  async def transact(self, ctx, coins):
    coins = coins or None
    if coins:
      u=await balance.get_or_none(uid=ctx.author.id)
      if not u: await self.bot.economy.open_acc(ctx.author.id);hand=500
      else: hand=u.hand

      if coins > hand: return await ctx.send((await ctx.get_lang()).plugins.games.insufficient, ephemeral=True)
      await self.bot.economy.take_money("wallet", ctx.author.id, coins)

  @play.subcommand(name="blackjack", description="Play blackjack with me!")
  async def play_blackjack(self,ctx, coins: coins_opt = -1):
    if coins:
      try:
        if await self.transact(ctx,coins): return
      except: return
    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    game = Blackjack(msg, ctx.author.id, coins=coins)
    await game.start()

  @play.subcommand(name="tic-tac-toe", description="play tic-tac-toe with me or somebody")
  async def play_tictactoe(self, ctx, with_player: discord.User = None):
    user = with_player or ctx.bot.user
    if user.id == ctx.author.id: return await ctx.send("You can't play tic-tac-toe with yourself!", ephemeral=True)
    if not user.bot:
      if not await ctx.confirm(
        f"{user.mention}, {ctx.author.mention} wants to play tic-tac-toe with you, confirm by clicking on buttons below",
        user=user,
        language=config.languages.english
      ): return

      game = TicTacToe(ctx.message, ctx.author.id, user.id)
      await ctx.edit(content=f"It's <@!{ctx.author.id}>\u200b's turn now!",)
    else:
      msg = await ctx.send(f"It's <@!{ctx.author.id}>\u200b's turn now!")
      game = TicTacToe_Ai(msg, ctx.author.id,)
      if user.id != ctx.bot.user.id: game.o.name = user.mention
    await game.start()

  @play.subcommand(name="hangman", description="Play hangman")
  async def play_hangman(self, ctx, coins: coins_opt = None):
    try: 
      if await self.transact(ctx,coins=coins): return
    except: return
    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    game = Hangman(msg, ctx.author.id, coins=coins)
    await game.start()

  @play.subcommand(name="2048", description="Play the game of 2048")
  async def play_2048(self, ctx, size: int = 4):
    if size<4 or size>10: return await ctx.send((await ctx.get_lang()).plugins.games._2048.value_err, ephemeral=True)

    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    game = Game_2048(size, msg, ctx.author.id)
    await game.start()

  @fun.subcommand(name="kill", description="Kill someone!")
  async def fun_kill(self, ctx, user: discord.Member):
    kill = json.load(open("assets/kill.json"))

    if user.id == ctx.author.id:
      return await ctx.send("Why do u want to kill yourself??", ephemeral=True)
      
    response = random.choice(kill.get("kills"))

    if "$author" in response:
      response=response.replace("$author", ctx.author.display_name)
      
    if "$mention" in response:
      response = response.replace("$mention", user.display_name)
      
    await ctx.send(response)


  fun_animation = fun.subcommandgroup(name="animation", description="Animation Commands!")


  @fun_animation.subcommand(name="cathi", description="Make a cat say something")
  async def fun_animation_cathi(self, ctx, text: str = "Hi..."):
    ctx=await ctx.reply("starting")
    list = (
        """??? ???????????????_??????
??????????????????  ???|"
??????|????????????|???|
??????|????????????|???
??????????????????""",
        f"""??? ?????????{text}
 ???   ??? ????????????_
?????????(??????????`)  ??????
??????|????????????|??????
??????|????????????|???
??????????????????""",
    )
    for i in range(3):
      for cat in list:
        await ctx.edit(content=cat)
        await asyncio.sleep(1)
        

  @fun_animation.subcommand(name="flop", description="...")
  async def fun_animation_flop(self, ctx):
    m = await ctx.send("Starting...")
    list = (
        "(   ?? - ??) (' - '   )",
        "(\\\?? - ??)\ (' - '   )",
        "(??????????)??? (' - '   )",
        "(??????????)???(' - '   )",
        "(??????????)??????(\\\ .o.)\\",
    )
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(1.5)

  @fun_animation.subcommand(name="poof", description="...")
  async def fun_animation_poof(self, ctx):
    m = await ctx.send("...")
    list = ("(   ' - ')", "' - ')", "- ')", "')", ")", "*poofness*")
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(1.5)

  @fun_animation.subcommand(name="virus", description="Insert a virus to yourself or someone else")
  async def fun_animation_virus(self, ctx, user: discord.Member = None, virus: str = "trojan"):
    m = await ctx.send("...")
    user = user or ctx.author
    list = (
        f"`[?????????                    ] / {virus}-virus.exe Packing files.`",
        f"`[?????????????????????                ] - {virus}-virus.exe Packing files..`",
        f"`[????????????????????????????????????           ] \ {virus}-virus.exe Packing files..`",
        f"`[??????????????????????????????????????????         ] | {virus}-virus.exe Packing files..`",
        f"`[???????????????????????????????????????????????????      ] / {virus}-virus.exe Packing files..`",
        f"`[????????????????????????????????????????????????????????????   ] - {virus}-virus.exe Packing files..`",
        f"`[?????????????????????????????????????????????????????????????????? ] \ {virus}-virus.exe Packing files..`",
        f"`Successfully downloaded {virus}-virus.exe`",
        "`Injecting virus.   |`",
        "`Injecting virus..  /`",
        "`Injecting virus... -`",
        f"`Successfully Injected {virus}-virus.exe into {user.name}`",
    )
    for i in list:
      await m.edit(content=i)
      await asyncio.sleep(0.8)

  @fun_animation.subcommand(name="boom", description="Booms a message!")
  async def fun_animation_boom(self, ctx):
    m = await ctx.send("THIS MESSAGE WILL SELFDESTRUCT IN 5")
    await asyncio.sleep(1)
    list = (
        "THIS MESSAGE WILL SELFDESTRUCT IN 4",
        "THIS MESSAGE WILL SELFDESTRUCT IN 3",
        "THIS MESSAGE WILL SELFDESTRUCT IN 2",
        "THIS MESSAGE WILL SELFDESTRUCT IN 1",
        "THIS MESSAGE WILL SELFDESTRUCT IN 0",
        "????","????")
    for i in list:
      await asyncio.sleep(1)
      await m.edit(content=i)
      
  @fun_animation.subcommand(name="table", description="Se a table.")
  async def fun_animation_table(self, ctx):
    m = await ctx.send("`(\??-??)\  ?????????`")
    lst = ("`(\???????)\  ?????????`",
      "`(-???????)-  ?????????`",
      "`(??????????)???    ]`",
      "`(??????????)???     ?????????`",
      "`(??????????)???       [`",
      "`(??????????)???          ?????????`",
      "`(??????????)???                 ]`",
      "`(??????????)???                  ?????????`",
      "`(??????????)???                         [`",
      "`(\??-??)\                               ?????????`")

    for k in lst:
      await asyncio.sleep(0.5)
      await ctx.edit(content=k)

  @fun_animation.subcommand(name="warning", description="...")
  async def fun_animation_warning(self, ctx):
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
      "`SHUT-DOWN EXIT ERROR ??\\(????????????)/??`",
      "`CTRL + R FOR MANUAL OVERRIDE...`",
    )

    for i in list:
      await ctx.message.edit(content=i)
      await asyncio.sleep(0.3)

def setup(bot):
  bot.add_cog(Fun(bot))
