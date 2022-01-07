import json
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


_emoji_data: dict = json.load(open("emojis.json"))
emoji_data  = {}

del json
del env

for emoji, data in _emoji_data.items():
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
  __slots__ = ("name","id","animated",)
  full = ""
  def json(self):
    return {
      "name": self.name,
      "id": int(self.id),
      "animated": self.animated
    }

def _emote():
  class _M(type):
    def __new__(meta, clsname, bases, attributes: dict):
      cls_attrs = attributes.copy()
      del cls_attrs["emojis"]
      cls = super().__new__(meta, clsname, bases, cls_attrs)
      for emoji in attributes["emojis"]:
        n = list(emoji.value())[0]
        if         r_emoji = Emoji()
        for r_emoin ji
  cl.__slots__:
          setattr(r_emoji,slot,list(emoji.values())[0][slot])ass _Emote(metaclass=_M):
    pass

for emoji, data in emoji_data.items():
  Emote.add_emoji(emoji, Emoji(**data))

del emoji_data
del _Emote
