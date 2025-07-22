from sqlalchemy import Column, Integer, String, BigInteger

from app.db.session import Base


class Privilege(Base):
    __tablename__ = "privilege"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment="权限ID")
    privilege_name = Column(String(100), comment="权限名称")
