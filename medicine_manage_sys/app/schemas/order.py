from datetime import datetime

from pydantic import BaseModel, UUID3

from app.schemas import MedicineBase


class OrderBase(BaseModel):
    # identity: UUID3
    user_id: int
    # status: int
    medicines: MedicineBase
    total_amount: int
    total_price: float
    receiver: str
    receive_address: str
    receiver_phone: str


class OrderPlace(BaseModel):
    pass


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    receiver: str
    receive_address: str
    receiver_phone: str

    class Config:
        orm_mode = True
