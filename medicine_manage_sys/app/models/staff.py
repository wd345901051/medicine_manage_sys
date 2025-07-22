from app.db.session import Base
from sqlalchemy import Column, BigInteger, String, Integer, Date, Enum, ForeignKey
from app.config import settings
from sqlalchemy.orm import relationship


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='员工ID')
    avatar = Column(String(100), server_default=f'{settings.BASE_URL}/{settings.STATIC_DIR}/author.jpg', comment='头像')
    job_number = Column(String(10), unique=True, comment="工号")
    hashed_password = Column(String(60), nullable=False, comment='登录密码')
    full_name = Column(String(50), comment='员工姓名')
    gender = Column(Enum('男', '女'), comment='性别')
    age = Column(Integer, comment='年龄')
    birthday = Column(Date, comment='生日')
    phone = Column(String(11), comment='手机号')
    email = Column(String(50), comment='邮箱')
    id_number = Column(String(18), unique=True, comment='身份证号')
    edu_background = Column(Enum('大专及以下', '本科', '硕士', '博士'), comment='学历')
    entry_time = Column(Date, comment='入职时间')
    # role_id = Column(BigInteger, comment="角色ID")
    # role = relationship('Role')
    depart_id = Column(BigInteger, ForeignKey('depart.id'))
    depart = relationship('Depart')
    # is_admin = Column(Boolean, default=False, comment='用户权限')
