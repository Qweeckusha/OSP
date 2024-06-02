from django import forms

class LoginForm(forms.Form):
    queue_id = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Ваш номер'}))

class LoginFormAdmin(forms.Form):
    username = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Пароль'}))

class RegFormAdmin(forms.Form):
    username = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Пароль'}))
    key = forms.CharField(label='', max_length=12, widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Ключ '}))