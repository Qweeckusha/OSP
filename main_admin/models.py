#main_admin/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager, AdminUserManager


class Counter(models.Model):
    university_counter = models.IntegerField(default=0)
    college_counter = models.IntegerField(default=0)

class CustomUser(AbstractUser):
    # Добавьте поля для ФИО
    username = None
    queue_id = models.CharField(max_length=10, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=12)
    USERNAME_FIELD = 'queue_id'

    # Добавьте атрибут related_name для избежания конфликта имен
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = CustomUserManager()

class AdminUser(AbstractUser):
    objects = AdminUserManager()