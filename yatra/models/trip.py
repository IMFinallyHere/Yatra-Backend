from django.db.models import PROTECT, Model, CharField, DateTimeField, BooleanField, ForeignKey, CASCADE
from django.utils import timezone
from yatra.models.user import User


class Trip(Model):
    created_on = DateTimeField(default=timezone.now, db_index=True)
    created_by = ForeignKey(User, PROTECT, 'trips_created')
    name = CharField(max_length=50, unique=True)
    started = BooleanField(default=False)
    started_on = DateTimeField(null=True)
    ended = BooleanField(default=False)
    ended_on = DateTimeField(null=True)

class UserTrip(Model):
    created_on = DateTimeField(default=timezone.now, db_index=True)
    created_by = ForeignKey(User, PROTECT, 'user_trips_created')
    user = ForeignKey(User, CASCADE, 'user_trips')
    trip = ForeignKey(Trip, CASCADE, 'trip_users')

    class Meta:
        unique_together = ('user', 'trip')