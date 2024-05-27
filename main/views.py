#main\views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from main_admin.models import CustomUser

@never_cache
@login_required
def main_user_page(request):
    queues = CustomUser.objects.all()
    user = request.user
    return render(request, 'main/index.html', {'queues': queues, 'user': user})

@never_cache
@login_required
@user_passes_test(lambda u: u.is_staff)
def tv_user(request):
    queues = CustomUser.objects.all()
    user = request.user
    return render(request, 'main/TV.html', {'queues': queues, 'user': user})
