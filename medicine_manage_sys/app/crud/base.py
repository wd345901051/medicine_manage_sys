from typing import Generic, TypeVar, Any, Type, Optional, List, Tuple, Union, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import Base
from app.utils.hashing import verify_password

# from app.utils.hashing import verify_password

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, id: Any, db: Session) -> Optional[ModelType]:
        """通过 id 获取对象"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 1, limit: int = 10):
        """获取分页数据"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_total(self, db: Session) -> int:
        """获取数据总数"""
        return db.query(self.model).count()

    def create(self, obj_in: CreateSchemaType, db: Session) -> ModelType:
        """添加对象"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]], db: Session) -> ModelType:
        """"更新对象"""
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

    # def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]], db: Session):
    #     db_obj = db.query(self.model).filter(self.model.id == id)
    #     db_obj.update(**obj_in)
    #     db.commit()
    #     return 'updated successfully'

    def remove(self, id: int, db: Session) -> ModelType:
        """ 通过id删除对象 """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_multi(self, id_list: List[int], db: Session):
        """通过id同时删除多个对象"""
        obj = db.query(self.model).filter(ModelType.id.in_(id_list)).delete(synchronize_session=False)
        db.commit()
        return obj


