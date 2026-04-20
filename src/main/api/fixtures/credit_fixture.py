import pytest

from src.main.api.models.credit_request import CreditRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def credit_user_request(api_manager: ApiManager) -> CreateUserRequest:
    credit_user_model = RandomModelGenerator.generate(CreateUserRequest)
    credit_user_model.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(credit_user_model)
    return credit_user_model

@pytest.fixture
def create_other_credit_user(api_manager: ApiManager) -> CreateUserRequest:
    credit_user_model = RandomModelGenerator.generate(CreateUserRequest)
    credit_user_model.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(credit_user_model)
    return credit_user_model

@pytest.fixture
def credit_user_account(api_manager: ApiManager, credit_user_request: CreateUserRequest) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(credit_user_request)

@pytest.fixture
def user_with_active_credit(api_manager: ApiManager, credit_user_request: CreateUserRequest, credit_user_account: CreateAccountResponse):
    credit_model = CreditRequest.create_credit_model(credit_user_account)
    return api_manager.credit_steps.request_credit(credit_user_request, credit_model)