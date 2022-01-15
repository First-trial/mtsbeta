import json

_emoji_data: dict = json.load(open("config/emojis.json"))
emoji_data  = {}
def_ems = {}

del json

for emoji, data in _emoji_data.items():
  if emoji == "defaults":
    for emojin, emojiv in data.items():
      globals()["def_ems"][emojin] = emojiv

    continue

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
  __slots__ = ("name","id","animated", "full")

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
      cls_attrs["emojis"] = {}
      cls_attrs["defaults"] = {}
      cls = super().__new__(meta, clsname, bases, cls_attrs)
      for emoji in attributes["emojis"]:
        n = list(emoji.values())[0]
        full = "<{name}:{id}>".format(
          name="{a}"+n["name"],
          id=str(n["id"])
        )
        full=full.format(
          a=("a:" if n["animated"] else "")
        )
        r_emoji = Emoji(full)
        r_emoji.full = full
        for slot in Emoji.__slots__:
          if slot != "full":
            setattr(
              r_emoji,
              slot,
              list(emoji.values())[0][slot]
            )
        setattr(cls, list(emoji.keys())[0], r_emoji)
        cls.emojis[list(emoji.keys())[0]] = r_emoji

      for emojin, emojiv in attributes["defaults"].items():
        setattr(cls, emojin, emojiv)
        cls.emojis[emojin] = emojiv
        cls.defaults[emojin] = emojiv

      return cls

  class _Emote(metaclass=_M):
    emojis = list({emoji: data} for emoji, data in emoji_data.items())
    defaults = def_ems.copy()

    def json(self):
      resp = {}
      for emojin, emoji in self.emojis.items():
        resp[emojin] = emoji.json()
        
      return resp
  return _Emote()

Emote = _emote()
del emoji_data
del _emote
del def_ems
