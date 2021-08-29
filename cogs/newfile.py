import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random
import json, datetime, sys, traceback


class Giveaways(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Giveaways are now ready!")

	def convert(self, time):
		pos = ["s", "m", "h", "d"]

		time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

		unit = time[-1]

		if unit not in pos:
			return -1
		try:
			val = int(time[:-1])
		except:
			return -2

		return val * time_dict[unit]

	def dump(self, iid, dur, ended, deleted, chann, prize):
		with open("data/gw.json", "r") as f:
			gg = json.load(f)

		gg[str(iid)] = {
		    "ended": ended,
		    "deleted": deleted,
		    "chann": chann,
		    "dur": dur,
		    "prize": prize
		}

		with open("data/gw.json", "w") as f:
			json.dump(gg, f, indent=2)

	def get_ch(self, id):
		with open("data/gw.json", "r") as f:
			ih = json.load(f)
		if str(id) in ih:
			hh = ih[str(id)]
			if hh["deleted"] == "y":
				return "del"
			elif hh["ended"] == "y":
				return "une"
			else:
				ok = hh["chann"]
				return ok
		else:
			return "nil"

	def _tm(self, *, args: str):
		date, time = args.split(" ")
		yr, mnth, day = date.split("-")
		hr, mins, sec = time.split(":")
		sec, mic = sec.split(".")
		hr = int(hr)
		#pre = int(pre)
		mins = int(mins)
		sec = int(sec)
		day = int(day)
		mnth = int(mnth)
		yr = int(yr)
		#hr=int(hr)
		mic = int(mic)
		return datetime.datetime(yr, mnth, day, hr, mins, sec, mic)

	def _get_time(self, args: str):
		suff = args[-1]
		pre, _ = args.split(suff)
		pre = pre
		time = str(datetime.datetime.now())
		date, time = time.split(" ")
		yr, mnth, day = date.split("-")
		hr, mins, sec = time.split(":")
		sec, mic = sec.split(".")
		hr = int(hr)
		pre = int(pre)
		mins = int(mins)
		sec = int(sec)
		day = int(day)
		mnth = int(mnth)
		yr = int(yr)
		if suff == "s":
			sec += pre
		if suff == "m":
			mins += pre
		if suff == "h":
			hr += pre
		if suff == "d":
			day += pre
		kl = [1, 3, 5, 7, 8, 10, 12]
		kk = [4, 6, 9, 11]
		while True:
			if sec > 59:
				sec -= 60
				mins += 1
			else:
				break
		while True:
			if mins > 59:
				mins -= 60
				hr += 1
			else:
				break
		while True:
			if hr > 23:
				hr -= 24
				day += 1
			else:
				break
		if mnth in kl:
			while True:
				if day > 30:
					day -= 30
					mnth += 1
				else:
					break
		elif mnth in kk:
			while True:
				if day > 29:
					day -= 30
					mnth += 1
				else:
					break
		else:
			if yr / 4:
				while True:
					if day > 28:
						day -= 29
						mnth += 1
					else:
						break
			else:
				while True:
					if day > 27:
						day -= 28
						mnth += 1
					else:
						break
		while True:
			if mnth > 11:
				mnth -= 12
				yr += 1
			else:
				break

		return [
		    int(yr),
		    int(mnth),
		    int(day),
		    int(hr),
		    int(mins),
		    int(sec),
		    int(mic)
		]

	@commands.Cog.listener()
	async def on_g_timer_complete(self, id_):
		with open("data/gw.json", "r") as f:
			k = json.load(f)
		id_,m=id_.args[0],id_.args[1]
		i_ = str(id_)
		if i_ not in k:
			return
		k_=k[i_]
		if k_["ended"] == "y":
			return
		if k_["deleted"] == "y":
			return
		tin = k
		tingd = k_["chann"]
		che = self.bot.get_channel(int(tingd)) or await self.bot.fetch_channel(
		    int(tingd))
		if not che:
			return
		my_msg = await che.fetch_message(id_)
		if not my_msg:
			return
		kk = tin[str(id_)]
		prize = kk["prize"]
		users = await my_msg.reactions[0].users().flatten()
		if self.bot.user in users:
		  users.pop(users.index(self.bot.user))
		if len(users) == 0:
			em = discord.Embed(title='Giveaway Failed', color=0x00ffff)
			em.add_field(name="Reason:", value="No one joined")
			em.add_field(name="Next steps:",
			             value="Dont make a giveaway which someone don't enter!")
			return await che.send(embed=em)
		winner = random.choice(users)
		newembed = discord.Embed(title="Giveaway Ended!",
		                         description=f"{prize}",
		                         color=0x00ffff,
		                         timestamp=datetime.datetime.utcnow())
		newembed.add_field(name="Hosted by:", value=m)
		newembed.set_footer(text="ended")
		newembed.add_field(name="Winner", value=f"{winner.mention}")
		await my_msg.edit(embed=newembed)
		await my_msg.reply(f"Congratulations! {winner.mention} won {prize}!")
		time = str(datetime.datetime.utcnow())
		self.dump(my_msg.id, time, "y", "n", che.id, prize)

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def gstart(self, ctx):
		await ctx.send(
		    "Let's start with this giveaway! Answer these questions within 15 seconds!"
		)

		questions = [
		    "Which channel should it be hosted in?",
		    "What should be the duration of the giveaway? (s|m|h|d)",
		    "What is the prize of the giveaway?"
		]

		answers = []

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		for i in questions:
			await ctx.send(i)

			try:
				msg = await self.bot.wait_for('message',
				                              timeout=15.0,
				                              check=check)
			except asyncio.TimeoutError:
				await ctx.send(
				    "You didn't answer in time, please be quicker next time!")
				return
			else:
				answers.append(msg.content)

		try:
			c_id = int(answers[0][2:-1])
		except:
			await ctx.send(
			    f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time."
			)
			return

		channel = self.bot.get_channel(c_id)

		time = self.convert(answers[1])
		if time == -1:
			await ctx.send(
			    f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!"
			)
			return
		elif time == -2:
			await ctx.send(
			    f"The time must be an integer. Please enter an integer next time"
			)
			return

		prize = answers[2]
		tat = self._get_time(answers[1])

		# send a message for the user to know the giveaway started!
		await ctx.send(
		    f"The Giveaway will be in {channel.mention} and will last {answers[1]}!"
		)
		# now send the embed in the channel!
		embed = discord.Embed(title="Giveaway!",
		                      description=f"{prize}",
		                      color=ctx.author.color,
		                      timestamp=datetime.datetime(
		                          tat[0], tat[1], tat[2], tat[3], tat[4],
		                          tat[5], tat[6]))
		embed.add_field(name="Hosted by:", value=ctx.author.mention)
		embed.set_footer(text=f"Ends")
		my_msg = await channel.send(embed=embed)
		# and then add the reactions
		await my_msg.add_reaction('🎉')
		self.dump(my_msg.id, time, "n", "n", channel.id, prize)
		t=await (self.bot.get_cog("Reminder")).create_timer(datetime.datetime(tat[0], tat[1], tat[2], tat[3], tat[4],tat[5], tat[6]),"g",my_msg.id,f"<@!{ctx.author.id}>")
		# sleep for the time!
		"""
		await asyncio.sleep(time)

		with open("data/gw.json", "r") as f:
			kk = json.load(f)

		wow = kk[str(my_msg.id)]

		if wow["ended"] == "y":
			return
		elif wow["deleted"] == "y":
			return
		else:
			# and then fetch it back
			new_msg = await channel.fetch_message(my_msg.id)
			# get a list of users
			users = await new_msg.reactions[0].users().flatten()
			users.pop(users.index(self.bot.user))
			# now have some checks
			if len(users) == 0:
				em = discord.Embed(title='Giveaway Failed',
				                   color=ctx.author.color)
				em.add_field(name="Reason:", value="No one joined")
				em.add_field(
				    name="Next steps:",
				    value="Dont make a giveaway which you don't enter!")
				await channel.send(embed=em)
				self.dump(my_msg.id, time, "y", "n", channel.id, prize)
				return

			winner = random.choice(users)
			# edit embed to show winner
			newembed = discord.Embed(title="Giveaway Ended!",
			                         description=f"{prize}",
			                         color=ctx.author.color,
			                         timestamp=datetime.datetime.utcnow())
			newembed.add_field(name="Hosted by:", value=ctx.author.mention)
			# now do winers gizmo
			newembed.add_field(name="Winner", value=f"{winner.mention}")
			newembed.set_footer(text="Ended")
			await my_msg.edit(embed=newembed)
			await channel.send(
			    f"Congratulations! {winner.mention} won {prize}!")
			self.dump(my_msg.id, f"{datetime.datetime.utcnow()}", "y", "n",
			          channel.id, prize)"""

	@gstart.error
	async def gstart_error(self, ctx, error):
		print(error, file=sys.stderr)
		traceback.print_exc()
		if isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title="Can't start giveaway",
			                      color=ctx.author.color)
			embed.add_field(
			    name="Reason:",
			    value="you don't have `manage_guild` permission for this")
			embed.add_field(name="Ideal Solution:",
			                value="Get the perms, lmao!")
			await ctx.send(embed=embed)

	@commands.command()
	@has_permissions(manage_guild=True)
	async def greroll(self, ctx, id: int):
		id_ = id
		with open("data/gw.json", "r") as f:
			tin = json.load(f)

		ih = tin

		if str(id_) in ih:
			hh = ih[str(id_)]
			if hh["deleted"] == "y":
				await ctx.send("This giveaway has been deleted")
			elif hh["ended"] == "n":
				await ctx.send("This giveaway has not been ended")
			else:
				ok = hh["chann"]

		else:
			await ctx.send("Incorrect id was entered")
			ok = "lol"

		if ok == "lol":
			return
		else:
			che = self.bot.get_channel(int(ok))
			my_msg = await che.fetch_message(id_)

			kk = tin[str(id_)]
			prize = kk["prize"]

			users = await my_msg.reactions[0].users().flatten()
			users.pop(users.index(self.bot.user))

			if len(users) == 0:
				em = discord.Embed(title='Giveaway Failed',
				                   color=ctx.author.color)
				em.add_field(name="Reason:", value="No one joined")
				em.add_field(
				    name="Next steps:",
				    value="Dont make a giveaway which you don't enter!")
				await che.send(embed=em)
				return
			winner = random.choice(users)
			await my_msg.reply(
			    f"Congratulations! The new winner is {winner.mention}!")
			prize = hh["prize"]
			time = hh["dur"]
			#date, =time.split(" ")
			newembed = discord.Embed(title="Giveaway Ended!",
			                         description=f"{prize}",
			                         color=ctx.author.color,
			                         timestamp=self._tm(args=time))
			newembed.add_field(name="Hosted by:", value=ctx.author.mention)
			newembed.add_field(name="Winner", value=f"{winner.mention}")
			newembed.set_footer(text="ended")
			await my_msg.edit(embed=newembed)
			self.dump(my_msg.id, time, "y", "n", ctx.channel.id, prize)

	@greroll.error
	async def reroll_error(self, ctx, error):
		print(error, file=sys.stderr)
		traceback.print_exc()
		if isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title="Can't reroll giveaway",
			                      color=ctx.author.color)
			embed.add_field(
			    name="Reason:",
			    value="you don't have `manage_guild` permission for this")
			embed.add_field(name="Ideal Solution:",
			                value="Get the perms, lmao!")
			await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(manage_guild=True)
	async def gend(self, ctx, id_: int):
		with open("data/gw.json", "r") as f:
			tin = json.load(f)

		tingd = self.get_ch(id_)

		if tingd == "nil":
			await ctx.send("Incorrect id was entered")
		elif tingd == "une":
			await ctx.send("This giveaway has already been ended")
		elif tingd == "del":
			await ctx.send("This giveaway has been deleted")
		else:

			che = self.bot.get_channel(int(tingd))
			my_msg = await che.fetch_message(id_)

			kk = tin[str(id_)]
			prize = kk["prize"]

			users = await my_msg.reactions[0].users().flatten()
			if self.bot.user in users:
			  users.pop(users.index(self.bot.user))

			if len(users) == 0:
				em = discord.Embed(title='Giveaway Failed',
				                   color=ctx.author.color)
				em.add_field(name="Reason:", value="No one joined")
				em.add_field(
				    name="Next steps:",
				    value="Dont make a giveaway which you don't enter!")
				await che.send(embed=em)
				return

			winner = random.choice(users)
			newembed = discord.Embed(title="Giveaway Ended!",
			                         description=f"{prize}",
			                         color=ctx.author.color,
			                         timestamp=datetime.datetime.utcnow())
			newembed.add_field(name="Hosted by:", value=ctx.author.mention)
			newembed.set_footer(text="ended")
			newembed.add_field(name="Winner", value=f"{winner.mention}")
			await my_msg.edit(embed=newembed)
			await my_msg.reply(f"Congratulations! {winner.mention} won {prize}!")
			time = str(datetime.datetime.utcnow())
			self.dump(my_msg.id, time, "y", "n", che.id, prize)

	@gend.error
	async def gend_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title="Can't end giveaway",
			                      color=ctx.author.color)
			embed.add_field(
			    name="Reason:",
			    value="you don't have `manage_guild` permission for this")
			embed.add_field(name="Ideal Solution:",
			                value="Get the perms, lmao!")
			await ctx.send(embed=embed)
		print(error,file=sys.stderr)
		traceback.print_exc()


def setup(bot):
	bot.add_cog(Giveaways(bot))
