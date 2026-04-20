from typing import Callable, Any
from requests import Response
from src.main.api.models.base_model import BaseModel
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class AccountSteps(BaseSteps):
    def deposit_money(self, create_user_request: CreateUserRequest, model: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_ok()
        ).post(model=model)
        return response


    def deposit_money_invalid(self, create_user_request: CreateUserRequest, model: DepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_bad()
        ).post(model=model)
        return response

    def action_unauthorized(self, endpoint: Endpoint, model: BaseModel):
        return CrudRequester(
            RequestSpecs.unauth_headers(),
            endpoint,
            ResponseSpecs.request_unauthorized()
        ).post(model=model)

    def deposit_money_as_user(self, login_user_request: LoginUserRequest, model: DepositRequest, expected_spec: Callable[[Response], Any]):
        response = CrudRequester(
            RequestSpecs.auth_headers(login_user_request.username, login_user_request.password),
            Endpoint.DEPOSIT_MONEY,
            response_spec=expected_spec
        ).post(model=model)
        return response

    def get_transactions(self, create_user_request: CreateUserRequest, account_id: int):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.GET_TRANSACTIONS,
            ResponseSpecs.request_ok()
        ).get(id=account_id)

    def transfer_money(self, create_user_request: CreateUserRequest, transfer_model: TransferRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_ok()
        ).post(model=transfer_model)

    def transfer_money_invalid(self, create_user_request: CreateUserRequest, transfer_model: TransferRequest, expected_spec: Callable[[Response], Any]):
        return CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER_MONEY,
            response_spec=expected_spec
        ).post(model=transfer_model)


