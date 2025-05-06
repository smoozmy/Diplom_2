import requests
import random
import string
from src.config import BASE_URL


def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

def create_user(email=None, password='password123', name='Test User'):
    if email is None:
        email = random_email()
    response = requests.post(f'{BASE_URL}/api/auth/register', json={
        'email': email,
        'password': password,
        'name': name
    })
    return response

def delete_user(access_token):
    headers = {'Authorization': access_token}
    requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)
