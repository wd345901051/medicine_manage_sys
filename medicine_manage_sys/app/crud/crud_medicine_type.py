from typing import Any, Union, Dict, Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.medicine_type import MedicineType

from app.schemas.medicine_type import MedicineTypeUpdate, MedicineTypeCreate
from app.utils.hashing import get_password_hash


class CRUDMedicineType(CRUDBase[MedicineType, MedicineTypeCreate, MedicineTypeUpdate]):

    def get_by_name(self, name: str, db: Session) -> Optional[MedicineType]:
        return db.query(MedicineType).filter(MedicineType.type_name == name).first()

    def get_total(self, db: Session):
        return db.query(MedicineType).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10) -> list[MedicineType]:
        offset = (skip - 1) * limit
        return db.query(MedicineType).order_by(MedicineType.id).offset(offset).limit(limit).all()

    def create(self, obj_in: MedicineTypeCreate, db: Session) -> MedicineType:
        # db_obj = MedicineType(type_name=obj_in.type_name)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = MedicineType(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_multi(self, id_list: List[int], db: Session):
        obj = db.query(MedicineType).filter(MedicineType.id.in_(id_list)).delete(synchronize_session=False)
        db.commit()
        return obj


medicine_type = CRUDMedicineType(MedicineType)
