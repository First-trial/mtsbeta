import discord
from discord.ext import commands
from appcommands import cog
from models import balance, workers
from core import Cog

async def check_work(ctx):
  if not await workers.get_or_none(uid=str(ctx.author.id)):
    await ctx.send(
        f"you are not working\n pls choose your work by `{ctx.clean_prefix}work as <work>`"
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
    ta=self.bot.loop.create_task(do_bucket_(i,t))
    self.tasks.append(ta) and

  def cog_unload(self,):
    for task in self._tasks:
      task.cancel()

  @commands.Cog.listener()
  async def on_ready(self):
    print("A wild economy system appeared")

  async def open_acc(self, id):
    await self.up_usr(id, 0, 500)

  async def give_work(self, id, work):
    await workers.create(uid=str(id), work=work)

  async def give_money(self, area, id, money,):
    id = str(id)
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
    r=await balance.get_or_none(uid=str(uid))
    if r is None:
      await balance.create(uid=str(uid), bank=str(bank), hand=str(hand))
    else:
      await r.update(bank=str(bank), hand=str(hand))

  async def take_money(self, area, id, money, ctx):
    id = str(id)
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

  @appcommands.command(name="balance")
  async def bal(self, ctx, user: discord.Member = None):
    u=user or ctx.author
    u = await balance.filter(uid=str(u.id))
    if u:
      wallet = u.wallet
      bank = u.bank
      b = discord.Embed(
          title=f"{u.name}'s balance",
          description=f"Wallet: `{wallet} coins`\nBank: `{bank} coins`")
      await ctx.reply(embed=b)
    else:
      await ctx.reply("Opening account....")
      await self.open_acc(u.id,)
      b = discord.Embed(
          title=f"{u.name}'s balance",
          description=f"Wallet: `500 coins`\nBank: `0 coins`")
      await ctx.edit(embed=b)

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
     return await ctx.send(f"you have already worked\nTry again in {c} minutes")

    if ctx.author.id == self.owner_id:
      salary = OWNER_SALARY
    else:
      we = OTHER_SALARY

    w = await workers.get(uid=str(ctx.author.id)).work
    await ctx.send(f"you got {salary} coins after working as {w}")
    w = "wallet"
    await self.give_money(w, ctx.author.id, salary,)


  @work.subcommand(name="as",)
  async def work_as(self, ctx, work):
    if work.lower() in WORKS:
      ch[str(ctx.author.id)] = work
      await ctx.send(f"You are working as {work} now")
      await self.give_work(ctx.author.id, work)
    else:
      await ctx.send(
          f"this is not valid work.\nSee a list of work by `{ctx.clean_prefix}work list`"
      )

  @work.subcommand(name="list")
  @commands.cooldown(0, 0, commands.BucketType.user)
  async def works_list(self, ctx):
    w = discord.Embed(
      description="\n".join(list(w.title() for w in WORKS))
    )
    w.set_footer(text=f"choose a work by `{ctx.clean_prefix}work as <work>`")
    await ctx.send(embed=w)


  @appcommands.command(name="deposit")
  async def dep(self, ctx, amount: int):
    am = amount
    u = await balance.get_or_none(uid=str(ctx.author.id))
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
      k = kk
      if am > 500:
        await ctx.reply("you only have 500 coins in your wallet to deposit", ephemeral=True)
      else:
        await ctx.reply(f'Depositing {am} coins in your bank...')
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(f"Successfully deposited {am} coins to your bank")

  @appcommands.command(name="withdraw")
  async def with_cmd(self, ctx, amount: int):
    am = amount
    u = await balance.get_or_none(uid=str(ctx.author.id))
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
      await ctx.reply("You don't have any money in your bank to withdraw, go deposit it first", ephemeral=True)
      await self.open_acc(ctx.author.id,)

  @appcommands.command(name="share",)
  async def share_cmd(self, ctx, user: discord.Member, amount: int):
    am=amount
    u = await balance.get_or_none(uid=str(ctx.author.id))
    if u:

      if am > int(u.hand):
        await ctx.send("you don't have enough money in your wallet to share", ephemeral=True)
        return
      else:
        pass

      w = "wallet"
      await self.take_money(w, ctx.author.id, am,)
      await self.give_money(w, user.id, am,)
      await ctx.send(f"you gave {am} coins to {user.mention}")
    else:
      await self.open_acc(ctx.author.id,)
      await ctx.send("I just opened your account so please now try again", ephemeral=True)


def setup(bot):
  bot.add_cog(eco(bot))
