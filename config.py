from os import environ as env

tog_gg = env.get("top_gg")
token = env.get("token")

from tortoise.backends.base.config_generator import expand_db_url
tortoise = {
  "connections": {
    "default": expand_db_url(env.get("psql")),
    "apps": {
      "default": {
        "models": [
          "models"
        ]
      }
    }
  }
}
tortoise["connection"]["default"]["credentials"]["ssl"] = "disable"
sbl = env.get("sbl") # token for https://smartbots.tk