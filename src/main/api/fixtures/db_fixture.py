import pytest

from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect().execution_options(isolation_level="READ COMMITTED")
    transaction = connection.begin()
    session = SessionLocal(bind=connection, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def non_existent_account_id(db_session):
    max_id = AccountCrudDb.get_max_account_id(db_session)
    return (max_id + 1) if max_id is not None else 1


@pytest.fixture
def non_existent_credit_id(db_session):
    max_id = CreditCrudDb.get_max_credit_id(db_session)
    return (max_id + 1) if max_id is not None else 1