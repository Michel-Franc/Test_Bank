from typing import Any, List

from src.main.api.steps.credit_steps import CreditSteps
from src.main.api.assertions.assertions import Assertions
from src.main.api.steps.account_steps import AccountSteps
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps

class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
        self.account_steps = AccountSteps(created_obj)
        self.credit_steps = CreditSteps(created_obj)
        self.assertions = Assertions(self)