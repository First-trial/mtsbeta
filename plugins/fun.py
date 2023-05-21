# plugin: loadable: True

import json
import config
import discord
import asyncio, random, discord
from discord.ext import commands
from discord import app_commands
from core import Cog

from models import balance

from plugins.games.hangman import Hangman
from plugins.games.blackjack import Blackjack
from plugins.games.twenty_48 import Game_2048
from plugins.games.tictactoe import TicTacToe, TicTacToe_Ai


coins_opt = int #app_commands.Parameter(display_name="bet coins", description="Bet How many coins? (You can lose them also)", required=False, type=discord.AppCommandOptionType.integer)


class Fun(Cog):
  play = app_commands.Group(name="play", description="Game commands!")
  # fun  = appcommands.slashgroup(name="fun", description="Fun Commands!")

  async def transact(self, ctx, coins):
    coins = coins or None
    if coins:
      u=await balance.get_or_none(uid=ctx.author.id)
      if not u: await self.bot.economy.open_acc(ctx.author.id);hand=500
      else: hand=u.hand

      if coins > hand: return await ctx.send((await ctx.get_lang()).plugins.games.insufficient, ephemeral=True)
      await self.bot.economy.take_money("wallet", ctx.author.id, coins)

  @play.command(name="blackjack", description="Play blackjack with me!")
  async def play_blackjack(self, ctx, coins: coins_opt = -1):
    if coins:
      try:
        if await self.transact(ctx,coins): return
      except: return
    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    game = Blackjack(msg, ctx.author.id, coins=coins)
    await game.start()

  @play.command(name="tic-tac-toe", description="play tic-tac-toe with me or somebody")
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

  @play.command(name="hangman", description="Play hangman")
  async def play_hangman(self, ctx, coins: coins_opt = None):
    try:
      if await self.transact(ctx,coins=coins): return
    except:
      return
    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    print(ctx.message, msg)
    game = Hangman(msg, ctx.author.id, coins=coins)
    await game.start()

  @play.command(name="2048", description="Play the game of 2048")
  async def play_2048(self, ctx, size: int = 4):
    if size<4 or size>10: return await ctx.send((await ctx.get_lang()).plugins.games._2048.value_err, ephemeral=True)

    msg = await ctx.send((await ctx.get_lang()).plugins.fun.starting)
    game = Game_2048(size, msg, ctx.author.id)
    await game.start()

'''
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
'''
async def setup(bot):
  await bot.add_cog(Fun(bot))
