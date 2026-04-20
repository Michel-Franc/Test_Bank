from typing import List, Optional
from pydantic import Field
from src.main.api.models.base_model import BaseModel


class TransactionItem(BaseModel):
    transaction_id: int = Field(alias="transactionId")
    type: str
    amount: float
    from_account_id: Optional[int] = Field(alias="fromAccountId", default=None)
    to_account_id: Optional[int] = Field(alias="toAccountId", default=None)
    created_at: str = Field(alias="createdAt")

class AccountHistoryResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[TransactionItem]