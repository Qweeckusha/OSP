# main_admin/managers.py
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, last_name, first_name, middle_name, affiliation, **extra_fields):
        """
        Создает и возвращает пользователя с указанными данными.
        """


        user = self.model(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            affiliation=affiliation,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        """
        Создает и возвращает суперпользователя с указанными данными.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(**extra_fields)

class AdminUserManager(BaseUserManager):
    def create_adminuser(self, username, password, **extra_fields):
        """
        Создает и возвращает администратора с указанным именем пользователя и паролем.
        """
        if not username:
            raise ValueError('Необходимо указать имя пользователя')

        admin_user = self.model(username=username, **extra_fields)
        admin_user.set_password(password)  # Установка захешированного пароля
        admin_user.is_staff = True
        admin_user.save(using=self._db)
        return admin_user