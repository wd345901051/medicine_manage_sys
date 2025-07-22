from typing import Union

from pydantic import BaseModel, Field
from pydantic.types import date


class MedicineBase(BaseModel):
    """共享模型字段"""
    medicine_name: str
    single_price: float


class MedicineCreate(MedicineBase):
    """添加数据时的字段验证"""
    medicine_sn: str
    medicine_img_url: str
    company_name: str
    medicine_type_id: int
    medicine_apply: str
    medicine_specification: str
    medicine_material: str
    medicine_recipe: str
    medicine_usage: str
    medicine_taboo: str
    medicine_produce_date: date
    medicine_valid_date: date
    medicine_exp: str
    medicine_stock: int = Field(..., ge=0)
    medicine_monthly_sales: int = Field(..., ge=0)


class MedicineUpdate(BaseModel):
    """"更新数据时的字段验证"""
    medicine_sn: str
    medicine_img_url: str
    company_name: str
    medicine_type_id: int
    medicine_apply: str
    medicine_specification: str
    medicine_material: str
    medicine_usage: str
    medicine_taboo: str
    medicine_produce_date: date
    medicine_valid_date: date
    medicine_exp: str
    medicine_stock: int = Field(..., ge=0)
    medicine_monthly_sales: int = Field(..., ge=0)


class Medicine(BaseModel):
    id: int

    class Config:
        orm_mode = True
