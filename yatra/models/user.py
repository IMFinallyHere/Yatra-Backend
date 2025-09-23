from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import transaction
from django.db.models import CharField, DateTimeField, BooleanField, CASCADE, ForeignKey, Model
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

    name = CharField(max_length=100, null=False, blank=False)
    number = CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    is_active = BooleanField(default=True)
    created_on = DateTimeField(default=timezone.now)
    created_by = ForeignKey('self', on_delete=CASCADE, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} - {self.number}"

class UserPartner(Model):
    """
    This table keeps records of a family group i.e partners.
    So from one account you can add as many partners as you want. So kids don't require phones to be on trip.
    """
    created_on = DateTimeField(default=timezone.now)
    user = ForeignKey(User, CASCADE, 'partners')
    name = CharField(max_length=100)
    number = CharField(null=True, max_length=10)
