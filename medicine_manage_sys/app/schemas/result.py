from typing import TypeVar, Generic, Union, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

SchemasType = TypeVar("SchemasType", bound=BaseModel)


class Result(GenericModel, Generic[SchemasType]):
    """普通结果验证"""
    code: int
    data: Union[SchemasType, str, list, dict, bool] = None
    msg: Optional[str]
