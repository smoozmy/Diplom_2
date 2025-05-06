import requests
import pytest
import allure
from src.config import BASE_URL

@allure.suite('Тесты на изменение данных пользователя')
class TestUserUpdate:

    @allure.title('Изменение имени авторизованного пользователя')
    def test_update_user_with_auth(self, auth_user):
        headers = auth_user['headers']
        new_name = 'Updated Name'

        with allure.step('Изменяем имя пользователя'):
            response = requests.patch(f'{BASE_URL}/api/auth/user', headers=headers, json={
                'name': new_name
            })

        with allure.step('Проверяем успешное обновление'):
            assert response.status_code == 200
            assert response.json()['user']['name'] == new_name

    @allure.title('Попытка изменить email без авторизации')
    def test_update_user_without_auth(self):
        with allure.step('Отправляем PATCH-запрос без токена'):
            response = requests.patch(f'{BASE_URL}/api/auth/user', json={
                'email': 'new@email.com'
            })

        with allure.step('Проверяем, что запрос отклонён'):
            assert response.status_code == 401
            assert response.json()['message'] == 'You should be authorised'


    @allure.title('Изменение любого поля авторизованного пользователя')
    @pytest.mark.parametrize('field,value', [
        ('password', 'newpassword123'),
        ('name', 'Super Burger')
    ])
    def test_update_each_field_with_auth(self, auth_user, field, value):
        headers = auth_user['headers']
        update_data = {field: value}

        with allure.step(f'Обновляем поле {field}'):
            response = requests.patch(f'{BASE_URL}/api/auth/user', headers=headers, json=update_data)

        with allure.step('Проверяем статус'):
            assert response.status_code == 200

        if field != 'password':
            with allure.step('Проверяем, что значение поля обновилось'):
                assert response.json()['user'][field] == value

