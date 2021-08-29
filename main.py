from core import MtsBot
from os import environ as env

shards = [0,1,2,3,4,5]
async def get_pre(
  bot: MtsBot,
  msg
):
  if msg.author.id == bot.author_id:
    if msg.content.startswith(("Mts ", "mts ")):
      return ("Mts ","mts ")
    if bot.get_command(msg.content):
      return ""
    if msg.content.startswith("jsk"):
      return ""
      
  return ("Mts ","mts ")
  
  
bot = MtsBot(command_prefix=get_pre, shard_ids=shards, shard_count=6)

es = [
  "cogs.anim",
  "cogs.dbl",
  "cogs.eco",
  "cogs.games",
  "cogs.ipc",
  "cogs.newfile",
  "cogs.r",
  "cogs.ttt"
]
for e in es:
  bot.load_extension(e)

bot.run(env.get("token"))