from django.db.models import Model, CharField, DateTimeField, CASCADE, ForeignKey, PROTECT, IntegerField
from django.utils import timezone
from yatra.models.user import User


class Hotel(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'hotels')
    name = CharField(max_length=20, unique=True)
    location = CharField()

class RoomType(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'room_type')
    name = CharField(max_length=20, unique=True)

class Room(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'room')
    number = CharField(max_length=10)
    type = ForeignKey(RoomType, PROTECT, 'rooms')
    capacity = IntegerField(db_index=True)
    hotel = ForeignKey(Hotel, CASCADE, 'rooms')

    class Meta:
        unique_together = ('number', 'hotel')

class UserRoom(Model):
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey(User, PROTECT, 'user_room_relation')
    user = ForeignKey(User, CASCADE, 'rooms')
    room = ForeignKey(Room, PROTECT, 'users')