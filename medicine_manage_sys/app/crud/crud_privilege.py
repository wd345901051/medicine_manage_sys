from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Privilege


class CRUDMedicine(CRUDBase[Privilege,None,None]):
    def get_multi(self, db: Session, skip: int = 1, limit: int = 10):
        offset = (skip - 1) * limit
        return db.query(Privilege).offset(offset).limit(limit).all()


privilege = CRUDMedicine(Privilege)
