import random
import discord
import asyncio
from discord.ext import commands

dice_1 = '1️⃣'
dice_2 = '2️⃣'
dice_3 = '3️⃣'
dice_4 = '4️⃣'
dice_5 = '5️⃣'
dice_6 = '6️⃣'


class wm:
	def __init__(self):
		self.footer = "Mts bot"


wm = wm()


class colors:
	def __init__(self):
		self.fun = 0xff9d57
		self.red = 0xff0000


colors = colors()


class ga(commands.Cog, name="Games"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def minesweeper(self, ctx):
		field00 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field01 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field02 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field03 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field04 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field05 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field06 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field07 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field08 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field10 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field11 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field12 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field13 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field14 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field15 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field16 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field17 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field18 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field20 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field21 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field22 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field23 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field24 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field25 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field26 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field27 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field28 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field30 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field31 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field32 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field33 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field34 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field35 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field36 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field37 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field38 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field40 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field41 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field42 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field43 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field44 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field45 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field46 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field47 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field48 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field50 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field51 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field52 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field53 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field54 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field55 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field56 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field57 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field58 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field60 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field61 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field62 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field63 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field64 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field65 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field66 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field67 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field68 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field70 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field71 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field72 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field73 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field74 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field75 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field76 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field77 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field78 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		field80 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field81 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field82 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field83 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field84 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field85 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field86 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field87 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
		field88 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

		minesweeper = f"""
|| {field00} || || {field10} || || {field20} || || {field30} || || {field40} || || {field50} || || {field60} || || {field70} || || {field80} ||
|| {field01} || || {field11} || || {field21} || || {field31} || || {field41} || || {field51} || || {field61} || || {field71} || || {field81} ||
|| {field02} || || {field12} || || {field22} || || {field32} || || {field42} || || {field52} || || {field62} || || {field72} || || {field82} ||
|| {field03} || || {field13} || || {field23} || || {field33} || || {field43} || || {field53} || || {field63} || || {field73} || || {field83} ||
|| {field04} || || {field14} || || {field24} || || {field34} || || {field44} || || {field54} || || {field64} || || {field74} || || {field84} ||
|| {field05} || || {field15} || || {field25} || || {field35} || || {field45} || || {field55} || || {field65} || || {field75} || || {field85} ||
|| {field06} || || {field16} || || {field26} || || {field36} || || {field46} || || {field56} || || {field66} || || {field76} || || {field86} ||
|| {field07} || || {field17} || || {field27} || || {field37} || || {field47} || || {field57} || || {field67} || || {field77} || || {field87} ||
|| {field08} || || {field18} || || {field28} || || {field38} || || {field48} || || {field58} || || {field68} || || {field78} || || {field88} ||
                    """
		m = discord.Embed(color=0xff9d57, description=minesweeper)
		m.set_author(name='Minesweeper',
		             icon_url="https://hqsartworks.me/icons/minesweeper.png")
		m.set_footer(text="Mts bot")
		await ctx.send(embed=m)

	@commands.command(pass_context=True)
	async def coinflip(self, ctx):
		flip = random.choice([
		    f'https://upload.wikimedia.org/wikipedia/de/thumb/8/80/2_euro_coin_Eu_serie_1.png/220px-2_euro_coin_Eu_serie_1.png',
		    f'https://www.zwei-euro.com/wp-content/uploads/2019/02/DE-2002.gif'
		])
		flipcoin = discord.Embed()
		flipcoin.colour = 0x12423
		flipcoin.set_thumbnail(
		    url=
		    "https://media1.tenor.com/images/938e1fc4fcf2e136855fd0e83b1e8a5f/tenor.gif?itemid=5017733"
		)
		flipcoin1 = await ctx.send(embed=flipcoin)
		coin = discord.Embed()
		coin.set_thumbnail(url=f'{flip}')
		await asyncio.sleep(2)
		await flipcoin1.delete()
		await ctx.send(embed=coin)

	@commands.command()
	async def rolldice(self, ctx):
		dice_ = [
		    f'{dice_1}', f'{dice_2}', f'{dice_3}', f'{dice_4}', f'{dice_5}',
		    f'{dice_6}'
		]

		rolldice = discord.Embed(
		    description=f'You rolled a {random.choice(dice_)}', color=0x00ffff)
		rolldice.set_author(
		    name='Roll a dice',
		    icon_url="https://hqsartworks.me/icons/giveaway_fun.png")
		rolldice.set_footer(text="Mts bot")
		await ctx.send(embed=rolldice)

	@commands.command()
	async def tournament(self, ctx, tc1: discord.Member, tc2: discord.Member,
	                     tc3: discord.Member,tc4: discord.Member=None):
		try:
			tc4 =tc4 or ctx.author
			user = [tc1, tc2, tc3, tc4]
			hitu1 = f'{tc1} chose a card!'
			hitu2 = f'{tc2} chose a card!'
			hitu3 = f'{tc3} chose a card!'
			hitu4 = f'{tc4} chose a card!'
			rndmc = [
			    'https://i.pinimg.com/originals/9b/bb/70/9bbb7015af1bcd420ee07d89048cebf7.jpg',
			    'https://pics.me.me/thumb_earth-angry-german-kid-spellcastor-tuner-he-rages-about-lag-and-52634494.png',
			    'https://www.memesmonkey.com/images/memesmonkey/cb/cbc69b7a454ec9f50fa0616ca3d4d4d9.jpeg',
			    'https://i.imgur.com/gq8aDzq.jpg',
			    'https://i.redd.it/gqse7u1cudw31.png',
			    'https://i.imgur.com/yeD5fGI.gif',
			    'https://images-na.ssl-images-amazon.com/images/I/51jxIccbroL._AC_.jpg',
			    'https://images-cdn.9gag.com/photo/aDzZ1LO_460s.jpg'
			]

			fight = discord.Embed(
			    description=
			    f'{tc1.display_name} vs. {tc2.display_name} vs. {tc3.display_name} vs. {tc4.display_name}'
			)
			fight.set_author(
			    name='Battle',
			    icon_url="https://hqsartworks.me/icons/battle.png",
			)
			fight.set_thumbnail(
			    url='https://media3.giphy.com/media/dw5SDFsmqFhYs/giphy.gif')
			fight.set_footer(text=wm.footer)
			fight1 = await ctx.send(embed=fight)

			hit = discord.Embed(title=hitu1, color=colors.fun)
			hit.set_image(url=random.choice(rndmc))
			hit_ = await ctx.send(embed=hit)
			await asyncio.sleep(3)

			hit2 = discord.Embed(title=hitu2, color=colors.fun)
			hit2.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit2)
			await asyncio.sleep(3)

			hit3 = discord.Embed(title=hitu3, color=colors.fun)
			hit3.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit3)
			await asyncio.sleep(3)

			hit4 = discord.Embed(title=hitu4, color=colors.fun)
			hit4.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit4)
			await asyncio.sleep(3)

			hit5 = discord.Embed(title=hitu1, color=colors.fun)
			hit5.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit5)
			await asyncio.sleep(3)

			hit6 = discord.Embed(title=hitu2, color=colors.fun)
			hit6.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit6)
			await asyncio.sleep(3)

			hit7 = discord.Embed(title=hitu3, color=colors.fun)
			hit7.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit7)
			await asyncio.sleep(3)

			hit8 = discord.Embed(title=hitu4, color=colors.fun)
			hit8.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit8)
			await asyncio.sleep(3)

			hit9 = discord.Embed(title=hitu2, color=colors.fun)
			hit9.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit9)
			await asyncio.sleep(3)

			hit10 = discord.Embed(title=hitu1, color=colors.fun)
			hit10.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit10)
			await asyncio.sleep(3)

			hit11 = discord.Embed(title=hitu2, color=colors.fun)
			hit11.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit11)
			await asyncio.sleep(3)

			hit12 = discord.Embed(title=hitu1, color=colors.fun)
			hit12.set_image(url=random.choice(rndmc))
			await hit_.edit(embed=hit12)
			await asyncio.sleep(3)
			m = [
			    fight1, hit_]#, hit2_, hit3_, hit4_, hit5_, hit6_, hit7_,
			    #hit8_, hit9_, hit10_, hit11_, hit12_
			#]
			for i in m:
				try:
					await i.delete()
				except:
					continue
			winner = discord.Embed(title=f'{random.choice(user)} WINS!!!\n',
			                       description=f'`{tc1}`'
			                       f' VS '
			                       f'`{tc2}`'
			                       f' VS `{tc3}` VS `{tc4}`',
			                       color=colors.red)
			winner.set_thumbnail(
			    url=
			    'https://cdna.artstation.com/p/assets/images/images/015/814/178/original/jean-baptiste-gabert-pokemonmockup.gif?1549763590'
			)
			winner.set_footer(text=wm.footer)
			await ctx.send(embed=winner)

		except Exception as e:
			print(e)
			error = discord.Embed(title='Cant find any user',
			                      description='User ```<@user>```')
			await ctx.send(embed=error)

	@commands.command(aliases=["rps", "sps"])
	async def ssp(self, ctx, args):
		ssp_choice = ['scissor', 'stone', 'paper']
		args = args.lower()
		choice = random.choice(ssp_choice)
		icon = "https://hqsartworks.me/icons/ssp.png"

		if choice == 'scissor' and args == 'scissor':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'scissor' and args == 'stone':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'scissor' and args == 'paper':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'stone' and args == 'scissor':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'stone' and args == 'stone':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'stone' and args == 'paper':
			s = discord.Embed(title='You win 🎉',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'paper' and args == 'scissor':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'paper' and args == 'stone':
			s = discord.Embed(title='You win 🎉',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'paper' and args == 'paper':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'scissor' and args == 'scissor':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'stone' and args == 'scissor':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'paper' and args == 'scissor':
			s = discord.Embed(title='You win 🎉',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'scissor' and args == 'stone':
			s = discord.Embed(title='You win 🎉',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'stone' and args == 'stone':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)
		elif choice == 'paper' and args == 'stone':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'scissor' and args == 'paper':
			s = discord.Embed(title='You lose 😂',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'stone' and args == 'paper':
			s = discord.Embed(title='You win 🎉',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		elif choice == 'paper' and args == 'paper':
			s = discord.Embed(title='Drawn 🙄',
			                  description='',
			                  color=colors.fun)
			s.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=s)

		else:
			n = discord.Embed(title='Dont try to cheat', color=colors.red)
			n.set_author(name='Scissor, stone and paper', icon_url=icon)
			await ctx.send(embed=n)


def setup(bot):
	bot.add_cog(ga(bot))
