from pydantic import BaseModel


class PrivilegeBase(BaseModel):
    id: int
    privilege_name: str



class Privilege(PrivilegeBase):
    class Config:
        orm_mode = True