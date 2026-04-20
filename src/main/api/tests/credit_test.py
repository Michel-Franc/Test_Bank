import pytest
from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.credit_response import CreditResponse
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import *
from src.main.api.db.models.transaction_table import Transaction


@pytest.mark.api
class TestCredit:
    def test_request_credit(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                    credit_user_account: CreateAccountResponse):
        credit_model = CreditRequest.create_credit_model(credit_user_account)
        response = api_manager.credit_steps.request_credit(credit_user_request, credit_model)

        assert response.credit_id is not None
        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, credit_model.amount)
        credit_db = CreditCrudDb.get_last_credit_by_account_id(db_session, credit_user_account.id)
        assert credit_db is not None, "Запись о кредите не найдена в таблице Credit"
        assert credit_db.amount == credit_model.amount
        assert credit_db.id == response.credit_id
        api_manager.assertions.assert_transaction_db(db_session, credit_user_account.id, 'credit_issuance', credit_model.amount)

    def test_request_credit_on_second_account(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                              credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse):
        second_credit_account = api_manager.user_steps.create_account(credit_user_request)
        credit_model = CreditRequest.create_credit_model(second_credit_account)
        api_manager.credit_steps.request_credit_invalid(credit_user_request, credit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(credit_user_request, second_credit_account.id, 0.0)

        second_credit_db = CreditCrudDb.get_last_credit_by_account_id(db_session, second_credit_account.id)
        assert second_credit_db is None, "Ошибка! В БД создана запись о кредите для второго счета"

        api_manager.assertions.assert_no_transaction_db(db_session, second_credit_account.id, transaction_type='credit_issuance')



    def test_request_credit_role_user(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                                      create_user_account: CreateAccountResponse):
        credit_model = CreditRequest.create_credit_model(create_user_account)
        api_manager.credit_steps.request_credit_invalid(create_user_request, credit_model, ResponseSpecs.request_forbidden())

        api_manager.assertions.assert_balance(create_user_request, create_user_account.id, 0.0)
        credit_db = CreditCrudDb.get_last_credit_by_account_id(db_session, create_user_account.id)
        assert credit_db is None, "Ошибка! В БД создана запись о кредите для ROLE_USER"
        api_manager.assertions.assert_no_transaction_db(db_session, create_user_account.id, transaction_type='credit_issuance')

    @pytest.mark.parametrize(
        "model_class",
        [CreditRequestTooLow, CreditRequestTooHigh]
    )
    def test_request_credit_invalid_amount(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                           credit_user_account: CreateAccountResponse,model_class: Type[CreditRequest]):
        invalid_credit_model = CreditRequest.create_credit_model(credit_user_account, cls=model_class)
        api_manager.credit_steps.request_credit_invalid(credit_user_request, invalid_credit_model, ResponseSpecs.request_bad())

        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, 0.0)
        credit_db = CreditCrudDb.get_last_credit_by_account_id(db_session, credit_user_account.id)
        assert credit_db is None, f"Ошибка! В БД создан кредит с невалидной суммой {invalid_credit_model.amount}"
        api_manager.assertions.assert_no_transaction_db(db_session, credit_user_account.id, transaction_type='credit_issuance')

    def test_request_second_credit(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                             credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse):
        second_credit_model = CreditRequest.create_credit_model(credit_user_account)
        api_manager.credit_steps.request_credit_invalid(credit_user_request, second_credit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, user_with_active_credit.amount)
        first_tx = db_session.query(Transaction).filter_by(
            to_account_id=credit_user_account.id,
            transaction_type='credit_issuance'
        ).first()
        new_credit_issuance = db_session.query(Transaction).filter(
            Transaction.to_account_id == credit_user_account.id,
            Transaction.transaction_type == 'credit_issuance',
            Transaction.id > first_tx.id
        ).first()

        assert new_credit_issuance is None, "Критическая ошибка! В БД найдена НОВАЯ транзакция выдачи кредита, для счета с активным кредитом"

    def test_request_credit_not_owner(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                      credit_user_account: CreateAccountResponse, create_other_credit_user: CreateUserRequest):
        credit_model = CreditRequest.create_credit_model_with_id(credit_user_account.id)
        api_manager.credit_steps.request_credit_invalid(create_other_credit_user, credit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, credit_user_account.balance)
        api_manager.assertions.assert_no_transaction_db(db_session, credit_user_account.id, transaction_type='credit_issuance')
        credit_db = CreditCrudDb.get_last_credit_by_account_id(db_session, credit_user_account.id)
        assert credit_db is None, "Кредит выдан на чужой счет!"

    def test_request_credit_non_existent_account(self, db_session: Session, api_manager: ApiManager,
                                                 credit_user_request: CreateUserRequest, non_existent_account_id: int):
        credit_model = CreditRequest.create_credit_model_with_id(non_existent_account_id)
        api_manager.credit_steps.request_credit_invalid(credit_user_request, credit_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_no_transaction_db(db_session, non_existent_account_id, transaction_type='credit_issuance')

        credit_in_db = db_session.query(Credit).filter_by(account_id=non_existent_account_id).first()
        assert credit_in_db is None, f"Создан кредит для несуществующего счета {non_existent_account_id}"