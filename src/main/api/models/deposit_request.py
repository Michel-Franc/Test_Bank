from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.base_model import BaseModel
from pydantic import Field
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule

class DepositRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r'^([1-8][0-9]{3}(\.[0-9]{1,2})?|9000)$')]

    @staticmethod
    def create_deposit_model(create_user_request, cls=None):
        class_model = cls if cls else DepositRequest
        model = RandomModelGenerator.generate(class_model)
        model.account_id = create_user_request.id
        return model

    @staticmethod
    def create_deposit_model_with_id(account_id: int, cls=None) -> 'DepositRequest':
        class_model = cls if cls else DepositRequest
        model = RandomModelGenerator.generate(class_model)
        model.account_id = account_id
        return model

class DepositRequestTooLow(DepositRequest):
    amount: Annotated[float, CreationRule(regex=r'^([1-9][0-9]{0,2})(\.[0-9]{1,2})?$')]

class DepositRequestTooHigh(DepositRequest):
    amount: Annotated[float, CreationRule(regex=r'^(900[1-9]| [1-9][0-9]{4,})(\.[0-9]{2})?$')]

class DepositRequestNegative(DepositRequest):
    amount: Annotated[float, CreationRule(regex=r'^-[1-9][0-9]{0,3}(\.[0-9]{1,2})?$')]