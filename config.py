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
  __slots__ = ("name","id","animated")
  def __init__(self, name, id, *, animated: bool = False):
    self.name, self.id, self.animated = name, id, animated
    em="<{a}{name}:{id}>".format(name=self.name,id=str(self.id),a=("a:" if animated else ""))
    super().__init__(em); return self

  def json(self):
    return {
      "name": self.name,
      "id": int(self.id),
      "animated": self.animated
    }

class _Emote:
  def __init__(self):
    self.__emojis = []

  def add_emoji(self, n, emoji):
    if emoji not in self.__emojis: self.__emojis.append(emoji)
    setattr(self, n, emoji)
    
  def json(self):
    r={}
    for i in self.__emojis: r[i.name] = i.json()
    return r

Emote = _Emote()
for emoji, data in emoji_data.items():
  Emote.add_emoji(emoji, Emoji.__init__(Emoji,**data))

del emoji_data
del _Emote
