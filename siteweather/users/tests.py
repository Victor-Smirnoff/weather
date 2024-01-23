from django.db import  IntegrityError
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
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


class LoginUserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_login_user_form(self):
        # Передаем корректные данные для успешного входа
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        form = LoginUserForm(data=form_data)

        # Проверяем, что форма валидна (должна быть валидной)
        self.assertTrue(form.is_valid())

    def test_invalid_login_user_form(self):
        # Передаем некорректные данные, которые приведут к ошибке валидации
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',  # Неверный пароль
        }

        form = LoginUserForm(data=form_data)

        # Проверяем, что форма не валидна (должна быть невалидной)
        self.assertFalse(form.is_valid())

        # Проверяем, что нужная ошибка валидации присутствует
        error_message = 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        self.assertIn(error_message, form.errors['__all__'])


class SessionExpirationTest(TestCase):
    def test_session_expiration(self):
        # Устанавливаем меньшее время жизни сессии для целей тестирования
        self.client.session['_session_expiry'] = int(timezone.now().timestamp()) - 1

        # Попробуем выполнить запрос с авторизованным пользователем
        response = self.client.get('/users/profile/')

        # Проверяем, что теперь сессия истекла, и пользователь вышел из системы
        self.assertEqual(response.status_code, 302)  # Должен быть редирект
        self.assertFalse(self.client.session.get('_session_expiry'))  # Проверяем, что _session_expiry удален
        self.assertFalse(self.client.session.get('_auth_user_id'))  # Пользователь разлогинен