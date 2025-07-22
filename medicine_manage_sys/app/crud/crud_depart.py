from typing import Optional, Union, Dict, Any, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Depart
from app.schemas import DepartCreate, DepartUpdate


class CRUDDepart(CRUDBase[Depart, DepartCreate, DepartUpdate]):

    def get_by_name(self, name: str, db: Session) -> Optional[str]:
        return db.query(Depart).filter(Depart.name == name).first()

    def get_by_id(self, id: int, db: Session) -> Optional[str]:
        return db.query(Depart).filter(Depart.id == id).first()

    def get_total(self, db: Session):
        return db.query(Depart).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10):
        offset = (skip - 1) * limit
        return db.query(Depart).order_by(Depart.id).offset(offset).limit(limit).all()

    def create(self, obj_in: DepartCreate, db: Session) -> Depart:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Depart(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def update(self,  db_obj: Depart, obj_in: Union[DepartUpdate, Dict[str, Any]], db: Session) -> Medicine:
    #     obj_data = jsonable_encoder(db_obj)
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    def remove(self, id: int, db: Session):
        obj = db.query(Depart).get(id)
        db.delete(obj)
        db.commit()
        return obj

    # def remove_multi(self, id_list: List[int], db: Session):
    #     obj = db.query(Depart).filter(Depart.id.in_(id_list)).delete(synchronize_session=False)
    #     db.commit()
    #     return obj


depart = CRUDDepart(Depart)
