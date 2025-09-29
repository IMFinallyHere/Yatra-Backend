from rest_framework import serializers
from yatra.models.trip import Trip, UserTrip
from yatra.serializers.user import UserSerializer


class TripSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['name', 'id'], read_only=True)
    activity_count = serializers.SerializerMethodField(read_only=True)
    bus_count = serializers.SerializerMethodField(read_only=True)
    user_count = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_activity_count(obj):
        return obj.activities.count()

    @staticmethod
    def get_bus_count(obj):
        return obj.buses.count()

    @staticmethod
    def get_user_count(obj):
        return sum(trip_user.user.partners.count() + 1 for trip_user in obj.trip_users.prefetch_related('user__partners').all()) # +1 for user itself

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', self.fields)
        exclude = set(kwargs.pop('exclude', []))
        super().__init__(*args, **kwargs)

        allowed = set(fields)
        existing = set(self.fields)
        for field_name in existing - allowed:
            self.fields.pop(field_name)

        if exclude:
            for field_name in exclude:
                self.fields.pop(field_name, None)

    class Meta:
        model = Trip
        fields = '__all__'

class UserTripSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['name', 'id'], read_only=True)
    user = UserSerializer(fields=['name', 'id'], read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', self.fields)
        exclude = set(kwargs.pop('exclude', []))
        super().__init__(*args, **kwargs)

        allowed = set(fields)
        existing = set(self.fields)
        for field_name in existing - allowed:
            self.fields.pop(field_name)

        if exclude:
            for field_name in exclude:
                self.fields.pop(field_name, None)

    class Meta:
        model = UserTrip
        fields = '__all__'