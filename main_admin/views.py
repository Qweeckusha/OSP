from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .backends import AdminAuthBackend, QueueAuthBackend
from .forms import LoginForm, LoginFormAdmin, RegFormAdmin
from .models import CustomUser, Counter, AdminUser


@login_required
@user_passes_test(lambda u: u.is_staff)
def main_admin_page(request):
    try:
        queues = CustomUser.objects.all()
        return render(request, 'main_admin/index.html', {'queues': queues})
    except:
        print('Что-то не так')
def admin_U_page(request):
    queues = CustomUser.objects.all()
    return render(request, 'main_admin/admin_U.html', {'queues': queues})

def admin_C_page(request):
    queues = CustomUser.objects.all()
    return render(request, 'main_admin/admin_C.html', {'queues': queues})

def add_to_queue(request):
    return render(request, 'main_admin/add_to_queue.html')

def edit_students(request):
    return render(request, 'main_admin/edit.html')


@require_POST
def create_user(request):
    # Получаем данные из POST-запроса
    last_name = request.POST.get('last_name')
    first_name = request.POST.get('first_name')
    middle_name = request.POST.get('middle_name')
    affiliation = request.POST.get('affiliation')

    # Получаем модель пользователя
    CustomUser = get_user_model()

    # Получаем или создаем объект счетчика
    counter, created = Counter.objects.get_or_create(id=1)

    # Обновляем счетчик в зависимости от принадлежности
    if affiliation == 'Университет':
        counter.university_counter += 1
        queue_id = f'У{counter.university_counter}'
    else:
        counter.college_counter += 1
        queue_id = f'К{counter.college_counter}'

    # Сохраняем изменения в счетчике
    counter.save()

    # Создаем нового пользователя
    CustomUser.objects.create_user(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        affiliation=affiliation,
        queue_id=queue_id
    )

    return redirect('admin_page')

@require_POST
def reset_queues(request):
    # Удаление всех записей из таблицы CustomUser
    CustomUser.objects.all().delete()

    admins = AdminUser.objects.all()
    for admin in admins:
        if admin.username not in ['collector', 'adminU', 'adminC']:
            admin.delete()

    # Сброс счетчика автоинкремента (если используется база данных, поддерживающая автоинкремент)
    # Важно: этот код работает только для определенных типов баз данных, таких как SQLite.

    counter, _ = Counter.objects.get_or_create(id=1)
    counter.university_counter = 0
    counter.college_counter = 0
    counter.save()

    from django.db import connection
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", ['main_admin_customuser'])
        except Exception as e:
            print("Error deleting from sqlite_sequence for main_admin_customuser:", e)

    # После сброса перенаправляем пользователя на страницу администратора
    return redirect('admin_page')

@require_POST
def edit_students_process(request):
    # Получаем данные из запроса
    student_id = int(request.POST.get('ID'))
    last_name = request.POST.get('last_name')
    first_name = request.POST.get('first_name')
    middle_name = request.POST.get('middle_name')

    # Находим студента по ID
    try:
        student = CustomUser.objects.get(id=student_id)
    except CustomUser.DoesNotExist:
        return render(request, 'main_admin/edit.html', {'error': 'Студент не найден.'})

    # Обновляем данные студента
    student.last_name = last_name
    student.first_name = first_name
    student.middle_name = middle_name
    student.save()

    # После редактирования перенаправляем пользователя на страницу администратора
    return redirect('admin_page')

@require_POST
def delete_students(request):
    student_queue = request.POST.get('queue_id')

    try:
        student = CustomUser.objects.get(queue_id=student_queue)
    except CustomUser.DoesNotExist:
        return render(request, 'main_admin/edit.html', {'error': 'Студент не найден.'})

    student.delete()

    return redirect('admin_page')

@require_POST
def call_ten_students_university():
    # Получаем первые 10 записей из очереди университета
    studs_to_call = CustomUser.objects.filter(affiliation='Университет')[:10]

    # Это пока заглушка
    # TODO: Сделать так, чтобы записи удалялись после того, как вызовут следующую 10, а перед ними подсвечивать
    #  другим цветом, выделять
    for stud in studs_to_call:
        stud.delete()

    # После удаления перенаправляем пользователя на страницу администратора
    return redirect('adminU')


@require_POST
def call_ten_students_college():
    # Получаем первые 10 записей из очереди университета
    studs_to_call = CustomUser.objects.filter(affiliation='Колледж')[:10]

    # Это пока заглушка
    for stud in studs_to_call:
        stud.delete()

    # После удаления перенаправляем пользователя на страницу администратора
    return redirect('adminC')

@never_cache
def login_users(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form_admin = None
        if form.is_valid():
            queue_id = form.cleaned_data['queue_id']
            user = QueueAuthBackend().authenticate(request, queue_id=queue_id)
            if user is not None:
                login(request, user, backend='main_admin.backends.QueueAuthBackend')
                return redirect('main')  # Перенаправление на главную страницу после успешного входа
            else:
                # Отображение сообщения об ошибке, если пользователь не найден
                error_message = "Неверные учетные данные. Пожалуйста, попробуйте еще раз."
                return render(request, 'main_admin/login.html', {'form_admin': form_admin, 'form': form, 'error_message': error_message})

    return render(request, 'main_admin/login.html', {'form': LoginForm()})

@never_cache
def login_admins(request):
    if request.method == 'POST':
        form_admin = LoginFormAdmin(request.POST)
        if form_admin.is_valid():
            username = form_admin.cleaned_data['username']
            password = form_admin.cleaned_data['password']

            user = AdminAuthBackend().authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='main_admin.backends.AdminAuthBackend')
                if username == 'collector':
                    return redirect('admin_page')
                elif username == 'adminU':
                    return redirect('adminU')
                elif username == 'adminC':
                    return redirect('adminC')
            else:
                # Отображение сообщения об ошибке, если пользователь не найден
                error_message = "Неверные учетные данные. Пожалуйста, попробуйте еще раз."
                return render(request, 'main_admin/login_admin.html', {'form_admin': form_admin, 'error_message': error_message})
    return render(request, 'main_admin/login_admin.html', {'form_admin': LoginFormAdmin()})


def create_admin(request):
    if request.method == 'POST':
        form = RegFormAdmin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            key = form.cleaned_data['key']
            print(username, password)

            if key == 'gT9uJ5sNpE4q':
                AdminUser.objects.create_adminuser(username=username, password=password)
                return redirect('login_admins')
            else:
                return render(request, 'main_admin/registr_admin.html', {'error': 'Неверный ключ', 'form': RegFormAdmin()})
        else:
            print('Форма неверная')
    else:  # Добавляем обработку GET-запросов для отображения формы
        form = RegFormAdmin()
    return render(request, 'main_admin/registr_admin.html', {'form': form})
