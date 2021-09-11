from tortoise import fields
from tortoise.models import Model


class reminders(Model):
	id = fields.BigIntField(pk=True)
	expires = fields.DatetimeField(index=True)
	created = fields.DatetimeField(auto_now=True)
	event = fields.TextField()
	extra = fields.JSONField(default=dict)

	@property
	def kwargs(self):
		return self.extra.get("kwargs", {})

	@property
	def args(self):
		return self.extra.get("args", ())

class balance(Model):
  class Meta:
    table = 'bal'

  uid = fields.TextField()
  hand = fields.TextField()
  bank = fields.TextField()

class inv(Model):
  uid = fields.TextField()
  item = fields.TextField()
  count = fields.TextField()

class dukaan(Model):
  class Meta:
    table = 'shop'

  uid = fields.TextField()
  item = fields.TextField()
  cost = fields.TextField()

class snipes:
  channel_id = fields.BigIntField(pk=True)
  author_id = fields.BigIntField()
  content = fields.TextField()
  delete_time = fields.DatetimeField(auto_now=True)

  @property
  def author(self):
      return self.bot.get_user(self.author_id)

