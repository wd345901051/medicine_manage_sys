from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Role
from app.schemas import RoleCreate
from app.schemas.role import RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def create(self, obj_in: RoleCreate, db: Session):
        obj_data = jsonable_encoder(obj_in)
        db_obj = Role(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, name: str, db: Session):
        return db.query(Role).filter(Role.role_name == name).first()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10):
        offset = (skip - 1) * limit
        return db.query(Role).offset(offset).limit(limit).all()


role = CRUDRole(Role)
