from django.db.models import Model, CharField, DateTimeField, BooleanField, CASCADE, ForeignKey, JSONField, Index, PROTECT
from django.utils import timezone
from yatra.models.user import User


class Bus(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'buses')
    name = CharField(max_length=50)
    number = CharField(max_length=15, db_index=True)
    metadata = JSONField(default=dict)

class UserBus(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'user_bus_relation')
    user = ForeignKey(User, CASCADE, 'buses')
    bus = ForeignKey(Bus, CASCADE, 'users')
    checked_in = BooleanField(default=False)
    checked_in_on = DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('bus', 'user')
        indexes = [
            Index(fields=["bus", "checked_in"]),
        ]