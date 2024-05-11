#main_admin\backends.py
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser, AdminUser


class QueueAuthBackend(BaseBackend):
    def authenticate(self, request, queue_id=None):
        try:
            user = CustomUser.objects.get(queue_id=queue_id)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

class AdminAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            admin_user = AdminUser.objects.get(username=username)
            if admin_user.check_password(password):
                return admin_user
            else:
                return None
        except AdminUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None
