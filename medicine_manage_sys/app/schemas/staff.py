import datetime
from datetime import date
from typing import Union, Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field, EmailStr


class StaffBase(BaseModel):
    """查询数据时的字段验证"""
    avatar: str
    job_number: str
    hashed_password: str = Field(min_length=6, max_length=18)
    full_name: str
    id_number: str
    gender: str
    age: int
    phone: str
    email: EmailStr
    depart_id: int
    edu_background: str
    entry_time: date
    birthday: date


class StaffCreate(BaseModel):
    """添加数据时的字段验证"""
    full_name: str
    gender: str
    age: int
    phone: str
    email: EmailStr
    edu_background: str
    entry_time: date
    birthday: date
    depart_id: int
    id_number: str

    class Config:
        orm_mode = True


class StaffUpdate(StaffBase):
    """更新数据时的字段验证"""

    class Config:
        orm_mode = True


class Staff(StaffBase):
    id: int

    class Config:
        orm_mode = True


class StaffSearch(BaseModel):
    skip: int = 1
    limit: int = 10
    depart_id: Optional[int] = None
    start_time: Optional[date] = None
    end_time: Optional[date] = Field(default=datetime.date.today())
    keyword: Optional[str] = None
