from tortoise import fields
from tortoise.models import Model


class balance(Model):
  uid = fields.BigIntField(unique=True)
  hand = fields.BigIntField()
  bank = fields.BigIntField()

class workers(Model):
  uid = fields.BigIntField(unique=True)
  work = fields.TextField()

class inventory(Model):
  item_uid = fields.CharField(110, unique=True)
  count = fields.BigIntField()

class GLanguage(Model):
  class Meta:
    table = "guild_language"

  gid = fields.BigIntField(unique=True)
  language = fields.TextField(default="english")

  @classmethod
  def edit(cls, gid, language):
    return cls.get(gid=gid).update(language=language)
