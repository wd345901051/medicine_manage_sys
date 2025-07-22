
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_PREFIX: str = "/admin"  # 接口前缀
    GLOBAL_ENCODING: str = 'utf-8'  # 全局编码
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8000"  # 开发环境
    STATIC_DIR: str = 'static'  # 静态文件目录
    IMG_DIR: str = 'img'  # 图片文件目录

    SECRET_KEY: str = "haha"  # secrets.token_urlsafe(32)  # 密钥（每次重启服务器密钥都会改变）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token过期时间（60 minutes * 24 hours * 1 day）

    # 权限数据表
    # PERMISSION_DATA: List[dict] = [{'admin': '超级管理员权限'}, {'staff': '员工权限'}, {'user': '普通用户权限'}]
    # 接口允许的角色
    MEDICINE_MANAGE = []
    DEPART_MANAGE = []
    STAFF_MANAGE = []
    PRIVILEGE_MANAGE = []
    ROLE_MANAGE = []
    ORDER_MANAGE = []
    MEDICINE_PRIVILEGE = 1
    DEPART_PRIVILEGE = 2
    STAFF_PRIVILEGE = 3
    PRIVILEGE_PRIVILEGE = 4
    ROLE_PRIVILEGE = 5
    ORDER_PRIVILEGE = 6
    ALL_PRIVILEGE = [MEDICINE_PRIVILEGE, DEPART_PRIVILEGE, STAFF_PRIVILEGE, PRIVILEGE_PRIVILEGE, ROLE_PRIVILEGE,
                     ORDER_PRIVILEGE]

    DEPART_NUMBER = "depart_number:"
    STAFF_JOB_NUMBER_LENGTH = 6


settings = Settings()
