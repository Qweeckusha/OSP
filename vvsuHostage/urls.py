#vvsuHostage\urls.py
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('admin_panel/', include('main_admin.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
