from pydantic import BaseModel


class Login(BaseModel):
    """登录模型"""
    username: str
    password: str
