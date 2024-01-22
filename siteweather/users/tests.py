from django.db import Error
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session


class NewUserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
        }

    def test_user_registration_creates_user_and_session(self):
        # Проверяем, что пользователь не существует до регистрации
        self.assertFalse(User.objects.filter(username=self.user_data['username']).exists())

        # Отправляем POST-запрос с данными формы регистрации
        response = self.client.post(self.register_url, data=self.user_data, follow=True)

        # Проверяем успешность регистрации
        self.assertEqual(response.status_code, 200)

        # Проверяем, что пользователь был создан
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        new_user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(new_user.email, self.user_data['email'])

        # Проверяем, что сессия была создана
        self.assertTrue(Session.objects.filter(session_key=self.client.session.session_key).exists())


class UserNonUniqueRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')

    def test_registration_with_non_unique_username_raises_exception(self):
        # Создаем пользователя с заданным логином (именем)
        existing_user = User.objects.create_user(username='existing_user', password='testpassword')

        # Используем assertRaises для проверки, что Error возникает при попытке создания пользователя с таким же именем
        with self.assertRaises(Error):
            new_user = User.objects.create_user(username='existing_user', password='testpassword')