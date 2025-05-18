import requests
import allure
from src.config import BASE_URL

@allure.suite('Тесты на получение заказов пользователя')
class TestUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_with_auth(self, auth_user):
        headers = auth_user['headers']

        with allure.step('Получаем список ингредиентов'):
            response = requests.get(f'{BASE_URL}/api/ingredients')
            ingredients = [item['_id'] for item in response.json()['data']]
            assert ingredients

        with allure.step('Создаём заказ для пользователя'):
            create_response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json={
                'ingredients': ingredients[:2]
            })
            assert create_response.status_code == 200

        with allure.step('Запрашиваем список заказов'):
            orders_response = requests.get(f'{BASE_URL}/api/orders', headers=headers)

        with allure.step('Проверяем успешный ответ и наличие заказов'):
            assert orders_response.status_code == 200
            assert orders_response.json().get('success') is True
            assert orders_response.json().get('orders')

    @allure.title('Попытка получения заказов без авторизации')
    def test_get_orders_without_auth(self):
        with allure.step('Пробуем получить список заказов без токена'):
            response = requests.get(f'{BASE_URL}/api/orders')

        with allure.step('Проверяем, что доступ запрещён'):
            assert response.status_code == 401
            assert response.json()['message'] == 'You should be authorised'
