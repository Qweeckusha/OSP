#main_admin\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import main_admin_page, create_user, add_to_queue, admin_U_page, admin_C_page, reset_queues, edit_students, \
    edit_students_process, delete_students, call_ten_students_university, call_ten_students_college, login_users, \
    create_admin, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
urlpatterns = [
    path('', main_admin_page, name='admin_page'),
    path('save/', create_user, name='save_data'),
    path('call_ten_students_U/', call_ten_students_university, name='call_ten_students_university'),
    path('call_ten_students_C/', call_ten_students_college, name='call_ten_students_college'),
    path('reset_queues/', reset_queues, name='reset_queues'),
    path('add_to_queue/', add_to_queue, name='add_to_queue'),
    path('edit_students/', edit_students, name='edit_students'),
    path('process/', edit_students_process, name='editing'),
    path('deleting/', delete_students, name='deleting'),
    path('adminUniversity/', admin_U_page, name='adminU'),
    path('adminCollege/', admin_C_page, name='adminC'),
    path('registr_admin/', create_admin, name='registr_admin'),
    path('api/', include(router.urls)),
]
