from rest_framework import serializers
from yatra.serializers.trip import TripSerializer
from yatra.serializers.user import UserSerializer
from yatra.models.trip import Trip
from yatra.models.bus import Bus, UserBus


class BusSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['name', 'id'], read_only=True)
    trip = TripSerializer(fields=['name', 'id'], read_only=True)
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', queryset=Trip.objects.all(), write_only=True)

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
        model = Bus
        fields = '__all__'

class UserBusSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['name', 'id'], read_only=True)
    bus = BusSerializer(fields=['id', 'number'], read_only=True)
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
        model = UserBus
        fields = '__all__'