from typing import Annotated
from pydantic import Field, ConfigDict
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule


class TransferRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    amount: Annotated[float, CreationRule(regex=r'^(([5-9][0-9]{2}|[1-9][0-9]{3})(\.[0-9]{2})?|10000)$')]

    @staticmethod
    def create_transfer_model(from_account_id, to_account_id, cls=None):
        class_model = cls if cls else TransferRequest
        model = RandomModelGenerator.generate(class_model)
        model.from_account_id = from_account_id.id
        model.to_account_id = to_account_id.id
        return model

class TransferRequestTooLow(TransferRequest):
    amount: Annotated[float, CreationRule(regex=r'^([1-4][0-9]{0,2}|[1-9][0-9]?)(\.[0-9]{1,2})?$')]


class TransferRequestTooHigh(TransferRequest):
    amount: Annotated[float, CreationRule(regex=r'^(1000[1-9]| 1[1-9][0-9]{3}|[2-9][0-9]{4,})(\.[0-9]{2})?$')]