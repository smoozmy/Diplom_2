import requests
import allure
from src.config import BASE_URL
from src.user_helper import random_email

@allure.step('Создание пользователя через API')
def create_user(email=None, password='password123', name='Test User'):
    if email is None:
        email = random_email()
    response = requests.post(f'{BASE_URL}/api/auth/register', json={
        'email': email,
        'password': password,
        'name': name
    })
    return response

@allure.step('Удаление пользователя через API')
def delete_user(access_token):
    headers = {'Authorization': access_token}
    return requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)
