import uvicorn
from fastapi import FastAPI

from app.core.permission_assign import flush_privilege, flush_all_privilege
from app.db import redis_pool
from app.db.session import Base, engine, SessionLocal
from app.register import register_router
from app.register.mount import register_mount

Base.metadata.create_all(bind=engine)

app = FastAPI()


def create_app():
    """注册中心"""
    register_router(app)
    register_mount(app)
    db = SessionLocal()
    flush_all_privilege(db)
    db.close()



@app.on_event("startup")
async def startup_event():
    create_app()  # 加载注册中心
    app.state.redis = await redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    # 关闭redis
    app.state.redis.close()
    await app.state.redis.wait_closed()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True, workers=1)
