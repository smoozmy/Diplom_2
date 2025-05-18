import requests
import allure
from src.config import BASE_URL

@allure.suite('Тесты на создание заказа')
class TestOrderCreate:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_authorized_with_ingredients(self, auth_user):
        headers = auth_user['headers']

        with allure.step('Получаем список ингредиентов'):
            response = requests.get(f'{BASE_URL}/api/ingredients')
            ingredients = [item['_id'] for item in response.json()['data']]
            assert ingredients

        with allure.step('Создаём заказ'):
            order_response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json={
                'ingredients': ingredients[:2]
            })

        with allure.step('Проверяем успешное создание заказа'):
            assert order_response.status_code == 200
            assert order_response.json()['success'] is True

    @allure.title('Создание заказа без авторизации и с ингредиентами')
    def test_create_order_unauthorized_with_ingredients(self):
        with allure.step('Получаем список ингредиентов'):
            response = requests.get(f'{BASE_URL}/api/ingredients')
            ingredients = [item['_id'] for item in response.json()['data']]
            assert ingredients

        with allure.step('Создаём заказ без токена'):
            order_response = requests.post(f'{BASE_URL}/api/orders', json={
                'ingredients': ingredients[:2]
            })

        with allure.step('Проверяем успешное создание заказа'):
            assert order_response.status_code == 200
            assert order_response.json()['success'] is True

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, auth_user):
        headers = auth_user['headers']

        with allure.step('Отправляем пустой список ингредиентов'):
            response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json={
                'ingredients': []
            })

        with allure.step('Проверяем ошибку'):
            assert response.status_code == 400
            assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с неверными хэшами ингредиентов')
    def test_create_order_with_invalid_ingredients(self, auth_user):
        headers = auth_user['headers']

        with allure.step('Отправляем список с невалидными ID'):
            response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json={
                'ingredients': ['123', '456']
            })

        with allure.step('Проверяем, что заказ не создаётся'):
            assert response.status_code == 500 or response.status_code == 400
