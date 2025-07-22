from fastapi import FastAPI

from app.apis import app_router
# from app.apis.backend import login


def register_router(app: FastAPI):
    """注册路由"""
    # app.include_router(login.router)
    app.include_router(app_router)
