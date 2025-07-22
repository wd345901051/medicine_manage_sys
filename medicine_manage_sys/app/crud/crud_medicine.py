from typing import Union, Dict, Any, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Medicine
from app.schemas import MedicineCreate, MedicineUpdate


class CRUDMedicine(CRUDBase[Medicine, MedicineCreate, MedicineUpdate]):

    def get__by_sn(self, sn: str, db: Session):
        return db.query(Medicine).filter(Medicine.medicine_sn == sn).first()

    def get_by_id(self, id: int, db: Session):
        return db.query(Medicine).filter(Medicine.id == id).first()

    def get_total(self, db: Session):
        return db.query(Medicine).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10) -> List[Medicine]:
        offset = (skip - 1) * limit
        return db.query(Medicine).order_by(Medicine.id).offset(offset).limit(limit).all()

    def create(self, obj_in: MedicineCreate, db: Session) -> Medicine:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Medicine(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self,  db_obj: Medicine, obj_in: Union[MedicineUpdate, Dict[str, Any]], db: Session) -> Medicine:
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

    def remove_multi(self, id_list: List[int], db: Session):
        # obj = db.query(Medicine).filter(Medicine.id == id).first()
        # db.delete(obj)
        # db.commit()
        # return obj
        obj = db.query(Medicine).filter(Medicine.id.in_(id_list)).delete(synchronize_session=False)
        db.commit()
        return obj


medicine = CRUDMedicine(Medicine)
