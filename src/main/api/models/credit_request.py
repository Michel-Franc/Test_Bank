from pydantic import Field
from typing import Annotated, Type
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel



class CreditRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r'^(([5-9][0-9]{3}|1[0-4][0-9]{3})(\.[0-9]{2})?|15000)$')]
    term_months: Annotated[int, CreationRule(regex=r'^12$')] = Field(alias="termMonths", default=12)

    @staticmethod
    def create_credit_model(account_obj, cls: Type['CreditRequest'] = None):
        target_class = cls if cls else CreditRequest
        credit_model = RandomModelGenerator.generate(target_class)
        credit_model.account_id = account_obj.id
        return credit_model

    @staticmethod
    def create_credit_model_with_id(account_id: int) -> 'CreditRequest':
        model = RandomModelGenerator.generate(CreditRequest)
        model.account_id = account_id
        return model

class CreditRequestTooLow(CreditRequest):
    amount: Annotated[float, CreationRule(regex=r'^[0-4][0-9]{0,3}(\.[0-9]{2})?$')]

class CreditRequestTooHigh(CreditRequest):
    amount: Annotated[float, CreationRule(regex=r'^(1500[1-9]|[1-9][0-9]{5})(\.[0-9]{2})?$')]