from app.db.session import Base, engine

from sqlalchemy import Column, BigInteger, String


class Depart(Base):
    __tablename__ = 'depart'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='部门ID')
    depart_number = Column(String(2), unique=True, index=True, comment='部门编号')
    name = Column(String(20), unique=True, nullable=False, comment='部门名称')
    desc = Column(String(200), comment='部门描述')
