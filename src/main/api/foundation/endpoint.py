from enum import Enum

from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.models.account_history_response import AccountHistoryResponse
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.base_model import BaseModel
from typing import Optional, Type, List
from dataclasses import dataclass

@dataclass
class EndpointConfiguration:
    url: str
    response_model: Optional[Type[BaseModel]]
    request_model: Optional[Type[BaseModel]] = None


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model= None,
        url = "/admin/users",
        response_model = None

    )
    LOGIN_USER = EndpointConfiguration(
        request_model= LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponse
    )

    DEPOSIT_MONEY = EndpointConfiguration(
        request_model = DepositRequest,
        url = "/account/deposit",
        response_model= DepositResponse
    )

    GET_TRANSACTIONS = EndpointConfiguration(
        url = "/account/transactions/{id}",
        request_model = None,
        response_model = AccountHistoryResponse
    )

    TRANSFER_MONEY = EndpointConfiguration(
        url="/account/transfer",
        request_model=TransferRequest,
        response_model=TransferResponse
    )

    REQUEST_CREDIT = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditRequest,
        response_model=CreditResponse
    )

    REPAY_CREDIT = EndpointConfiguration(
        url="/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse
    )

    CREDIT_HISTORY = EndpointConfiguration(
        url="/credit/history",
        request_model=None,
        response_model=CreditHistoryResponse
    )