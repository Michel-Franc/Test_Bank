from pydantic import BaseModel as BM, ConfigDict


class BaseModel(BM):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True
    )
