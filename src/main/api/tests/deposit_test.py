import pytest
from typing import Type
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.deposit_request import *
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager



@pytest.mark.api
class TestDeposit:
    def test_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                create_user_account: CreateAccountResponse):
        deposit_model = DepositRequest.create_deposit_model(create_user_account)
        api_manager.account_steps.deposit_money(create_user_request, deposit_model)

        api_manager.assertions.assert_balance(create_user_request, create_user_account.id, deposit_model.amount)

        api_manager.assertions.assert_transaction_db(db_session, create_user_account.id, 'deposit', deposit_model.amount)

    @pytest.mark.parametrize(
        "model_class",
        [DepositRequestTooLow, DepositRequestTooHigh, DepositRequestNegative]
    )
    def test_deposit_invalid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                           create_user_account: CreateAccountResponse, model_class: Type[DepositRequest]):
        invalid_model = DepositRequest.create_deposit_model(create_user_account, cls=model_class)

        api_manager.account_steps.deposit_money_invalid(create_user_request, invalid_model)
        api_manager.assertions.assert_balance(create_user_request, create_user_account.id, create_user_account.balance)
        last_tx = AccountCrudDb.get_last_transaction(db_session, create_user_account.id)
        if last_tx:
            assert last_tx.amount != invalid_model.amount, "Ошибочная транзакция попала в базу!"

    def test_deposit_unauthorized(self, db_session: Session, api_manager: ApiManager, create_user_account: CreateAccountResponse):
        deposit_model = DepositRequest.create_deposit_model(create_user_account)
        response = api_manager.account_steps.action_unauthorized(Endpoint.DEPOSIT_MONEY, deposit_model)

        assert response.json()["message"] == "JWT Token not found"

        last_tx = AccountCrudDb.get_last_transaction(db_session, create_user_account.id)
        assert last_tx is None, "Транзакция была создана в БД без авторизации!"

    def test_deposit_admin(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                           create_user_account: CreateAccountResponse, admin_login: LoginUserRequest):
        deposit_model = DepositRequest.create_deposit_model(create_user_account)
        api_manager.account_steps.deposit_money_as_user(admin_login, deposit_model, ResponseSpecs.request_forbidden())

        api_manager.assertions.assert_balance(create_user_request, create_user_account.id, create_user_account.balance)

        account_db = AccountCrudDb.get_account_by_id(db_session, create_user_account.id)
        assert account_db.balance == create_user_account.balance, "Админ смог изменить баланс в БД!"

        api_manager.assertions.assert_no_transactions_db(db_session, create_user_account.id)


    def test_deposit_not_owner(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                               create_other_user_request: CreateUserRequest, create_user_account: CreateAccountResponse):
        login_other_user_request = create_other_user_request.as_login()
        api_manager.admin_steps.login_user(login_other_user_request)
        deposit_model = DepositRequest.create_deposit_model(create_user_account)
        api_manager.account_steps.deposit_money_as_user(login_other_user_request, deposit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(create_user_request, create_user_account.id, create_user_account.balance)

        account_db = AccountCrudDb.get_account_by_id(db_session, create_user_account.id)
        assert account_db.balance == create_user_account.balance, "Баланс в БД изменился, пополнение не от владельца!"
        api_manager.assertions.assert_no_transactions_db(db_session, create_user_account.id)

    def test_deposit_non_existent_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                          non_existent_account_id: int):
        deposit_model = DepositRequest.create_deposit_model_with_id(non_existent_account_id)
        api_manager.account_steps.deposit_money_as_user(create_user_request.as_login(), deposit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_no_transactions_db(db_session, non_existent_account_id)





