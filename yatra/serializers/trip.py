from rest_framework import serializers
from yatra.models.trip import Trip
from yatra.serializers.user import UserSerializer


class TripSerializer(serializers.ModelSerializer):
    # created_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    created_by = UserSerializer(fields=['name', 'id'], read_only=True)

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