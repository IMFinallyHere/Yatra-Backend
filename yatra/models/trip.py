from django.db.models import PROTECT, Model, CharField, DateTimeField, BooleanField, ForeignKey
from django.utils import timezone
from yatra.models.user import User


class Trip(Model):
    created_on = DateTimeField(default=timezone.now, db_index=True)
    created_by = ForeignKey(User, PROTECT, 'trips')
    name = CharField(max_length=50, unique=True)
    started = BooleanField(default=False)
    started_on = DateTimeField(null=True)
    ended = BooleanField(default=False)
    ended_on = DateTimeField(null=True)