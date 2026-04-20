from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction
from src.main.api.db.models.account_table import Account
from sqlalchemy import func


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commit()

    @staticmethod
    def get_max_account_id(db: Session) -> int | None:
        return db.query(func.max(Account.id)).scalar()

    @staticmethod
    def get_last_transaction(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id)
        ).order_by(Transaction.id.desc()).first()

