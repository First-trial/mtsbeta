# plugin: loadable: True

import discord, asyncio
from discord.ext import commands
import appcommands
from models import balance, workers, inventory
from core import Cog
from appcommands import Option
from typing import List
from base64 import b64decode as _decode, b64encode as _encode
from config import languages


cns = [
  "abcdefghi",
  "jklmnopqr",
  "stuvwxyzA",
  "BCDEFGHIJ",
  "KLMNOPQRS",
  "TUVWXYZ01",
  "23456789=",
  "+/",
]

def decode(item_uid: str, seperator: str = "."):
  c,_="",0
  item_uid=str(item_uid)[1:]

  for i in item_uid:
    if _==0:
     fmt=cns[int(i)]
     _=1
    else:
     c+=fmt[int(i)]
     _=0
  cnt=_decode(bytes(c, encoding="utf-8")).decode("utf-8")
  assert seperator in cnt
  uid, item = cnt.split(seperator)
  return [int(uid), int(item)]

def encode(uid: int, item: int, seperator: str = "."):
  resp = "1"
  enc = _encode(bytes(str(uid)+"."+str(item), encoding="utf-8")).decode("utf-8")
  for c in enc:
    for n, cn in enumerate(cns):
      if c in cn:
        resp += str(n)+str(cn.index(c))

  return resp

class Item:
  def __init__(self,id:int,name:str,price:float,emoji:str=""):
    self.id,self.name,self.price,self.emoji=id,name,price,emoji

  def json(self):
    return {"id":self.id,"name":self.name,"price":self.price,"emoji":self.emoji}

  def __repr__(self):
    id=self.id
    if id == 1:
      fmt="st"
    elif id == 2:
      fmt="nd"
    elif id == 3:
      fmt="rd"
    else:
      fmt="th"

    return f"{self.id}{fmt} Item, {self.name} at {self.price} coins"

class Shop:
  def __init__(self):
    self.items: List[Item] = []

  def add_item(self, item: Item):
    assert isinstance(item, Item)
    if item in self.items:
      self.items.remove(item)

    self.items.append(item)

  def remove_item(self, item: Item):
    assert isinstance(item, Item)
    if item in self.items:
      self.items.remove(item)

  def get_item(self, k):
    for item in self.items:
      if item.name==str(k).lower().upper() or item==k or str(item.id)==str(k):
        return item

    return None

  def get(self, k):
    return self.get_item(k)

  def filter_items(self, price=1):
    assert isinstance(price, int) and price > 0
    resp=[]
    for item in self.items:
      if item.price==price:
        resp.append(item)

    return resp

  def filter(self,price=1):
    return self.filter_items()

  def filter_by(self,**kwargs):
    item_lookup=self.json()
    _resp,include,exclude,resp=[],[],[],[]
    attrs = ["id","name","price","emoji"]

    if "include" in kwargs:
      include.extend(kwargs["include"])
      del kwargs["include"]
    else:
      include=attrs

    if "exclude" in kwargs:
      exclude.extend(kwargs["exclude"])
      del kwargs["exclude"]

    resplen = len(list(kwargs.keys()))
    temp = 0
    if kwargs:
      for item in item_lookup:
        for k, v in kwargs.items():
          if item.get(k,) == v:
            temp += 1
        if temp == resplen:
          _resp.append(self.get(item["id"]))
        temp = 0
    else:
      _resp.extend(self.items)
    for item in _resp:
      class _Item(object):
        __slots__=tuple(i for i in attrs)
      _item=_Item()
      if len(include)>0:
        for i in include:
          setattr(_item, i, getattr(item, i, None))
      if len(exclude)>0:
        for i in exclude:
          delattr(_item, i,)
      if include==attrs and len(exclude)==0:
        resp.append(item)
      else:
        resp.append(_item)

    return resp

  def json(self):
    return [item.json() for item in self.items]

  def __repr__(self):
    return "A cool MtsBot's shop"

async def check_work(ctx):
  if not await workers.get_or_none(uid=str(ctx.author.id)):
    await ctx.send(
        f"You are not working\nPls choose your work by `{ctx.clean_prefix}work as <work>`",
        ephemeral=True
    )
    return False
  return True

OWNER_SALARY: int = 5000000
OTHER_SALARY: int = 1500
WORK_COOLDOWN: int = 60 * 30 # 30 minutes
WORKS: List[str] = [
  "youtuber",
  "coder",
  "housewife",
  "cosplayer",
  "memer",
  "farmer",
  "engineer",
  "ghost"
]

SHOP: Shop = Shop();i=1
SHOP.add_item(Item(i, "Popcorn", 20, ":popcorn:"));i+=1
SHOP.add_item(Item(i, "Milk", 40, ":milk:"));i+=1
SHOP.add_item(Item(i, "Apple", 80, ":apple:"));i+=1
SHOP.add_item(Item(i, "Cupcake", 100, ":cupcake:"));i+=1
SHOP.add_item(Item(i, "Banana", 120, ":banana:"));i+=1
SHOP.add_item(Item(i, "Computer", 35000, ":desktop:"));i+=1
SHOP.add_item(Item(i, "Laptop", 40000, ":computer:"))

WORKS: List[appcommands.Choice] = [appcommands.Choice(work.title()) for work in WORKS]

class Task(object):
  def __init__(self, id, task):
    self.id, self.task, self.cancelled = id, task, False

  def cancel(self):
    if not self.cancelled:
      self.task.cancel()
      self.cancelled = True

class CooldownBucket(dict):
  def __init__(self, loop, **kwargs):
    super().__init__(**kwargs)
    self.__loop = loop
    self.__tasks = []
    self.index = 0

  async def __do_bucket(self, k, v):
    while self[k] > 0:
      await asyncio.sleep(1)
      super().__setitem__(
        k,
        {
          "id": super().__getitem__(k)["id"],
          "item": self[k] - 1
        }
      )
    super().__delitem__(k)

  def __setitem__(self, k, v):
    assert isinstance(v, int), "value should must be int"

    if k in self:
      self.__tasks[super().__getitem__(k)["id"]].cancel()
    super().__setitem__(k, {"item": v, "id": self.index})

    task = Task(self.index, self.__loop.create_task(self.__do_bucket(k,v)))
    self.__tasks.append(task)
    self.index += 1

  def items(self,):
    return ((k, v["item"],) for k, v in super().items())

  def __getitem__(self, k):
    return super().__getitem__(k)["item"]

  def __delitem__(self, k):
    self.__tasks[super().__getitem__(k)["id"]].cancel()
    super().__delitem__(k)

  def clear_tasks(self,):
    for task in self.__tasks:
      task.cancel()

  def destroy(self):
    self.clear_tasks()
    _=[k for k in self]
    for k in _:
      del self[_]

    def N(*args, **kwargs):
      pass

    self.__getitem__ = N
    self.__setitem__ = N
    self.__delitem__ = N
    self.__del__ = N
    self.destroy = N
    self.clear_tasks = N

  def __del__(self, *args, **kwargs):
    self.destroy()
    super().__del__(*args, **kwargs)

class Economy(Cog):
  def __init__(self, bot):
    super().__init__(bot)
    self.buckets = CooldownBucket(bot.loop)

  def do_bucket(self,i,t):
    self.buckets[i] = t

  def cog_unload(self,):
    self.buckets.destroy()

  @commands.Cog.listener()
  async def on_ready(self):
    print("A wild economy system appeared")

  async def open_acc(self, id):
    await balance.create(uid=int(id), bank=0, hand=500); return True

  async def get_lang(self, ctx):
    return await ctx.get_lang()

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
        w -= money
        await self.up_usr(id, bank, w)
      else:
        w = int(u.hand)
        bank = int(u.bank)
        bank -= money
        await self.up_usr(id, bank, w)
    else:
      if area == "wallet":
        bank = 0
        money = 500 - money
        await self.up_usr(id, bank, money)
      else: await self.open_acc(id)


  economy = appcommands.slashgroup(name="economy", description="Economy commands")


  @economy.subcommand(name="balance", description="Check balance of your or someone other")
  async def economy_balance(self, ctx, user: discord.Member = None):
    usr=user or ctx.author
    language = (await self.get_lang(ctx)).economy.balance
    u = await balance.get_or_none(uid=usr.id)
    if u:
      wallet = u.hand
      bank = u.bank
      b = discord.Embed(
          title=f"{usr.name}{language.balance}",
          description=f"{language.wallet}: `{wallet} coins`\n{language.bank}: `{bank} coins`",color=0x00ffff)
      await ctx.reply(embed=b)
    else:
      await ctx.reply(language.new_acc)
      await self.open_acc(usr.id,)
      b = discord.Embed(
          title=f"{usr.name}{language.balance}",
          description=f"{language.wallet}: `500 coins`\n{language.bank}: `0 coins`",color=0x00ffff)
      await ctx.edit(content=None, embed=b)

  economy_work = economy.subcommandgroup(name="work", description="Commands related to jobs.")

  @economy_work.subcommand(name="now", description="Do some work")
  async def economy_work_now(self, ctx):
    language = (await self.get_lang(ctx)).economy.work.now
    if not await check_work(ctx):
      return

    if ctx.author.id not in self.buckets:
      self.do_bucket(ctx.author.id, WORK_COOLDOWN)
    else:
      c = round(self.buckets[ctx.author.id])
      if c > 60:
        c = str(round(c / 60))+" minutes"
      else:
        c = str(c)+" second"+("c" if int(c)>1 else "")
      return await ctx.send(language.err.cooldown.format(time=c), ephemeral=True)

    if ctx.author.id == self.author_id:
      salary = OWNER_SALARY
    else:
      salary = OTHER_SALARY

    w = (await workers.get(uid=ctx.author.id)).work
    await ctx.send(language.success.format(salary=str(salary),work=w))
    w = "wallet"
    await self.give_money(w, ctx.author.id, salary,)


  @economy_work.subcommand(name="as", description="Choose your work")
  async def economy_work_as(self, ctx, work: Option("-", "Chosee work", choices=WORKS, required=True)):
    language = (await self.get_lang(ctx)).economy.work.as_
    if work.lower() not in list(w.value.lower() for w in WORKS):
      await ctx.send(
        language.err.not_found.format(prefix=ctx.clean_prefix),
        ephemeral=True
      )
    if not await ctx.confirm(language.confirm.format(work=work)): return
    if not await self.give_work(ctx.author.id, work):
      await ctx.edit(content=language.err.resign.format(prefix=ctx.prefix))
    else:
      await ctx.edit(content=language.success.format(work=work))

  @economy_work.subcommand(name="resign", description="Resign from your work")
  async def economy_work_resign(self, ctx):
    language = (await ctx.get_lang()).economy.work.resign
    worker = workers.get_or_none(uid=ctx.author.id)
    work = await worker
    if not work:
      await ctx.send(language.err.choose.format(prefix=ctx.prefix), ephemeral=True)
    else:
      if not await ctx.confirm(language.confirm.format(work=work.work)): return
      await worker.delete()
      await ctx.send(language.success.format(work=work.work))


  @economy_work.subcommand(name="list", description="List of available jobs.")
  async def economy_work_list(self, ctx):
    language = (await ctx.get_lang()).economy.work.list_
    w = discord.Embed(
      title=f"**{language.success}**",
      description="\n".join(list(w.value.title() for w in WORKS)),
      color=0x00ffff
    )
    w.set_footer(text=f"You can choose a work by `{ctx.clean_prefix}work as <work>`")
    await ctx.send(embed=w)


  @economy.subcommand(name="deposit", description="Deposit some money in your bank.")
  async def economy_deposit(self, ctx, amount: int):
    language = (await ctx.get_lang()).economy.deposit
    am = amount
    if amount <= 0:
        return await ctx.send(language.err.minus_0.format(amount=str(am)), ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:
      a = "wallet"
      b = "bank"
      am = int(am)
      if am > int(u.hand):
        await ctx.reply(language.err.insufficient, ephemeral=True)
      else:
        await ctx.reply(language.success.depositing.format(coins=am))
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(content=language.success.deposited.format(coins=am))
    else:
      await self.open_acc(ctx.author.id,)
      a = "wallet"
      b = "bank"
      if am > 500:
        await ctx.reply(language.err.insufficient, ephemeral=True)
      else:
        await ctx.reply(language.success.depositing.format(coins=am))
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(content=language.success.deposited.format(coins=am))

  @economy.subcommand(name="withdraw", description="Withdraw some money from your bank")
  async def economy_withdraw(self, ctx, amount: int):
    language = (await ctx.get_lang()).economy.withdraw
    am = amount
    if amount <= 0:
        return await ctx.send(language.err.minus_0.format(amount=str(am)), ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:
      b = "wallet"
      a = "bank"
      am = int(am)
      if am > int(u.bank):
        await ctx.reply(language.err.insufficient, ephemeral=True)
      else:
        await ctx.reply(language.success.withdrawing.format(coins=am))
        await self.take_money(a, ctx.author.id, am,)
        await self.give_money(b, ctx.author.id, am,)
        await ctx.edit(content=language.success.withdrawed.format(coins=am))
    else:
      await ctx.reply(language.err.insufficient, ephemeral=True)
      await self.open_acc(ctx.author.id,)

  @economy.subcommand(name="share", description="Share your money to someone else")
  async def economy_share(self, ctx, user: discord.Member, amount: int):
    am, language=amount,(await ctx.get_lang()).economy.share
    if user.id == ctx.author.id:
      return await ctx.send(language.err.same, ephemeral=True)
    if amount <= 0:
        return await ctx.send(language.err.minus_0.format(amount=am), ephemeral=True)
    u = await balance.get_or_none(uid=ctx.author.id)
    if u:

      if am > int(u.hand):
        return await ctx.send(language.err.insufficient, ephemeral=True)

      w = "wallet"
      confirmed = await ctx.confirm(language.confirm.format(amount=am,user=user.mention))
      if not confirmed:
        return # user cancelled or didn't reacted within 15 seconds

      await self.take_money(w, ctx.author.id, am,)
      await self.give_money(w, user.id, am,)
      await ctx.edit(content = language.success.format(amount=am,user=user.mention))
    else:
      await self.open_acc(ctx.author.id,)
      await ctx.send(language.err.try_again, ephemeral=True)

  @economy.subcommand(name="shop",description="Get items of shop.")
  async def economy_shop(self, ctx, item: str = None):
    language = (await ctx.get_lang()).economy.shop

    if not item: d="\n".join([f"**{item.id}: {item.emoji} __{item.name}__** @ `{item.price}coins`" for item in SHOP.items])
    elif not SHOP.get(item): d=language.err.not_found.format(item=item)
    else: item=SHOP.get(item);d=f"**__ \u200b{item.emoji}{item.name}\u200b __**\n\n**Cost: **`{item.price}coins`"
    await ctx.send(embed=discord.Embed(title=f"**__{language.success}__**",description=d,color=0x00ffff))


  @economy.subcommand(name="inventory", description="Check inventory of your or someone else")
  async def economy_inventory(self, ctx, user: discord.Member = None):
    user = user or ctx.author
    language = (await ctx.get_lang()).economy.inventory

    id_lookup=SHOP.filter_by(include=["id"])
    fmt = []
    for iid in id_lookup:
      item=await inventory.get_or_none(item_uid=encode(user.id, iid.id))
      r_item = SHOP.get(iid.id)
      if item and r_item:
        fmt.append(f"{r_item.emoji} {r_item.name} — {item.count}")

    if not fmt:
      fmt = [language.err.nothing]

    if not await balance.get_or_none(uid=user.id):
      await self.open_acc(user.id)

    await ctx.send(
      embed=discord.Embed(
        title=user.display_name+language.success,
        description="\n".join(fmt),
        color=0x00ffff
      )
    )
    
def setup(bot):
  bot.add_cog(Economy(bot))
