from src.main.api.models.base_model import BaseModel
from pydantic import Field, ConfigDict



class CreditRepayResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credit_id: int = Field(alias="creditId")
    amount_deposited: float = Field(alias="amountDeposited")