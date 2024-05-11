#main\urls.py
from django.urls import path
from .views import main_user_page
from main_admin.views import main_admin_page, login_users, login_admins

urlpatterns = [
    path('', main_user_page, name='main'),
    path('admin_page/', main_admin_page, name='admin_page'),
    path('login/', login_users, name='login'),
    path('login_admin/', login_admins, name='login_admins'),

]
