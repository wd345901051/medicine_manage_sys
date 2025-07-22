from sqlalchemy import Column, BigInteger, String

from app.db.session import Base


class StaffRole(Base):
    __tablename__ = "staff_role"
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='ID')
    staff_id = Column(BigInteger, comment="员工ID")
    role_id = Column(BigInteger, comment="角色ID")
    role_name = Column(String(50), comment="角色名称")

