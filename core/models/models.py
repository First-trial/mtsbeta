from tortoise import fields
from tortoise.models import Model


class balance(Model):
  uid = fields.TextField(unique=True)
  hand = fields.TextField()
  bank = fields.TextField()

class workers(Model):
  uid = fields.TextField(unique=True)
  work = fields.TextField()
  
