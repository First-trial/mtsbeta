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


_emoji_data = open("emojis.json")
emoji_data  = {}
for emoji, data in _emoji_data.values():
  _=[]
  for alias in data.get("aliases",[emoji]) or [emoji]:
    _.append(alias)
    _data = data.copy()
    if "aliases" in _data: del _data["aliases"]
    emoji_data[alias] = _data

  if "aliases" in data: del data["aliases"]
  if emoji not in _: emoji_data[emoji] = data

del _emoji_data

class Emoji(str):
  def __init__(self, name: str, id: int, *, animated: bool = False):
    self.name, self.id, self.animated = name, id, animated
    em="<{a}{name}:{id}>".format(name=self.name,id=str(self.id))
    em = em.format(a=("a:" if animated else ""))
    super().__init__(em)

class _Emote(object):
  __slots__ = tuple(i for i in emoji_data.keys())

Emote = _Emote()
for emoji, data in emoji_data.values():
  setattr(Emote, emoji, Emoji(**data))

del emoji_data
del _Emote
