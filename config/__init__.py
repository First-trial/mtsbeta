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


del env
