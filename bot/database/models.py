from tortoise.models import Model
from tortoise import fields


class Event(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=255)
    car = fields.CharField(max_length=255)
    plate_number = fields.CharField(max_length=255, unique=True)
    phone_number = fields.CharField(max_length=255)

    class Meta:
        table = 'events'
