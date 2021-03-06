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

class UserLanguage(Model):
  class Meta:
    table = "user_language"

  uid = fields.BigIntField(unique=True)
  language = fields.TextField(default="english")

  @classmethod
  def edit(cls, uid, language):
    return cls.get(uid=uid).update(language=language)
