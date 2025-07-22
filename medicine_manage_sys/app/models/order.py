import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, Numeric, Integer, SmallInteger, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class Order(Base):
    __tablename__ = 'order'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='订单ID')
    identity = Column(String(18), unique=True, comment='订单号')
    create_time = Column(DateTime, default=datetime.datetime.now(), comment='创建时间')
    total_amount = Column(Integer, comment='药品总数')
    total_price = Column(Numeric, comment='药品总价')
    status = Column(Boolean, comment='订单状态:0->未支付，1->已支付')
    user_id = Column(BigInteger, comment='用户ID')
    receiver = Column(String(50), comment='收货人')
    receive_address = Column(String(100), comment='收获地址')
    receiver_phone = Column(String(100), comment='收货人手机号')
    medicines = relationship('OrderMedicine')


class OrderMedicine(Base):
    __tablename__ = 'order_medicine'
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    order_id = Column(BigInteger, ForeignKey('order.id'), primary_key=True, comment='订单ID')
    medicine_id = Column(BigInteger, comment='药品ID')
    medicine_name = Column(String(100), nullable=False, comment='药品名称')
    single_price = Column(Numeric, nullable=False, comment='药品单价')
    medicine_amount = Column(Integer, nullable=False, comment='药品数量')

