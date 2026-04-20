import pytest

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_other_user_request(api_manager):
    other_user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(other_user_request)
    return other_user_request

@pytest.fixture
def admin_login():
    return LoginUserRequest(username="admin", password="123456")