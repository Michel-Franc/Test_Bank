from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod
    def request_ok(): # ПРОВЕРКА 200
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created(): # ПРОВЕРКА 201
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad(): # ПРОВЕРКА 400
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def request_conflict(): #409
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm

    @staticmethod
    def request_unauthorized():  # ПРОВЕРКА 401
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    @staticmethod
    def request_forbidden():  # ПРОВЕРКА 403
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
        return confirm

    @staticmethod
    def request_not_found():  # ПРОВЕРКА 404
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm

    @staticmethod
    def request_unprocessable(): # ПРОВЕРКА # 422
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm

    @staticmethod
    def any_status():  # Пропускаем любой статус для ручной проверки в тесте
        def confirm(response: Response):
            pass
        return confirm