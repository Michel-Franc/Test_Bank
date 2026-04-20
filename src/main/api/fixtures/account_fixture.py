import pytest
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def create_user_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def create_user_second_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def create_other_user_account(api_manager, create_other_user_request):
    return api_manager.user_steps.create_account(create_other_user_request)

@pytest.fixture
def rich_account(api_manager, create_user_request, create_user_account):
    for _ in range(3):
        model = DepositRequest(accountId=create_user_account.id, amount=5500.0)
        api_manager.account_steps.deposit_money(create_user_request, model)

    return api_manager.account_steps.get_transactions(create_user_request, create_user_account.id)

@pytest.fixture
def standard_account(api_manager, create_user_request, create_user_account):
    deposit_model = DepositRequest(accountId=create_user_account.id, amount=1000.0)
    api_manager.account_steps.deposit_money(create_user_request, deposit_model)
    return api_manager.account_steps.get_transactions(create_user_request, create_user_account.id)

