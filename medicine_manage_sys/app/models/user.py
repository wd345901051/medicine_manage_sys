from sqlalchemy import Column, BigInteger, String, Boolean, Enum

from app.config import settings

from app.db.session import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='用户ID')
    avatar = Column(String(100), default=f'{settings.BASE_URL}/{settings.STATIC_DIR}/author.jpg', comment='头像')
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    hashed_password = Column(String(60), nullable=False, comment='密码')
    email = Column(String(50), comment='邮箱')
    phone = Column(String(11), comment='电话号码')
    gender = Column(Enum('男', '女'), default='男', comment='性别')
    full_name = Column(String(20), comment='真实姓名')
    id_number = Column(String(18), unique=True, comment='身份证号')
    # is_admin = Column(Boolean, default=False, nullable=False, comment='用户权限')
    is_vip = Column(Boolean, default=False, comment='会员')
