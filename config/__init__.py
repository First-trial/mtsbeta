import os
from .emotes import Emote

from os import environ as env

#env.update()
top_gg = env.get("top_gg")
token = env.get("token")
# postgres_database_url = env.get("psql")
db=env.get('TempDb')

from tortoise.backends.base.config_generator import expand_db_url


tortoise = {
  "connections": {
 #   "default": expand_db_url(postgres_database_url),
    "default": expand_db_url(db)
  },
  "apps": {
    "default": {
      "models": [
        "models"
      ]
    }
  }
}

del expand_db_url

tortoise["connections"]["default"]["credentials"]["ssl"] = "disable"
sbl = env.get("sbl") # token for https://smartbots.tk



DISCORD_JOIN_URL  = "https://discord.gg/zdrSUu98BP"
DISCORD_GUILD_ID  = 731072681688039444
ERROR_LOG_CHANNEL = 864372513198178304
TESTING_GUILD_IDS = [821599275929567232, 803824283897823253]

OWNER_ID = 730454267533459568 # will self-generate if not given
AUTHOR_ID = OWNER_ID # main developer
AUTHOR_IDS = [730454267533459568, 1109466227140743239] # all developers
BOT_ID = "" # will self-generate
BOT_INVITE_URL = "" # will self-generate if not given

async def generate(bot):
  owner = (await bot.application_info()).owner.id
  def change(k,v): globals()[k]=v
  change("BOT_ID",bot.user.id)

  if not OWNER_ID:
    change("OWNER_ID",owner)
  elif not AUTHOR_IDS:
    bot.owner_id = OWNER_ID

  if not AUTHOR_ID:
    change("AUTHOR_ID",owner)

  if not AUTHOR_IDS:
    change("AUTHOR_IDS",[owner])
  else:
    bot.owner_ids = AUTHOR_IDS
    
  if not BOT_INVITE_URL:
    change(
      "BOT_INVITE_URL",
      "https://discord.com/oauth2/authorize?"
      f"client_id={BOT_ID}&scope=bot+applications.commands"
      f"&permissions=8"
    )

# Jishaku Flags

flags = [
  "no underscore",
  "hide",
  "retain",
  "force paginator",
  "no dm_traceback",
]

for flag in flags: env[("jishaku_"+flag).upper().replace(" ","_")] = "t"
del flags

