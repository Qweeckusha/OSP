#main\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import main_user_page, tv_user
from main_admin.views import main_admin_page, login_users, login_admins, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
urlpatterns = [
    path('', main_user_page, name='main'),
    path('television/', tv_user, name='tv'),
    path('login/', login_users, name='login'),
    path('login_admin/', login_admins, name='login_admins'),
    path('api/', include(router.urls))
]
