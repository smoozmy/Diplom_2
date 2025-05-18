import requests
import pytest
import allure
from src.config import BASE_URL

@allure.suite('Тесты на авторизацию пользователя')
class TestUserLogin:

    @allure.title('Авторизация под существующим пользователем')
    def test_login_valid_user(self, auth_user):
        user = auth_user['user']

        with allure.step('Отправляем POST-запрос на логин'):
            response = requests.post(f'{BASE_URL}/api/auth/login', json={
                'email': user['email'],
                'password': user['password']
            })

        with allure.step('Проверяем успешный логин'):
            assert response.status_code == 200
            assert response.json().get('success') is True
            assert 'accessToken' in response.json()


    @allure.title('Авторизация пользователем с неверными данными')
    @pytest.mark.parametrize('email,password', [
        ('wrong@example.com', 'password123'),
        ('valid@email.com', 'wrongpassword')
    ])
    def test_login_invalid_user(self, email, password):
        with allure.step('Пытаемся войти с неверными учётными данными'):
            response = requests.post(f'{BASE_URL}/api/auth/login', json={
                'email': email,
                'password': password
            })

        with allure.step('Проверяем код и сообщение об ошибке'):
            assert response.status_code == 401
            assert response.json()['message'] == 'email or password are incorrect'
