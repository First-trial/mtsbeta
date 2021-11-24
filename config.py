from os import environ as env

top_gg = env.get("top_gg")
token = env.get("token")

from tortoise.backends.base.config_generator import expand_db_url
tortoise = {
  "connections": {
    "default": expand_db_url(env.get("psql")),
  },
  "apps": {
    "default": {
      "models": [
        "models"
      ]
    }
  }
}
tortoise["connections"]["default"]["credentials"]["ssl"] = "disable"
sbl = env.get("sbl") # token for https://smartbots.tk