# main_admin/serializers.py
from rest_framework import serializers
from main_admin.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
