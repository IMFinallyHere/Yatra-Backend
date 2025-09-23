from django.core.validators import MinLengthValidator
from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    @transaction.atomic
    def create_user(self, number, password=None, **extra_fields):
        user = self.model(number=number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    last_name = None
    last_login = None
    first_name = None
    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name']

    name = models.CharField(max_length=100, null=False, blank=False)
    number = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} - {self.number}"