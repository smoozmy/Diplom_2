import requests
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

    @allure.title('Изменение пароля авторизованного пользователя')
    def test_update_user_password(self, auth_user):
        headers = auth_user['headers']
        new_password = 'newpassword123'

        with allure.step('Обновляем пароль'):
            response = requests.patch(f'{BASE_URL}/api/auth/user', headers=headers, json={'password': new_password})

        with allure.step('Проверяем, что пароль успешно обновился'):
            assert response.status_code == 200

    @allure.title('Изменение имени повторно авторизованного пользователя')
    def test_update_user_name_again(self, auth_user):
        headers = auth_user['headers']
        new_name = 'Super Burger'

        with allure.step('Обновляем имя ещё раз'):
            response = requests.patch(f'{BASE_URL}/api/auth/user', headers=headers, json={'name': new_name})

        with allure.step('Проверяем обновлённое имя'):
            assert response.status_code == 200
            assert response.json()['user']['name'] == new_name
