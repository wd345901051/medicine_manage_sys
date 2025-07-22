from typing import Optional, Union, Dict, Any, List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud import CRUDBase
from app.models import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


class CRUDStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):
    def get_by_job_number(self, job_number: str, db: Session) -> Optional[str]:
        return db.query(Staff).filter(Staff.job_number == job_number).first()

    def get_total(self, db: Session):
        return db.query(Staff).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10):
        offset = (skip - 1) * limit
        return db.query(Staff).order_by(Staff.id).offset(offset).limit(limit).all()

    # def create(self, obj_in: StaffCreate, db: Session) -> Staff:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = Staff(**obj_in_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    def update(self, db_obj: Staff, obj_in: Union[StaffUpdate, Dict[str, Any]], db: Session) -> Staff:
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

    def remove(self, id: int, db: Session):
        obj = db.query(Staff).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_multi(self, id_list: List[int], db: Session):
        obj = db.query(Staff).filter(Staff.id.in_(id_list))
        # if not obj.all():
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="员工不存在")
        obj.delete(synchronize_session=False)
        db.commit()
        return obj

    def update_avatar(self, id: int, avatar: str, db: Session):
        db.query(Staff).filter(Staff.id == id).update({"avatar": avatar})
        db.commit()


staff = CRUDStaff(Staff)
