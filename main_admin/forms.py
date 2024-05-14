from django import forms

class LoginForm(forms.Form):
    queue_id = forms.CharField(label='Номер в очереди', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Ваш номер'}))

class LoginFormAdmin(forms.Form):
    username = forms.CharField(label='Логин', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Пароль'}))

class RegFormAdmin(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Пароль'}))
    key = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Ключ '}))