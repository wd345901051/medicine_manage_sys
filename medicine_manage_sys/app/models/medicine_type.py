from sqlalchemy import Column, Integer, Enum, String

from app.db.session import Base, engine


class MedicineType(Base):
    __tablename__ = 'medicine_type'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='药品种类ID')
    type_name = Column(String(100), unique=True, comment='药品种类')

