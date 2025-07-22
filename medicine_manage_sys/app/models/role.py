from sqlalchemy import Column, String, BigInteger

from app.db.session import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment="角色ID")
    role_name = Column(String(50), comment="角色名称")
    desc = Column(String(200), comment="角色描述")






