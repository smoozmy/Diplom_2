import requests
import pytest
import allure
from src.user_helper import create_user, delete_user, random_email
from src.config import BASE_URL

@allure.suite('Тесты на авторизацию пользователя')
class TestUserLogin:

    @allure.title('Авторизация под существующим пользователем')
    def test_login_valid_user(self):
        email = random_email()
        password = 'password123'

        with allure.step('Создаём пользователя'):
            create_response = create_user(email=email, password=password)
            assert create_response.status_code == 200
            access_token = create_response.json()['accessToken']

        with allure.step('Пытаемся войти с правильными логином и паролем'):
            login_response = requests.post(f'{BASE_URL}/api/auth/login', json={
                'email': email,
                'password': password
            })

        with allure.step('Проверяем статус-код и success'):
            assert login_response.status_code == 200
            assert login_response.json().get('success') is True

        with allure.step('Удаляем пользователя после теста'):
            delete_user(access_token)

    @allure.title('Авторизация пользователем с неверными данными')
    @pytest.mark.parametrize('email,password', [
        ('wrong@example.com', 'password123'),
        ('valid@email.com', 'wrongpassword')
    ])
    def test_login_invalid_user(self, email, password):
        with allure.step('Отправляем запрос на авторизацию с неверными данными'):
            response = requests.post(f'{BASE_URL}/api/auth/login', json={
                'email': email,
                'password': password
            })

        with allure.step('Проверяем, что вернулась ошибка'):
            assert response.status_code == 401
            assert response.json()['message'] == 'email or password are incorrect'
