from django.urls import path, include
from .views import LoginView, RegistrationView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from .forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeDoneView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name="password_reset_complete"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(template_name = "password/password_change_done.html"), name="password_change_done"),
    path('', include('django.contrib.auth.urls')),
]
