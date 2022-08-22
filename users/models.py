import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def update_user(self, email, first_name, last_name, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.save()
        return user

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

    def get_all_users(self):
        try:
            return UserProfile.objects.get_all_users()
        except UserProfile.DoesNotExist:
            return None
    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        upload_to='user/', default='user/default.png')
    phone = models.CharField(max_length=100)

    class Roles(models.IntegerChoices):
        Adminstrador = 1
        Vendedor = 2
        Comprador = 3

    id_rol = models.IntegerField(choices=Roles.choices)

    slug = models.SlugField(max_length=255, unique=True)

    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.username)
        super(UserProfile, self).save(*args, **kwargs)