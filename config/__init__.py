from .emotes import Emote

from os import environ as env


top_gg = env.get("top_gg")
token = env.get("token")
postgres_database_url = env.get("psql")


from tortoise.backends.base.config_generator import expand_db_url


tortoise = {
  "connections": {
    "default": expand_db_url(postgres_database_url),
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



DISCORD_JOIN_URL = "https://discord.gg/zdrSUu98BP"
DISCORD_GUILD_ID = 731072681688039444

OWNER_ID = "" # will self-generate if not given
AUTHOR_ID = OWNER_ID # mass developer
AUTHOR_IDS = [] # all developers
BOT_ID = "" # will self-generate
BOT_INVITE_URL = "" # will self-generate if not given

def generate(bot):
  change = lambda k,v: globals()[k]=v
  change("BOT_ID",bot.user.id)

  if not OWNER_ID:
    change("OWNER_ID",bot.owner_id)
  else:
    bot.owner_id = OWNER_ID

  if not AUTHOR_ID:
    change("AUTHOR_ID",bot.owner_id)

  if not AUTHOR_IDS:
    change("AUTHOR_IDS",[bot.owner_id])

  if not BOT_INVITE_URL:
    change(
      "BOT_INVITE_URL",
      "https://discord.com/oauth2/authorize?"
      f"client_id={BOT_ID}&scope=bot+applications.commands"
      f"&permissions=8"
    )

# Jishaku Flags

flags = [
  "jishaku_no underscore",
  "jishaku hide",
  "jishaku retain",
  "jishaku_force paginator",
  "jishaku_no_dm traceback",
]

for flag in flags: env.get]flags.upper().replace(" ","_")] = "t"
del flags
