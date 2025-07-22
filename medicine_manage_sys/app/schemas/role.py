from pydantic import BaseModel

from app.schemas import Privilege


class RoleBase(BaseModel):
    id: int
    role_name: str


class RoleCreate(BaseModel):
    role_name: str
    desc: str


class RoleUpdate(RoleBase):
    desc: str


class PrivilegeBase(BaseModel):
    privilege_id: int
    privilege_name: str


class Role(BaseModel):
    privileges: PrivilegeBase

    class Config:
        orm_mode = True
