from typing import Union

from pydantic import BaseModel, Field


class DepartBase(BaseModel):
    name: str
    desc: Union[str, None] = None


class DepartCreate(DepartBase):
    depart_number: str = Field(..., max_length=2, min_length=2)


class DepartUpdate(DepartBase):
    pass
