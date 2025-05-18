import pytest
from src.user_helper import random_email
from src.user_api import create_user, delete_user

@pytest.fixture
def user_data():
    return {
        'email': random_email(),
        'password': 'password123',
        'name': 'Test User'
    }

@pytest.fixture
def auth_user(user_data):
    response = create_user(**user_data)
    token = response.json()['accessToken']
    yield {
        'token': token,
        'headers': {'Authorization': token},
        'user': user_data
    }
    delete_user(token)
