import discord, json
from discord.ext import commands


async def _ch(ctx):
	with open("data/workers.json", "r") as f:
		kk = json.load(f)

	if not str(ctx.author.id) in kk:
		await ctx.send(
		    "you are not working\n pls choose your work by `mts work as <work>`"
		)
		raise ValueError("uhuh")
	return True


class eco(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("A wild economy system appeared")

	async def open_acc(self, id, ctx):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)
		kk[str(id)] = {"wallet": 500, "bank": 0}
		await self.up_usr(ctx, id, 0, 500)
		with open("data/bal.json", "w") as f:
			json.dump(kk, f, indent=4)

	async def give_work(self, id, work):
		with open("data/workers.json", "r") as f:
			kk = json.load(f)
		kk[str(id)] = work

		with open("data/workers.json", "w") as f:
			json.dump(kk, f, indent=4)

	async def give_money(self, area, id, money, ctx):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(id) in kk:
			if area == "wallet":
				k = kk[str(id)]
				w = k["wallet"]
				bank = k["bank"]
				money += w
				kk[str(id)] = {"wallet": money, "bank": bank}
				await self.up_usr(ctx, id, bank, money)
			else:
				k = kk[str(id)]
				w = k["bank"]
				bank = k["wallet"]
				money += w
				kk[str(id)] = {"wallet": bank, "bank": money}
				await self.up_usr(ctx, id, money, bank)
		else:
			if area == "wallet":
				bank = 0
				money += 500
				kk[str(id)] = {"wallet": money, "bank": bank}
				await self.up_usr(ctx, id, bank, money)
			else:
				bank = money
				mon = 500
				kk[str(id)] = {"wallet": mon, "bank": bank}
				await self.up_usr(ctx, id, bank, mon)
		with open("data/bal.json", "w") as f:
			json.dump(kk, f, indent=4)

	async def up_usr(self, ctx, uid, bank, hand):
		await ctx.db.execute(f"DELETE FROM bal WHERE uid = '{uid}'")
		await ctx.db.execute(
		    f"INSERT INTO bal (uid, bank, hand) VALUES ('{uid}','{bank}','{hand}')"
		)

	async def take_money(self, area, id, money, ctx):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(id) in kk:
			if area == "wallet":
				k = kk[str(id)]
				w = k["wallet"]
				bank = k["bank"]
				w -= money
				kk[str(id)] = {"wallet": w, "bank": bank}
				await self.up_usr(ctx, id, bank, w)
			else:
				k = kk[str(id)]
				w = k["bank"]
				bank = k["wallet"]
				w -= money
				kk[str(id)] = {"wallet": bank, "bank": w}
				await self.up_usr(ctx, id, w, bank)

		else:
			if area == "wallet":
				bank = 0
				money = 500 - money
				kk[str(id)] = {"wallet": money, "bank": bank}
				await self.up_usr(ctx, id, bank, money)
			else:
				return

		with open("data/bal.json", "w") as f:
			json.dump(kk, f, indent=4)

	@commands.command(name="bal", aliases=["balance"])
	async def bal(self, ctx, u: discord.Member = None):
		if u == None:
			u = ctx.author
		else:
			u = u

		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(u.id) in kk:
			k = kk[str(u.id)]
			wallet = k["wallet"]
			bank = k["bank"]
			b = discord.Embed(
			    title=f"{u.name}'s balance",
			    description=f"Wallet: `{wallet} coins`\nBank: `{bank} coins`")
			await ctx.send(embed=b)
		else:
			await self.open_acc(u.id, ctx)
			b = discord.Embed(
			    title=f"{u.name}'s balance",
			    description=f"Wallet: `500 coins`\nBank: `0 coins`")
			await ctx.send(embed=b)

	@commands.group(name="work", invoke_without_command=True)
	@commands.check(_ch)
	@commands.cooldown(1, 1800, commands.BucketType.user)
	async def work(self, ctx):
		with open("data/workers.json", "r") as f:
			kk = json.load(f)

		if ctx.author.id == 730454267533459568:
			we = 50000000
			pass
		else:
			we = 1500
			pass

		if str(ctx.author.id) in kk:
			w = kk[str(ctx.author.id)]

			await ctx.send(f"you got {we} coins after working as {w}")
			w = "wallet"
			await self.give_money(w, ctx.author.id, we, ctx)
		else:
			await ctx.send(
			    "you are not working\nChoose your work by `Mts work as <work>`"
			)

	@work.command(name="as", pass_context=True)
	@commands.cooldown(0, 0, commands.BucketType.user)
	async def work_as(self, ctx, *, work):
		with open("assets/works.json", "r") as f:
			ch = json.load(f)

		if work.lower() in ch["works"]:
			ch[str(ctx.author.id)] = work
			await ctx.send(f"You are working as {work} now")
			await self.give_work(ctx.author.id, work)
		else:
			await ctx.send(
			    "this is not valid work.\nSee a list of work by `Mts work list`"
			)

	@work.command(name="list")
	@commands.cooldown(0, 0, commands.BucketType.user)
	async def works_list(self, ctx):
		w = discord.Embed(
		    description=
		    f"youtuber\ncoder\nhousewife\ncosplayer\nmemer\nfarmer\nengineer")
		w.set_footer(text="choose a work by `Mts work as <work>`")
		await ctx.send(embed=w)

	@work.error
	async def work_error(self, ctx, exc):
		if isinstance(exc, commands.CommandOnCooldown):
			c = round(exc.retry_after)
			if c > 60:
				c = round(c / 60)
			else:
				c = 1
			await ctx.send(f"you have already worked\nTry again in {c} minutes"
			               )
		else:
			print(exc)
			c = self.bot.get_channel(797336604045344788)
			await c.send(exc)

	@commands.command(name="dep", aliases=["deposit"])
	async def dep(self, ctx, am):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(ctx.author.id) in kk:
			a = "wallet"
			b = "bank"
			k = kk[str(ctx.author.id)]
			if am == "all":
				am = k["wallet"]
				await self.take_money(a, ctx.author.id, am, ctx)
				await self.give_money(b, ctx.author.id, am, ctx)
				await ctx.send(
				    f"Successfully deposited {am} coins to your bank")
			else:
				try:
					am = int(am)
					if am > k["wallet"]:
						await ctx.send(
						    "You don't have enough money in your wallet to deposit"
						)
					else:
						await self.take_money(a, ctx.author.id, am, ctx)
						await self.give_money(b, ctx.author.id, am, ctx)
						await ctx.send(
						    f"Successfully deposited {am} coins to your bank")
				except ValueError:
					await ctx.send("This is not a value")
					return
		else:
			await self.open_acc(ctx.author.id, ctx)
			a = "wallet"
			b = "bank"
			k = kk[str(ctx.author.id)]
			if am == "all":
				am = 500
				await self.take_money(a, ctx.author.id, am, ctx)
				await self.give_money(b, ctx.author.id, am, ctx)
				await ctx.send(
				    f"Successfully deposited {am} coins to your bank")
			else:
				if am > 500:
					await ctx.send(
					    "you only have 500 coins in your wallet to deposit")
				else:
					await self.take_money(a, ctx.author.id, am, ctx)
					await self.give_money(b, ctx.author.id, am, ctx)
					await ctx.send(
					    f"Successfully deposited {am} coins to your bank")

	@commands.command(name="with", aliases=["withdraw"])
	async def with_cmd(self, ctx, am):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(ctx.author.id) in kk:
			a = "wallet"
			b = "bank"
			k = kk[str(ctx.author.id)]
			if am == "all":
				am = k["bank"]
				await self.take_money(b, ctx.author.id, am, ctx)
				await self.give_money(a, ctx.author.id, am, ctx)
				await ctx.send(
				    f"Successfully withdrawed {am} coins from your bank")
			else:
				try:
					am = int(am)
					if am > k["bank"]:
						await ctx.send(
						    "You don't have enough money in your bank to withdraw"
						)
					else:
						await self.take_money(b, ctx.author.id, am, ctx)
						await self.give_money(a, ctx.author.id, am, ctx)
						await ctx.send(
						    f"Successfully withdraw {am} coins from your bank")
				except ValueError:
					await ctx.send("This is not a value")
					return
		else:
			await ctx.send("you don't have any money in your bank to withdraw")
			await self.open_acc(ctx.author.id, ctx)

	@commands.command(name="share", aliases=["givemoney"])
	async def share_cmd(self, ctx, u: discord.Member, am: int):
		with open("data/bal.json", "r") as f:
			kk = json.load(f)

		if str(ctx.author.id) in kk:
			h = kk[str(ctx.author.id)]

			if am > h["wallet"]:
				await ctx.send(
				    "you don't have enough money in your wallet to share")
				return
			else:
				pass

			w = "wallet"
			await self.take_money(w, ctx.author.id, am, ctx)
			await self.give_money(w, u.id, am, ctx)
			await ctx.send(f"you gave {am} coins to {u.mention}")
		else:
			await self.open_acc(ctx.author.id, ctx)
			await ctx.send("I just opened your account so please now try again"
			               )

	@commands.command()
	async def shop(self, ctx):
		e = discord.Embed(
		    title="Mts bot shop",
		    description=
		    "**1** :apple: Apple [**40 coins**](https://discord.gg/zdrSUu98BP)\n**2** :banana: Banana [**20 coins**](https://discord.gg/zdrSUu98BP)\n**3** :pizza: Pizza [**200 coins**](https://discord.gg/zdrSUu98BP)\n**4** :milk: Milk [**40 coins**](https://discord.gg/zdrSUu98BP)\n**5** :computer: Laptop [**3000 coins**](https://discord.gg/zdrSUu98BP)\n",
		    url="https://discord.gg/zdrSUu98BP")
		await ctx.send(embed=e)

	@commands.command()
	async def buy(self, ctx, item, count: int = 1):
		try:
			item = int(item)
		except:
			item = item
		if count <= 0:
			return await ctx.send("You can't buy this much thing")
		if isinstance(item, int):
			if item > 5 or item <= 0:
				return await ctx.send("item not found")
			it = {
			    "1": "apple",
			    "2": "banana",
			    "3": "pizza",
			    "4": "milk",
			    "5": "laptop"
			}
			item = it[str(item)]
		else:
			if item.lower() not in [
			    "apple", "banana", "pizza", "milk", "laptop"
			]:
				return await ctx.send("item not found")
			item = item.lower()
		with open("data/bal.json", "r") as f:
			k = json.load(f)
		if str(ctx.author.id) not in k:
			await self.open_acc(ctx.author.id, ctx)
		k = k[str(ctx.author.id)]
		cost = {
		    "apple": 40,
		    "banana": 20,
		    "pizza": 200,
		    "milk": 40,
		    "laptop": 3000
		}
		cost = cost[item]
		if k["wallet"] < cost * count:
			return await ctx.send(
			    f"you don't have enough money in your wallet to buy {items}")
		await self.take_money("wallet", ctx.author.id, cost * count, ctx)
		await ctx.send(f"You bought {count} {item} for {cost*count} coins")
		lst = await ctx.db.fetch(
		    f"SELECT * FROM inv WHERE uid='{ctx.author.id}' AND item='{item}'")
		_l = []
		c = count
		for i in lst:
			_l.append(dict(i))
		for i in _l:
			c = int(i["count"]) + count
		await ctx.db.execute(
		    f"DELETE FROM inv WHERE uid = '{ctx.author.id}' AND item = '{item}'"
		)
		await ctx.db.execute(
		    f"INSERT INTO inv (uid, item, count) VALUES ('{ctx.author.id}', '{item}','{c}')"
		)

	@commands.command(aliases=["inv"])
	async def inventory(self, ctx, user: discord.Member = None):
		user = user or ctx.author
		lst = await ctx.db.fetch(f"SELECT * FROM inv WHERE uid='{user.id}'")
		lst = list(dict(i) for i in lst)
		shop = {"apple": 1, "banana": 2, "pizza": 3, "milk": 4}
		t = ""
		apples, bananas, pizzas, milks, laptops = 0, 0, 0, 0, 0
		for i in lst:
			if i["item"] == "apple":
				apples = int(i["count"])
				t += f"**1** :apple: Apple -> {apples}\n"
			if i["item"] == "banana":
				bananas = int(i["count"])
				t += f"**2** :banana: Banana -> {bananas}\n"
			if i["item"] == "pizza":
				pizzas = int(i["count"])
				t += f"**3** :pizza: Pizza -> {pizzas}\n"
			if i["item"] == "milk":
				milks = int(i["count"])
				t += f"**4** :milk: Milk -> {milks}\n"
			if i["item"] == "laptop":
				laptops = int(i["count"])
				t += f"**5** :computer: Laptop -> {laptops}\n"
		e = discord.Embed(title=f"{user.display_name}'s Inventory",
		                  description=t or "Nothing In Inventory",
		                  url="https://discord.gg/zdrSUu98BP")
		await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(eco(bot))
