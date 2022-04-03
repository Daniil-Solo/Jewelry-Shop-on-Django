from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from core.utils import MenuMixin
from .forms import EmailForm


class Authorization(MenuMixin, TemplateView):
    template_name = 'authorization/auth.html'
    form_class = EmailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title="Авторизация")
        return {**context, **menu_context}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'))
            # отправить сообщение на email
            return redirect('authorization')
        return render(request, self.template_name, {'form': form})
