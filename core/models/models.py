from typing import Any
from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import Field


class balance(Model):
  uid = fields.BigIntField(unique=True)
  hand = fields.BigIntField()
  bank = fields.BigIntField()

class workers(Model):
  uid = fields.BigIntField(unique=True)
  work = fields.TextField()
  
class ListField(Field, list):
  def __init__(self, field: Field, **kwargs) -> None:
    super().__init__(**kwargs)
    self.sub_field = field
    self.SQL_TYPE = "%s[]" % field.SQL_TYPE


  def to_python_value(self, value: Any) -> Any:
    return list(map(self.sub_field.to_python_value, value))


  def to_db_value(self, value: Any, instance: Any) -> Any:
    return [self.sub_field.to_db_value(val, instance) for val in value]
