from typing import Optional, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from pydantic import UUID3
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Order
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_identity(self, db: Session, identity: UUID3) -> Optional[Order]:
        return db.query(Order).filter(Order.identity == identity).first()

    def get_by_id(self, db: Session, id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == id).first()

    def get_total(self, db: Session):
        return db.query(Order).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10) -> list[Order]:
        offset = (skip - 1) * limit
        return db.query(Order).order_by(Order.id).offset(offset).limit(limit).all()

    def create(self, db: Session, *, obj_in: OrderCreate) -> Order:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Order(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Order, obj_in: Union[OrderUpdate, Dict[str, Any]]) -> Order:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Order).get(id)
        db.delete(obj)
        db.commit()
        return obj


order = CRUDOrder(Order)
