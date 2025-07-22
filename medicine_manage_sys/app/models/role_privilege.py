from sqlalchemy import Column, BigInteger, String

from app.db.session import Base


class RolePrivilege(Base):
    __tablename__ = "role_privilege"
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='ID')
    role_id = Column(BigInteger, comment="角色ID")
    privilege_id = Column(BigInteger, comment="权限ID")
    privilege_name = Column(String(100), comment="权限名称")

