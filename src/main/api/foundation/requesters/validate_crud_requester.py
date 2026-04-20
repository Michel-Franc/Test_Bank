from typing import Optional, Any
from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.http_requester import HttpRequester
import allure

class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec = request_spec,
            endpoint = endpoint,
            response_spec = response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
         response = self.crud_requester.delete(user_id)

         with allure.step(f"DELETE {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id} and Validated Model"):
             allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

         self.response_spec(response)
         return self.endpoint.value.response_model.model_validate(response.json())

    def get(self, id: Any = None) -> Any:
        response = self.crud_requester.get(id=id)

        with allure.step(f"GET {response.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}",)

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


