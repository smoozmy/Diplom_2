import pytest
import requests
import allure
from src.user_helper import create_user, delete_user, random_email
from src.config import BASE_URL

@allure.suite('Тесты на создание пользователя')
class TestUserCreate:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        email = random_email()

        with allure.step('Создаём пользователя'):
            response = create_user(email)

        with allure.step('Проверяем статус-код'):
            assert response.status_code == 200
            assert response.json().get('success') is True

        with allure.step('Удаляем пользователя после теста'):
            access_token = response.json()['accessToken']
            delete_user(access_token)

    @allure.title('Создание уже существующего пользователя')
    def test_create_existing_user(self):
        email = random_email()

        with allure.step('Создаём пользователя в первый раз'):
            create_user(email)

        with allure.step('Пытаемся создать пользователя повторно'):
            response = create_user(email)

        with allure.step('Проверяем статус-код и сообщение об ошибке'):
            assert response.status_code == 403
            assert response.json()['message'] == 'User already exists'

    @allure.title('Создание пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_missing_required_field(self, missing_field):
        data = {
            'email': random_email(),
            'password': 'password123',
            'name': 'Test User'
        }
        data.pop(missing_field)

        with allure.step(f'Отправляем запрос без поля: {missing_field}'):
            response = requests.post(f'{BASE_URL}/api/auth/register', json=data)

        with allure.step('Проверяем статус-код и сообщение об ошибке'):
            assert response.status_code == 403
            assert response.json()['message'] == 'Email, password and name are required fields'
