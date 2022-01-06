# plugin: loadable: True
import discord
import asyncio
from discord.ext import commands
import random
from typing import Optional
import appcommands
from core import Cog
from appcommands import cog
from typing import Union

class animations(Cog, name="animation"):
	"""animated messages"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def cathi(self, ctx: Union[appcommands.InteractionContext, commands.Context], *, text: str = "Hi..."):
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
			  await asyncio.sleep(1.5)
				

	@commands.command()
	async def flop(self, ctx: commands.Context):
		m = await ctx.send("Starting...")
		list = (
		    "(   ° - °) (' - '   )",
		    "(\\\° - °)\ (' - '   )",
		    "(—°□°)— (' - '   )",
		    "(╯°□°)╯(' - '   )",
		    "(╯°□°)╯︵(\\\ .o.)\\",
		)
		for i in list:
			#await asyncio.sleep(1.5)
			await m.edit(content=i)
			await asyncio.sleep(1.5)

	@commands.command()
	async def poof(self, ctx):
		m = await ctx.send("Ok")
		#await asyncio.sleep(0.5)
		"""poofness"""
		list = ("(   ' - ')", "' - ')", "- ')", "')", ")", "*poofness*")
		for i in list:
			#await asyncio.sleep(1.5)
			await m.edit(content=i)
			await asyncio.sleep(1.5)

	@commands.command()
	async def virus(self,
	                ctx,
	                user: Optional[discord.Member] = None,
	                *,
	                virus: str = "trojan"):
		m = await ctx.send("00")
		#await asyncio.sleep(0.5)
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
			await asyncio.sleep(1.5)
			#await m.edit(content=i)

	@commands.command()
	async def boom(self, ctx):
		m = await ctx.send("THIS MESSAGE WILL SELFDESTRUCT IN 5")
		await asyncio.sleep(1.5)
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
		  
	@commands.command()
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
	    await ctx.send(k)
  	  
class _:
    @commands.command()
    async def warning(self, ctx):
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
            "`CTRL + R FOR MANUAL OVERRIDE..`",
        )
        for i in list:
            await asyncio.sleep(1.5)
            await ctx.message.edit(content=i)

def setup(bot):
  bot.add_cog(anim(bot))
