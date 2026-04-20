from typing import Optional
from src.main.api.models.base_model import BaseModel
from src.main.api.foundation.http_requester import HttpRequester
from requests import Response
import requests
from src.main.api.configs.config import Config
import allure

class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump(by_alias=True) if model is not None else ""
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}"

        with allure.step(f"POST {url}"):
            allure.attach(str(self.request_spec), "Request Headers", allure.attachment_type.TEXT)
            if body:
                allure.attach(str(body), "Request Body", allure.attachment_type.JSON)

            response = requests.post(url=url, headers=self.request_spec, json=body)

            allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
            allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)

            self.response_spec(response)
            return response

    def delete(self, user_id: int) -> Response:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"

        with allure.step(f"DELETE {url}"):
            allure.attach(str(self.request_spec), "Request Headers", allure.attachment_type.TEXT)

            response = requests.delete(url=url, headers=self.request_spec)

            allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
            self.response_spec(response)
            return response

    def get(self, id: Any = None) -> Response:
        endpoint_url = self.endpoint.value.url
        full_url = endpoint_url.format(id=id) if id is not None else endpoint_url
        url = f"{Config.fetch('backendUrl')}{full_url}"

        with allure.step(f"GET {url}"):
            allure.attach(str(self.request_spec), "Request Headers", allure.attachment_type.TEXT)

            response = requests.get(url=url, headers=self.request_spec)

            allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
            self.response_spec(response)
            return response