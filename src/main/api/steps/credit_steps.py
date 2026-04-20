from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps
from typing import Callable
from src.main.api.foundation.requesters.crud_requester import CrudRequester



class CreditSteps(BaseSteps):
    def __init__(self, created_obj):
        super().__init__(created_obj)

    def request_credit(self, create_user_request: CreateUserRequest, credit_model: CreditRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_created()
        ).post(model=credit_model)

    def repay_credit(self, create_user_request: CreateUserRequest, repay_model: CreditRepayRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(model=repay_model)

    def get_credit_history(self, create_user_request: CreateUserRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_HISTORY,
            ResponseSpecs.request_ok()
        ).get()

    def request_credit_invalid(self, create_user_request: CreateUserRequest, credit_model: CreditRequest,
                               expected_spec: Callable):
        return CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            response_spec=expected_spec
        ).post(model=credit_model)

    def repay_credit_invalid(self, create_user_request: CreateUserRequest, repay_model: CreditRepayRequest, expected_spec: Callable):

        return CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.REPAY_CREDIT,
            response_spec=expected_spec
        ).post(model=repay_model)