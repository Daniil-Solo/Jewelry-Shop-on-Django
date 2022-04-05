from django.urls import path, include
from .views import LoginView, RegistrationView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
