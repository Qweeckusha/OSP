from datetime import timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from rest_framework import viewsets

from .backends import AdminAuthBackend, QueueAuthBackend
from .forms import LoginForm, LoginFormAdmin, RegFormAdmin
from .models import CustomUser, Analytics, AdminUser
from time import *

from .serializers import CustomUserSerializer


# ---------------------- renders ----------------------
@login_required
@user_passes_test(lambda u: u.is_staff)
@never_cache
def main_admin_page(request):
    try:
        queues = CustomUser.objects.all()
        return render(request, 'main_admin/index.html', {'queues': queues})
    except Exception as e:
        return HttpResponse(f'Что-то не так (main_admin_page): {str(e)}')
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

# -----------------------helping funcs------------------------------

def format_timedelta(td): # Форматирование строки времени в чч:мм:сс
    return str(td).split('.')[0]

def get_allAnalytics():
    try:
        visitors = Analytics.objects.get(id=1)
        analytics_objects_list = [Analytics.objects.filter(id__gte=2, is_university=False), Analytics.objects.filter(id__gte=2, is_university=True)]
        if analytics_objects_list:
            print('Всё ок!')
            summary = []
            for analytics_objects in analytics_objects_list:
                prev_time = None
                for analytics_object in analytics_objects:

                    if prev_time:
                        time_diff = analytics_object.start_time - prev_time
                        print(f'{analytics_object.start_time} - {prev_time} = {time_diff}')
                        summary.append(
                            {'start_time': prev_time, 'end_time': analytics_object.start_time, 'duration': time_diff}
                        )
                    prev_time = analytics_object.start_time

            durations_timedelta = [entry['duration'] for entry in summary]
            average_timedelta = sum(durations_timedelta, timedelta(0)) / len(durations_timedelta)
            max_duration = max(durations_timedelta)
            min_duration = min(durations_timedelta)
            counterAll = visitors.college_counter + visitors.university_counter

            return [format_timedelta(average_timedelta),
                    format_timedelta(max_duration),
                    format_timedelta(min_duration),
                    str(counterAll)]
        else:
            print('Почему так?')
            return ["Н/Д", "Н/Д", "Н/Д", "Н/Д"]
    except Exception as e:
        print(f'Ошибка в get_allAnalytics() {str(e)}')
        return ["Ошибка", "Ошибка", "Ошибка", "Ошибка"]

def get_analytics_data(is_university=False):
    try:
        Visitors = Analytics.objects.get(id=1)
        analytics_objects = Analytics.objects.filter(id__gte=2, is_university=is_university)
        if analytics_objects.exists():
            summary = []
            prev_time = None
            for analytics_object in analytics_objects:
                if prev_time:
                    time_diff = analytics_object.start_time - prev_time
                    summary.append(
                        {'start_time': prev_time, 'end_time': analytics_object.start_time, 'duration': time_diff}
                    )
                prev_time = analytics_object.start_time

            durations_timedelta = [entry['duration'] for entry in summary]
            average_timedelta = sum(durations_timedelta, timedelta(0)) / len(durations_timedelta)
            max_duration = max(durations_timedelta)
            min_duration = min(durations_timedelta)
            if is_university:
                studs_counter = Visitors.university_counter
            else:
                studs_counter = Visitors.college_counter

            return [format_timedelta(average_timedelta),
                    format_timedelta(max_duration),
                    format_timedelta(min_duration),
                    str(studs_counter)]
        else:
            print('Почему так?')
            return ["Н/Д", "Н/Д", "Н/Д", "Н/Д"]
    except Exception as e:
        print(f'Ошибка в help funcs (get_analytics_data) {str(e)}')
        return ["Ошибка", "Ошибка", "Ошибка", "Ошибка"]
# ------------------------------------------------------------------

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
    counter, created = Analytics.objects.get_or_create(id=1)
    try:
        if int(last_name[:2]) in range(10,100):
            for i in range(int(last_name[:2])):  #Крысерский жоский бэк для дабавления n челов до 99
                # Обновляем счетчик в зависимости от принадлежности
                if affiliation == 'Университет':
                    counter.university_counter += 1
                    queue_id = f'У{counter.university_counter}'
                else:
                    counter.college_counter += 1
                    queue_id = f'К{counter.college_counter}'

                # Сохраняем изменения в счетчике
                counter.save()
                CustomUser.objects.create_user(
                    last_name=last_name[2:],
                    first_name=first_name,
                    middle_name=middle_name,
                    affiliation=affiliation,
                    queue_id=queue_id
                )
    except:
        # Обновляем счетчик в зависимости от принадлежности
        if affiliation == 'Университет':
            counter.university_counter += 1
            queue_id = f'У{counter.university_counter}'
        else:
            counter.college_counter += 1
            queue_id = f'К{counter.college_counter}'

        # Сохраняем изменения в счетчике
        counter.save()

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
    key = request.POST.get('key')
    if key == '932468':
        # ------------------------------------------Сводка по сессии----------------------------------------------------
        try:
            stats = get_allAnalytics()
            stats_U = get_analytics_data(True)
            stats_C = get_analytics_data()

            # Удаление всех записей из таблицы CustomUser
            CustomUser.objects.all().delete()
            Analytics.objects.all().delete()

            admins = AdminUser.objects.all()
            for admin in admins:
                if admin.username not in ['collector', 'adminU', 'adminC', 'television']:
                    admin.delete()

            # Сброс счетчика автоинкремента (если используется база данных, поддерживающая автоинкремент)
            # Важно: этот код работает только для определенных типов баз данных, таких как SQLite.

            counter, _ = Analytics.objects.get_or_create(id=1)
            counter.university_counter = 0
            counter.college_counter = 0
            counter.save()

            from django.db import connection
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", ['main_admin_customuser']) # клоака ---v
                except Exception as e:
                    print("Error deleting from sqlite_sequence for main_admin_customuser:", e)
                try:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", ['main_admin_analytics'])
                except Exception as e:
                    print("Error deleting from sqlite_sequence for main_admin_analytics:", e)             # ----------^

            # После сброса перенаправляем пользователя на страницу администратора
            # print(f'stats_U: {stats_U}\nstats_C: {stats_C}')
            return render(request, 'main_admin/index.html', {'stats': stats, 'stats_U': stats_U, 'stats_C': stats_C})
        except Exception as e:
            print('Ошибка в reset_queues: ', str(e))


        # Удаление всех записей из таблицы CustomUser
        CustomUser.objects.all().delete()
        Analytics.objects.all().delete()

        admins = AdminUser.objects.all()
        for admin in admins:
            if admin.username not in ['collector', 'adminU', 'adminC', 'television']:
                admin.delete()

        # Сброс счетчика автоинкремента (если используется база данных, поддерживающая автоинкремент)
        # Важно: этот код работает только для определенных типов баз данных, таких как SQLite.

        counter, _ = Analytics.objects.get_or_create(id=1)
        counter.university_counter = 0
        counter.college_counter = 0
        counter.save()

        from django.db import connection
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", ['main_admin_customuser'])
            except Exception as e:
                print("Error deleting from sqlite_sequence for main_admin_customuser:", e)
            try:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", ['main_admin_analytics'])
            except Exception as e:
                print("Error deleting from sqlite_sequence for main_admin_analytics:", e)

        # После сброса перенаправляем пользователя на страницу администратора
        return redirect('admin_page')
    else:
        queues = CustomUser.objects.all()
        return render(request, 'main_admin/index.html', {'queues': queues, 'error': 'Неверный код!'})

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
def call_ten_students_university(request):
    # Получаем первые 10 записей из очереди университета
    called_studs = CustomUser.objects.filter(affiliation='Университет', called=True)[:10]
    studs_to_call = CustomUser.objects.filter(affiliation='Университет', called=False)[:10]

    # Проверяем, есть ли студенты для вызова

    for stud in called_studs:
        stud.delete()
    # Обновляем статус вызова для студентов, которых собираемся вызвать
    for stud in studs_to_call:
        stud.called = True
        stud.save()
    Analytics.objects.create()


    # После удаления перенаправляем пользователя на страницу администратора
    # return redirect('adminU')
    return HttpResponse(status=204)

@require_POST
def call_ten_students_college(request):
    # Получаем первые 10 записей из очереди университета
    called_studs = CustomUser.objects.filter(affiliation='Колледж', called=True)[:10]
    studs_to_call = CustomUser.objects.filter(affiliation='Колледж', called=False)[:10]

    for stud in called_studs:
        stud.delete()
    for stud in studs_to_call:
        stud.called = True
        stud.save()
    Analytics.objects.create(is_university=False)

    # После удаления перенаправляем пользователя на страницу администратора
    return HttpResponse(status=204)

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
                elif username == 'television':
                    return redirect('tv')
                else:
                    return HttpResponse('Не стоило этого делать... Зачем вам ещё один администратор???? Аааааа?')
            else:
                # Отображение сообщения об ошибке, если пользователь не найден
                error_message = "Неверные учетные данные. Пожалуйста, попробуйте еще раз."
                return render(request, 'main_admin/login_admin.html', {'form_admin': form_admin, 'error_message': error_message})
    return render(request, 'main_admin/login_admin.html', {'form_admin': LoginFormAdmin()})

@never_cache
def create_admin(request):
    if request.method == 'POST':
        form = RegFormAdmin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            key = form.cleaned_data['key']

            if key == 'gT9uJ5sNpE4q':
                AdminUser.objects.create_adminuser(username=username, password=password)
                return redirect('login_admins')
            else:
                return render(request, 'main_admin/registr_admin.html', {'error': 'Неверный ключ', 'form': RegFormAdmin()})
        else:
            print('Форма неверная')
    else:  # Добавляем обработку GET-запросов для отображения формы
        return render(request, 'main_admin/registr_admin.html', {'form': RegFormAdmin()})

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
