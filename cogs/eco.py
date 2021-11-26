import discord, asyncio
from discord.ext import commands
import appcommands
from models import balance, workers
from core import Cog
from appcommands import Option

async def check_work(ctx):
  if not await workers.get_or_none(uid=str(ctx.author.id)):
    await ctx.send(
        f"You are not working\nPls choose your work by `{ctx.clean_prefix}work as <work>`",
        ephemeral=True
    )
    return False
  return True

OWNER_SALARY = 5000000
OTHER_SALARY = 1500
WORK_COOLDOWN = 60 * 30
WORKS = [
  "youtuber",
  "coder",
  "housewife",
  "cosplayer",
  "memer",
  "farmer",
  "engineer",
  "ghost"
]
WORKS = [appcommands.Choice(work) for work in WORKS]

class eco(Cog):
  def __init__(self, bot):
    super().__init__(bot)
    self.buckets = {}
    self._tasks = []

  async def do_bucket_(self, id, t):
    self.buckets[id] = t
    while self.buckets[id] > 0:
      await asyncio.sleep(1)
      self.buckets[id] -= 1
    del self.buckets[id]

  def do_bucket(self,i,t):
    ta=self.bot.loop.create_task(self.do_bucket_(i,t))
    self._tasks.append(ta)

  def cog_unload(self,):
    for task in self._tasks:
      task.cancel()

  @commands.Cog.listener()
  async def on_ready(self):
    print("A wild economy system appeared")

  async def open_acc(self, id):
    await balance.create(uid=int(id), bank=0, hand=500); return True

  async def give_work(self, id, work):
    try:
      await workers.create(uid=int(id), work=work); return True
    except:
      return False

  async def give_money(self, area, id, money,):
    id = int(id)
    u = await balance.get_or_none(uid=id)
    if u:
      if area == "wallet":
        w = int(u.hand)
        bank = int(u.bank)
        money += w
        await self.up_usr(id, bank, money)
      else:
        w = int(u.hand)
        bank = int(u.bank)
        bank += money
        await self.up_usr(id, bank, w)
    else:
      if area == "wallet":
        bank = 0
        money += 500
        await self.up_usr(id, bank, money)
      else:
        bank = money
        money = 500
        await self.up_usr(id, bank, money)

  async def up_usr(self, uid, bank, hand):
    r=balance.get_or_none(uid=int(uid))
    if await r is None:
      await self.open_acc(uid)
      r=balance.get_or_none(uid=int(uid))

    await r.update(bank=int(bank), hand=int(hand))

  async def take_money(self, area, id, money,):
    id = int(id)
    u = await balance.get_or_none(uid=id)
    if u:
      if area == "wallet":
        w = int(u.hand)
        bank = int(u.bank)
        money -= w
        await self.up_usr(id, bank, money)
      else:
        w = int(u.hand)
        bank = int(u.bank)
        bank -= money
        await self.up_usr(id, bank, w)
    else:
      if area == "wallet":
        bank = 0
        money -= 500
        await self.up_usr(id, bank, money)
      else:
        await self.open_acc(id)

  @appcommands.command(name="balance", description="Check balance of your or someone other")
  async def bal(self, ctx, user: discord.Member = None):
    usr=user or ctx.author
    u = await balance.get_or_none(uid=usr.id)
    if u:
      wallet = u.hand
      bank = u.bank
      b = discord.Embed(
          title=f"{usr.name}'s balance",
          description=f"Wallet: `{wallet} coins`\nBank: `{bank} coins`")
      await ctx.reply(embed=b)
    else:
      await ctx.reply("Opening account....")
      await self.open_acc(usr.id,)
      b = discord.Embed(
          title=f"{usr.name}'s balance",
          description=f"Wallet: `500 coins`\nBank: `0 coins`")
      await ctx.edit(None, embed=b)

  work = appcommands.slashgroup(name="work",)

  @work.subcommand(name="now", description="Do some work")
  async def work_now(self, ctx):
    if not await check_work(ctx):
      return

    if ctx.author.id not in self.buckets:
      self.do_bucket(ctx.author.id, WORK_COOLDOWN)
    else:
      c = round(self.buckets[ctx.author.id])
      if c > 60:
        c = round(c / 60)
      else:
        c = 1
      return await ctx.send(f"You have already worked\nTry again in {c} minutes", ephemeral=True)

    if ctx.author.id == self.author_id:
      salary = OWNER_SALARY
    else:
      salary = OTHER_SALARY

    w = (await workers.get(uid=ctx.author.id)).work
    await ctx.send(f"you got {salary} coins after working as {w}")
    w = "wallet"
    await self.give_money(w, ctx.author.id, salary,)


  @work.subcommand(name="as", description="Choose your work")
  async def work_as(self, ctx, work: Option("-", "Chosen work", choices=WORKS, required=True)):
    if work.lower() not in list(w.value for w in WORKS):
      await ctx.send(
        f"This is not valid work.\nSee a list of work by `{ctx.clean_prefix}work list`",
        ephemeral=True
      )
    elif not await self.give_work(ctx.author.id, work):
      await ctx.send("You are already doing a job, pls resign from it before taking a new job\n" \
f"(`{ctx.clean_prefix} work resign`)", ephemeral=True)
    else:
      await ctx.send(f"You are working as {work} now!")

  @work.subcommand(name="resign", description="Resign from your work")
  async def work_resign(self, ctx):
    worker = workers.get_or_none(uid=ctx.author.id)
    if not await worker:
      await ctx.send(f"You aren't working, pls choose a job (`{ctx.prefix}work as [work]`)", ephemeral=True)
    else:
      await worker.delete()
      await ctx.send(f"Successfully resigned from the job of {worker.work}")

  @work.subcommand(name="list", description="List of available jobs.")
  async def works_list(self, ctx):
    w = discord.Embed(
      title="**__Available Jobs__**",
      description="\n".join(list(w.value.title() for w in WORKS))
    )
    w.set_footer(text=f"choose a work by `{ctx.clean_prefix}work as <work>`")
    await ctx.send(embed=w)


  @appcommands.command(name="deposit", description="Deposit some money in your bank.")
  async def dep(self, ctx, amount: int):
    am = amount
    if amount <= 0:
        return await ctx.send("Amount should must be greater than 0, not {am}", ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:
      a = "wallet"
      b = "bank"
      am = int(am)
      if am > int(u.hand):
        await ctx.reply("You don't have enough money in your wallet to deposit", ephemeral=True)
      else:
        await ctx.reply(f'Depositing {am} coins in your bank...')
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(f"Successfully deposited {am} coins to your bank")
    else:
      await self.open_acc(ctx.author.id,)
      a = "wallet"
      b = "bank"
      if am > 500:
        await ctx.reply("you only have 500 coins in your wallet to deposit", ephemeral=True)
      else:
        await ctx.reply(f'Depositing {am} coins in your bank...')
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(f"Successfully deposited {am} coins to your bank")

  @appcommands.command(name="withdraw", description="Withdraw some money from your bank")
  async def with_cmd(self, ctx, amount: int):
    am = amount
    if amount <= 0:
        return await ctx.send("Amount should must be greater than 0, not {am}", ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:
      b = "wallet"
      a = "bank"
      am = int(am)
      if am > int(k.bank):
        await ctx.reply("You don't have enough money in your bank to withdraw", ephemeral=True)
      else:
        await ctx.reply(f'Withdrawing {am} coins from your bank...')
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(f"Successfully withdrawed {am} coins from your bank")
    else:
      await ctx.reply("You don't have any money in your bank to withdraw, go deposit some first", ephemeral=True)
      await self.open_acc(ctx.author.id,)

  @appcommands.command(name="share", description="Share your money to someone else")
  async def share_cmd(self, ctx, user: discord.Member, amount: int):
    am=amount
    if amount <= 0:
        return await ctx.send("Amount should must be greater than 0, not {am}", ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:

      if am > int(u.hand):
        return await ctx.send("you don't have enough money in your wallet to share", ephemeral=True)

      w = "wallet"
      await self.take_money(w, ctx.author.id, am,)
      await self.give_money(w, user.id, am,)
      await ctx.send(f"you gave {am} coins to {user.mention}")
    else:
      await self.open_acc(ctx.author.id,)
      await ctx.send("I just opened your account so please now try again", ephemeral=True)


def setup(bot):
  bot.add_cog(eco(bot))
