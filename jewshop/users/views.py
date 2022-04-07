from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordChangeView as DjangoPasswordChangeView
)
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm, RegistrationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
User = get_user_model()


class PasswordChangeView(DjangoPasswordChangeView):
    template_name = "password/password_change_form.html"
    form_class = PasswordChangeForm


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    form_class = SetPasswordForm


class PasswordResetView(DjangoPasswordResetView):
    template_name = "password/password_reset_form.html"
    form_class = PasswordResetForm
    email_template_name = "password/password_reset_email.html"
    title = "Восстановление пароля"
    subject_template_name = "password/password_reset_subject.txt"


class LoginView(DjangoLoginView):
    form_class = LoginForm


class RegistrationView(View):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get(self, request):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError as ex:
                print(ex)
                form.add_error('email', 'Аккаунт с такой почтой уже зарегистрирован. Пожалуйста авторизуйтесь')
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

