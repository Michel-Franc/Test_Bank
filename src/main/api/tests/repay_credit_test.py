import pytest
from typing import Callable
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.models.credit_table import Credit
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.account_history_response import AccountHistoryResponse
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.models.transaction_table import Transaction


@pytest.mark.api
class TestCreditRepay:
    def test_repay_credit(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                  credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse):

        repay_model = CreditRepayRequest.create_repay_model(user_with_active_credit, credit_user_account)
        api_manager.credit_steps.repay_credit(credit_user_request, repay_model)

        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, 0.0)

        db_session.expire_all()
        credit_db = db_session.query(Credit).filter_by(id=user_with_active_credit.credit_id).first()
        assert credit_db.balance == 0.0, f"Ошибка! В БД остаток долга по кредиту {credit_db.balance}, а должен быть 0"

        api_manager.assertions.assert_transaction_db(db_session, credit_user_account.id, 'credit_repayment', user_with_active_credit.amount)

    @pytest.mark.parametrize("factory_method", [
        CreditRepayRequest.create_low_repay_model,
        CreditRepayRequest.create_high_repay_model
    ])
    def test_repay_credit_invalid_amounts(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                          credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse,
                                          factory_method: Callable):
        invalid_repay_model = factory_method(user_with_active_credit, credit_user_account)
        api_manager.credit_steps.repay_credit_invalid(credit_user_request, invalid_repay_model, ResponseSpecs.request_unprocessable())

        api_manager.assertions.assert_balance(credit_user_request, credit_user_account.id, user_with_active_credit.amount)
        db_session.expire_all()
        credit_db = db_session.query(Credit).filter_by(id=user_with_active_credit.credit_id).first()
        assert abs(credit_db.balance) == user_with_active_credit.amount, "Долг в БД изменился при невалидной сумме!"
        api_manager.assertions.assert_no_transaction_db(db_session, credit_user_account.id, transaction_type='credit_repayment')

    def test_repay_another_user_credit_forbidden(self, db_session: Session, api_manager: ApiManager, user_with_active_credit: CreditResponse,
                                                 create_user_request: CreateUserRequest, rich_account: AccountHistoryResponse):
        repay_model = CreditRepayRequest.create_repay_model(user_with_active_credit, rich_account)
        api_manager.credit_steps.repay_credit_invalid(create_user_request, repay_model, ResponseSpecs.request_forbidden())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)
        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Деньги списались со счета в БД!"

        credit_db = db_session.query(Credit).filter_by(id=user_with_active_credit.credit_id).first()
        assert abs(credit_db.balance) == user_with_active_credit.amount, "Чужой долг в БД изменился!"
        api_manager.assertions.assert_no_transaction_db(db_session, rich_account.id, transaction_type='credit_repayment')

    def test_repay_non_existent_credit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                                 rich_account: AccountHistoryResponse, credit_user_request: CreateUserRequest, non_existent_credit_id: int):
        repay_model = CreditRepayRequest.create_phantom_repay_model(non_existent_credit_id, rich_account)
        api_manager.credit_steps.repay_credit_invalid(credit_user_request, repay_model, ResponseSpecs.request_not_found())

        api_manager.assertions.assert_balance(create_user_request, rich_account.id, rich_account.balance)
        db_session.expire_all()
        account_db = AccountCrudDb.get_account_by_id(db_session, rich_account.id)
        assert account_db.balance == rich_account.balance, "Баланс в БД изменился при 404 ошибке!"
        api_manager.assertions.assert_no_transaction_db(db_session, rich_account.id, transaction_type='credit_repayment')

    def test_request_credit_after_repayment(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                            credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse):
        repay_model = CreditRepayRequest.create_repay_model(user_with_active_credit, credit_user_account)
        api_manager.credit_steps.repay_credit(credit_user_request, repay_model)

        new_credit_model = CreditRequest.create_credit_model(credit_user_account)
        response = api_manager.credit_steps.request_credit(credit_user_request, new_credit_model)

        assert response.credit_id is not None
        assert response.credit_id != user_with_active_credit.credit_id

        db_session.expire_all()
        credits_in_db = db_session.query(Credit).filter_by(account_id=credit_user_account.id).all()

        assert len(credits_in_db) == 2, f"Ожидалось 2 записи в таблице Credit, найдено {len(credits_in_db)}"
        closed_credit = next(c for c in credits_in_db if c.id == user_with_active_credit.credit_id)
        active_credit = next(c for c in credits_in_db if c.id == response.credit_id)

        assert abs(closed_credit.balance) == 0.0, "Старый кредит не обнулился в БД"
        assert abs(active_credit.balance) == new_credit_model.amount, "Новый кредит имеет неверный баланс в БД"

    def test_repay_credit_insufficient_account_balance(self, db_session: Session, api_manager: ApiManager,
                                                       credit_user_request: CreateUserRequest,
                                                       user_with_active_credit: CreditResponse):
        empty_account = api_manager.user_steps.create_account(credit_user_request)
        repay_model = CreditRepayRequest.create_repay_model(user_with_active_credit, empty_account)
        api_manager.credit_steps.repay_credit_invalid(credit_user_request, repay_model, ResponseSpecs.request_unprocessable())

        api_manager.assertions.assert_balance(credit_user_request, empty_account.id, 0.0)

        db_session.expire_all()
        credit_db = db_session.query(Credit).filter_by(id=user_with_active_credit.credit_id).first()
        assert abs(credit_db.balance) == user_with_active_credit.amount

    def test_repay_already_closed_credit(self, db_session: Session, api_manager: ApiManager, credit_user_request: CreateUserRequest,
                                         credit_user_account: CreateAccountResponse, user_with_active_credit: CreditResponse):
        repay_model = CreditRepayRequest.create_repay_model(user_with_active_credit, credit_user_account)
        api_manager.credit_steps.repay_credit(credit_user_request, repay_model)
        api_manager.credit_steps.repay_credit_invalid(credit_user_request, repay_model, ResponseSpecs.request_unprocessable())

        repay_tx_count = db_session.query(Transaction).filter_by(
            from_account_id=credit_user_account.id,
            transaction_type='credit_repayment'
        ).count()

        assert repay_tx_count == 1, f"Обнаружено {repay_tx_count} транзакций погашения вместо одной!"