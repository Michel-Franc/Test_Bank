from src.main.api.models.base_model import BaseModel
from pydantic import Field, ConfigDict
from typing import List

class CreditItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    created_at: str = Field(alias="createdAt")

class CreditHistoryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    credits: List[CreditItem]