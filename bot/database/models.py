from tortoise.models import Model
from tortoise import fields


class Event(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255, null=True, default=None)
    name = fields.CharField(max_length=255)
    car = fields.CharField(max_length=255)
    plate_number = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=255)
    vip = fields.CharField(max_length=255, null=True, default=None)

    class Meta:
        table = 'events'
