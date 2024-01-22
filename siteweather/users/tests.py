from django.db import  IntegrityError
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session

from users.forms import LoginUserForm, RegisterUserForm


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

        # IntegrityError возникает при попытке создания пользователя с таким же именем
        with self.assertRaises(IntegrityError):
            new_user = User.objects.create_user(username='existing_user', password='testpassword')


class UserCreationFormTest(TestCase):
    def test_valid_user_creation_form(self):
        # Передаем корректные данные для успешной регистрации
        form_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'newuser@example.com',
        }

        form = RegisterUserForm(data=form_data)

        # Проверяем, что форма валидна (должна быть валидной)
        self.assertTrue(form.is_valid())

    def test_invalid_user_creation_form(self):
        # Передаем некорректные данные, что приведет к ошибкам валидации
        form_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Пароли не совпадают
            'email': 'invalidemail',  # Некорректный формат email
        }

        form = RegisterUserForm(data=form_data)

        # Проверяем, что форма не валидна (должна быть невалидной)
        self.assertFalse(form.is_valid())

        # Проверяем, что нужные ошибки валидации присутствуют
        self.assertEqual(form.errors['password2'], ['Введенные пароли не совпадают.'])
        self.assertEqual(form.errors['email'], ['Введите правильный адрес электронной почты.'])