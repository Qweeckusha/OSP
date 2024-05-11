from django import forms

class LoginForm(forms.Form):
    queue_id = forms.CharField(label='Номер в очереди', max_length=10)

class LoginFormAdmin(forms.Form):
    username = forms.CharField(label='Логин', max_length=40)
    password = forms.CharField(label='Пароль', max_length=100)

class RegFormAdmin(forms.Form):
    username = forms.CharField(label='Логин', max_length=40)
    password = forms.CharField(label='Пароль', max_length=100)
    key = forms.CharField(label='Ключ', max_length=12)