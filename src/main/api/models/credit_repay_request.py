from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.account_history_response import AccountHistoryResponse
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.base_model import BaseModel
from pydantic import Field, ConfigDict


class CreditRepayRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: float

    @staticmethod
    def create_repay_model(credit_response: CreditResponse, account_info: AccountHistoryResponse | CreateAccountResponse) -> CreditRepayRequest:
        return CreditRepayRequest(
            creditId=credit_response.credit_id,
            accountId=account_info.id,
            amount=credit_response.amount
        )

    @staticmethod
    def create_low_repay_model(credit_response: CreditResponse, account_info: AccountHistoryResponse | CreateAccountResponse):
        return CreditRepayRequest(
            creditId=credit_response.credit_id,
            accountId=account_info.id,
            amount=round(credit_response.amount - 100.0, 2)
        )

    @staticmethod
    def create_high_repay_model(credit_response: CreditResponse, account_info: AccountHistoryResponse | CreateAccountResponse):
        return CreditRepayRequest(
            creditId=credit_response.credit_id,
            accountId=account_info.id,
            amount=round(credit_response.amount + 100.0, 2)
        )

    @staticmethod
    def create_phantom_repay_model(phantom_id: int, account_info: AccountHistoryResponse | CreateAccountResponse) -> 'CreditRepayRequest':
        return CreditRepayRequest(
            creditId=phantom_id,
            accountId=account_info.id,
            amount=100.0
        )