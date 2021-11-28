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
  uid = fields.BigIntField()
  item = fields.TextField()
  count = fields.BigIntField()
