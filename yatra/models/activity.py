from django.db.models import Model, CharField, DateTimeField, BooleanField, CASCADE, ForeignKey, Index, PROTECT
from django.utils import timezone
from yatra.models.trip import Trip
from yatra.models.user import User


class Activity(Model):
    created_on = DateTimeField(default=timezone.now, db_index=True)
    created_by = ForeignKey(User, PROTECT, 'activities')
    name = CharField(max_length=50)
    trip = ForeignKey(Trip, CASCADE, 'activities')
    started = BooleanField(default=False)
    started_on = DateTimeField(null=True)
    ended = BooleanField(default=False)
    ended_on = DateTimeField(null=True)

    class Meta:
        unique_together = ('name', 'trip')

class UserActivity(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'user_activity_relation')
    user = ForeignKey(User, CASCADE, 'activities')
    activity = ForeignKey(Activity, CASCADE, 'users')
    checked_in = BooleanField(default=False)
    checked_in_on = DateTimeField(default=timezone.now)
    checked_out = BooleanField(default=False)
    checked_out_on = DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            Index(fields=["activity", "checked_in"]),
        ]