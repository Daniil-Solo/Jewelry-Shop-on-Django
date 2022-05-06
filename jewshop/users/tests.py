from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from django.test import TestCase, Client
from django.contrib.auth import login, get_user_model
from django.urls import reverse

User = get_user_model()


class TestUser(TestCase):
    def setUp(self):
        self.username = "tUser"
        self.email = "tuser@mail.ru"
        self.password = "tpassword"
        user = User.objects.create(username=self.username, email=self.email)
        user.set_password(self.password)
        user.save()
        self.client = Client()
        self.login_link = reverse('login')
        self.register_link = reverse('register')

    def test_success_login_POST(self):
        response = self.client.post(
            self.login_link,
            {
                "username": self.email,
                "password": self.password,
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_fail_login_POST(self):
        response = self.client.post(
            self.login_link,
            {
                "username": "wrong_username",
                "password": "wrong_password",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/login.html')

    def test_success_registration_POST(self):
        response = self.client.post(
            self.register_link,
            {
                "username": "nUser",
                "email": "nuser@gmail.com",
                "password1": "password123!",
                "password2": "password123!"
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_fail_registration_same_username_POST(self):
        response = self.client.post(
            self.register_link,
            {
                "username": self.username,
                "email": "nuser@gmail.com",
                "password1": "password123!",
                "password2": "password123!"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/register.html')

    def test_fail_registration_same_email_POST(self):
        with self.assertRaises(TransactionManagementError):
            self.client.post(
                self.register_link,
                {
                    "username": "nUser",
                    "email": self.email,
                    "password1": "password123!",
                    "password2": "password123!"
                }
            )
