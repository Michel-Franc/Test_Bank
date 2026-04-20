from sqlalchemy.orm import Session
from sqlalchemy import func
from src.main.api.db.models.credit_table import Credit

class CreditCrudDb:
    @staticmethod
    def get_max_credit_id(db: Session) -> int | None:
        return db.query(func.max(Credit.id)).scalar()

    @staticmethod
    def get_last_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=account_id).order_by(Credit.id.desc()).first()