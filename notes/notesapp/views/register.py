from django import forms
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect


class RegisterForm(forms.ModelForm):
    """
    Форма регистрации пользователей. Имя пользователя, пароль и поддверждение пароля
    """
    password_confirm = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_confirm']

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            "password": forms.PasswordInput(),
        }


def register(request):
    """
    Зарегистрировать пользователя
    :param request:
    :return:
    """
    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password'])
            new_user.group = Group.objects.filter(name='common user')[0]
            new_user.save()
            return redirect('mainpage')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})