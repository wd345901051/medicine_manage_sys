from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Comment
from app.schemas import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def get_by_id(self, db: Session, id: int) -> Optional[Comment]:
        return db.query(Comment).filter(Comment.id == id).first()

    def get_total(self, db: Session):
        return db.query(Comment).count()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10) -> list[Comment]:
        offset = (skip - 1) * limit
        return db.query(Comment).order_by(Comment.id).offset(offset).limit(limit).all()

    def create(self, db: Session, *, obj_in: CommentCreate) -> Comment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Comment(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_multi(self, db: Session, id_list: List[int]):
        # obj = db.query(Comment).get(id)
        # db.delete(obj)
        # db.commit()
        # return obj
        obj = db.query(Comment).filter(Comment.id.in_(id_list)).delete(synchronize_session=False)
        db.commit()
        return obj


comment = CRUDComment(Comment)
