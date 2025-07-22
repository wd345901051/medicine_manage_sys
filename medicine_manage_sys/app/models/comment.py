from datetime import datetime

from sqlalchemy.orm import relationship

from app.db.session import Base
from sqlalchemy import Column, BigInteger, DateTime, String, Text, ForeignKey


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='评价ID')
    publish_time = Column(DateTime, default=datetime.now, comment='发布时间')
    comment_content = Column(Text, comment='评价内容')
    user_id = Column(BigInteger, ForeignKey('user.id'), comment='用户ID')
    user = relationship('User')
    # user = Column(String(50), comment='用户名')
    medicine_id = Column(BigInteger, ForeignKey('medicine.id'), comment='药品ID')
    medicine = relationship('Medicine')

