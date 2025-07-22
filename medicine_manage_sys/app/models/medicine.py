from sqlalchemy import Column, BigInteger, String, Date, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Medicine(Base):
    __tablename__ = 'medicine'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment='药品ID')
    medicine_sn = Column(String(13), unique=True, nullable=False, comment='药品编号')
    medicine_img_url = Column(String(100), comment='药品图片')
    medicine_name = Column(String(100), nullable=False, comment='药品名称')
    company_name = Column(String(50),  nullable=False, comment='生产厂商')
    single_price = Column(Numeric,  nullable=False, comment='药品单价')
    medicine_type_id = Column(Integer, ForeignKey('medicine_type.id'))
    medicine_type = relationship('MedicineType')
    medicine_apply = Column(String(100), nullable=False, comment='适用人群')
    medicine_specification = Column(String(50), nullable=False, comment='规格')
    medicine_material = Column(String(60), nullable=False, comment='主要成分')
    medicine_recipe = Column(String(600), nullable=False, comment="配方")
    medicine_usage = Column(String(50),  nullable=False, comment='用法用量')
    medicine_taboo = Column(String(100),  nullable=False, comment='注意事项')
    medicine_produce_date = Column(Date,  nullable=False, comment='生产日期')
    medicine_valid_date = Column(Date,  nullable=False, comment="截止日期")
    medicine_exp = Column(String(10), nullable=False, comment='保质期')
    medicine_stock = Column(Integer,  nullable=False, comment='库存量')
    medicine_monthly_sales = Column(Integer, nullable=False, comment='月销量')
