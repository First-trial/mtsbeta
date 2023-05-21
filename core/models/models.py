from tortoise import fields
from tortoise.models import Model





class balance(Model):
  class Meta:
    table="bbal"
  uid = fields.BigIntField(unique=True)
  hand = fields.BigIntField()
  bank = fields.BigIntField()
  def to_dict(self):
    return {'uid':self.uid,'bank':self.bank,'hand':self.hand}

class workers(Model):
  class Meta:
    table="bwor"
  uid = fields.BigIntField(unique=True)
  work = fields.TextField()
  def to_dict(self):
    return {'uid':self.uid,'work':self.work}

class inventory(Model):
  class Meta:
    table="binv"
  item_uid = fields.CharField(110, unique=True)
  count = fields.BigIntField()
  def to_dict(self):
    return {'item_uid':self.item_uid,'count':self.count}

class UserLanguage(Model):
  class Meta:
    table = "buser_language"

  uid = fields.BigIntField(unique=True)
  language = fields.TextField(default="english")
  def to_dict(self):
    return {'uid':self.uid, "language":self.language}

  @classmethod
  def edit(cls, uid, language):
    return cls.get(uid=uid).update(language=language)
