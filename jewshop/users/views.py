from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm, RegistrationForm
User = get_user_model()


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
