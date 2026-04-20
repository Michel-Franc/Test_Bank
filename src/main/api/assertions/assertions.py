from src.main.api.db.models.transaction_table import Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest



class Assertions:
    def __init__(self, api_manager):
        self.api_manager = api_manager

    def assert_balance(self, create_user_request: CreateUserRequest, account_id: int, expected_balance: float):
        history = self.api_manager.account_steps.get_transactions(create_user_request, account_id)
        assert history.balance == expected_balance

    def assert_transaction_db(self, db_session, account_id: int, expected_type: str, expected_amount: float):
        transaction = AccountCrudDb.get_last_transaction(db_session, account_id)

        assert transaction is not None, f"Транзакция для счета {account_id} не найдена в БД"
        assert transaction.transaction_type == expected_type, f"Ожидался тип {expected_type}, но в БД {transaction.transaction_type}"
        assert transaction.amount == expected_amount, f"Ожидалась сумма {expected_amount}, но в БД {transaction.amount}"

    def assert_no_transactions_db(self, db_session, account_id: int):
        transaction = AccountCrudDb.get_last_transaction(db_session, account_id)
        assert transaction is None, f"Обнаружена лишняя транзакция (ID: {transaction.id}) в БД!"

    def assert_transfer_transaction_db(self, db_session, from_account_id: int, to_account_id: int, amount: float):
        transaction = AccountCrudDb.get_last_transaction(db_session, from_account_id)

        assert transaction is not None, f"Транзакция перевода для счета {from_account_id} не найдена"
        assert transaction.transaction_type == 'transfer', f"Тип должен быть 'transfer', а не {transaction.transaction_type}"
        assert transaction.from_account_id == from_account_id, "ID отправителя в БД не совпадает"
        assert transaction.to_account_id == to_account_id, "ID получателя в БД не совпадает"
        assert transaction.amount == amount, f"Сумма в БД {transaction.amount} не совпадает с {amount}"

    def assert_no_transaction_db(self, db_session, account_id: int, transaction_type: str = None):
        query = db_session.query(Transaction).filter(
            (Transaction.from_account_id == account_id) | (Transaction.to_account_id == account_id)
        )
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)

        transaction = query.order_by(Transaction.id.desc()).first()

        assert transaction is None, f"В БД найдена лишняя транзакция {transaction_type} (ID: {transaction.id})!"