import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.account_history_response import AccountHistoryResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.transfer_request import TransferRequestTooLow, TransferRequestTooHigh
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, rich_account: AccountHistoryResponse,
                                 create_other_user_request: CreateUserRequest, create_other_user_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(rich_account, create_other_user_account)

        response = api_manager.account_steps.transfer_money(create_user_request, transfer_model)

        assert response.from_account_id_balance == rich_account.balance - transfer_model.amount
        api_manager.assertions.assert_balance(create_other_user_request, create_other_user_account.id, transfer_model.amount)
        api_manager.assertions.assert_transfer_transaction_db(db_session, rich_account.id, create_other_user_account.id, transfer_model.amount)

    def test_transfer_between_own_accounts(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                           rich_account: AccountHistoryResponse,
                                           create_user_second_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(rich_account, create_user_second_account)
        response = api_manager.account_steps.transfer_money(create_user_request, transfer_model)

        assert response.from_account_id_balance == rich_account.balance - transfer_model.amount
        api_manager.assertions.assert_balance(create_user_request, create_user_second_account.id, transfer_model.amount)

        acc_from_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        acc_to_db = AccountCrudDb.get_account_by_id(db_session, create_user_second_account.id)

        assert acc_from_db.balance == rich_account.balance - transfer_model.amount
        assert acc_to_db.balance == transfer_model.amount
        api_manager.assertions.assert_transfer_transaction_db(db_session, rich_account.id, create_user_second_account.id, transfer_model.amount)

    @pytest.mark.parametrize(
        "model_class",
        [TransferRequestTooLow, TransferRequestTooHigh]
    )
    def test_transfer_limits_negative(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                      rich_account: AccountHistoryResponse, create_other_user_account: CreateAccountResponse, model_class):
        invalid_model = TransferRequest.create_transfer_model(rich_account, create_other_user_account, cls=model_class)
        api_manager.account_steps.transfer_money_invalid(create_user_request, invalid_model, ResponseSpecs.request_bad())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)

        acc_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert acc_db.balance == rich_account.balance, "Баланс в БД изменился при невалидном лимите перевода!"

    def test_transfer_insufficient__balance(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                            standard_account: CreateAccountResponse, create_other_user_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(standard_account, create_other_user_account)
        transfer_model.amount = 2000.0
        api_manager.account_steps.transfer_money_invalid(create_user_request, transfer_model, ResponseSpecs.request_unprocessable())

        api_manager.assertions.assert_balance(create_user_request, standard_account.id, standard_account.balance)
        account_db = AccountCrudDb.get_account_by_id(db_session, standard_account.id)
        assert account_db.balance == standard_account.balance, "Баланс в БД изменился при нехватке средств!"
        api_manager.assertions.assert_no_transaction_db(db_session, standard_account.id, transaction_type='transfer')

    def test_transfer_not_owner(self,  db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, rich_account: AccountHistoryResponse,
                                create_other_user_request: CreateUserRequest, create_other_user_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(rich_account, create_other_user_account)
        api_manager.account_steps.transfer_money_invalid(create_other_user_request, transfer_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)
        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Баланс в БД изменился: перевод совершен не владельцем!"
        api_manager.assertions.assert_no_transaction_db(db_session, rich_account.id, transaction_type='transfer')

    def test_transfer_as_admin(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, admin_login: LoginUserRequest,
                                         rich_account: AccountHistoryResponse, create_other_user_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(rich_account, create_other_user_account)
        api_manager.account_steps.transfer_money_invalid(admin_login, transfer_model, ResponseSpecs.request_forbidden())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)
        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Админ смог изменить баланс счета в БД!"
        api_manager.assertions.assert_no_transaction_db(db_session, rich_account.id, transaction_type='transfer')

    def test_transfer_unauthorized(self, db_session: Session, api_manager: ApiManager, rich_account: AccountHistoryResponse,
                                   create_other_user_account: CreateAccountResponse):
        transfer_model = TransferRequest.create_transfer_model(rich_account, create_other_user_account)
        response = api_manager.account_steps.action_unauthorized(Endpoint.TRANSFER_MONEY, transfer_model)

        assert response.json()["message"] == "JWT Token not found"
        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Баланс в БД изменился при неавторизованном запросе!"


    def test_transfer_to_non_existent_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                              rich_account: AccountHistoryResponse, non_existent_account_id: int):
        transfer_model = TransferRequest.create_transfer_model(rich_account, rich_account)
        transfer_model.to_account_id = non_existent_account_id
        api_manager.account_steps.transfer_money_invalid(create_user_request, transfer_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)

        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Баланс в БД изменился при переводе на несуществующий счет!"




