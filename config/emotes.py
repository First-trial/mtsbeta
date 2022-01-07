import json

_emoji_data: dict = json.load(open("config/emojis.json"))
emoji_data  = {}

del json

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
      del cls_attrs["emojis"]
      cls = super().__new__(meta, clsname, bases, cls_attrs)
      for emoji in attributes["emojis"]:
        n = list(emoji.values())[0]
        full = "<{a}{name}:{id}>".format(
          name=n["name"],
          id=str(n["id"])
        ).format(
          a=("a:" if n["animated"] else "")
        )
        r_emoji = Emoji(full)
        r_emoji.full = full
        for slot in cls.__slots__:
          if slot is not "full":
            setattr(
              r_emoji,
              slot,
              list(emoji.values())[0][slot]
            )
        setattr(cls, list(emoji.keys())[0], r_emoji)

  class _Emote(metaclass=_M):
    emojis = list({emoji: data} for emoji, data in emoji_data.items())

  return _Emote()

del emoji_data
del _emote
