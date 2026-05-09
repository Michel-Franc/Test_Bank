import allure
from typing import Union, List, overload
from playwright.sync_api import Locator


@overload
def get_price_value(data: str) -> float: ...


@overload
def get_price_value(data: List[str]) -> List[float]: ...


@overload
def get_price_value(data: Locator) -> Union[float, List[float]]: ...


def get_price_value(data: Union[str, List[str], Locator]) -> Union[float, List[float]]:
    with allure.step(f"Парсинг цены из данных типа: {type(data)}"):
        if isinstance(data, list):
            return [float(str(item).split("$")[-1].strip()) for item in data]

        elif isinstance(data, str):
            return float(data.split("$")[-1].strip())

        elif isinstance(data, Locator):
            if data.count() > 1:
                return [float(str(item).split("$")[-1].strip()) for item in data.all_text_contents()]

            data.wait_for(state="visible")
            return float(data.inner_text().split("$")[-1].strip())

        else:
            raise TypeError(f"Неподдерживаемый тип для парсинга цен: {type(data)}")


