#main\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import main_user_page
from main_admin.views import main_admin_page, login_users, login_admins, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
urlpatterns = [
    path('', main_user_page, name='main'),
    path('login/', login_users, name='login'),
    path('login_admin/', login_admins, name='login_admins'),
    path('api/', include(router.urls))
]
