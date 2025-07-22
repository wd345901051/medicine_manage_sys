from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine_url = "mysql://root:123456@192.168.43.113/medicine_manage_sys?charset=utf8"
engine = create_engine(engine_url, echo=True, pool_size=10)  # 初始化数据库连接
# 创建SessionLocal类型
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData(engine)
Base = declarative_base()   # 创建对象的基类

