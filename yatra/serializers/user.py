from dataclasses import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
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
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    password = serializers.CharField(write_only=True)
    groups = GroupSerializer(fields=['name', 'id'], many=True, read_only=True)
    created_by = serializers.SerializerMethodField()

    @staticmethod
    def get_created_by(obj):
        if obj.created_by:
            return UserSerializer(obj.created_by, fields=['name', 'id']).data
        return None

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
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'number', 'password')

    @transaction.atomic
    def create(self, validated_data):
        req = self.context.get('request')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data, created_by=req.user)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    number = serializers.CharField(required=True)

    def validate(self, attrs):
        number = attrs.get('number')
        password = attrs.get('password')

        try:
            user: User = User.objects.get(number=number)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')

        if check_password(password, user.password):
            refresh = self.get_token(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'number': user.number,
                'groups': GroupSerializer(user.groups.all(), fields=['id', 'name'], many=True).data,
            }
        else:
            raise serializers.ValidationError('Invalid credentials.')

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # gives { "access": "..." }

        refresh = RefreshToken(attrs["refresh"])
        user = User.objects.get(id=refresh["user_id"])  # extract user from refresh token payload

        # add the extra fields like in obtain
        data.update({
            "user_id": user.id,
            "number": user.number,
            "groups": GroupSerializer(user.groups.all(), fields=["id", "name"], many=True).data,
        })
        return data