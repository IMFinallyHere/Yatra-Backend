from django.db.models import Model, CharField, DateTimeField, BooleanField, CASCADE, ForeignKey, JSONField, Index, PROTECT
from django.utils import timezone
from yatra.models.user import User
from yatra.models.trip import Trip


class Bus(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'buses_created')
    trip = ForeignKey(Trip, CASCADE, 'buses')
    number = CharField(max_length=15)
    metadata = JSONField(default=dict)

    class Meta:
        unique_together = ('trip', 'number')

class UserBus(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'user_bus_created')
    user = ForeignKey(User, CASCADE, 'buses')
    bus = ForeignKey(Bus, CASCADE, 'users')
    checked_in = BooleanField(default=False)
    checked_in_on = DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('bus', 'user')
        indexes = [
            Index(fields=["bus", "checked_in"]),
        ]