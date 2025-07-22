import uuid

from app.config import settings


def get_uuid() -> uuid.UUID:
    """生成文件唯一标识"""
    return uuid.uuid4()


def generate_job_number(num: str):
    fill = settings.STAFF_JOB_NUMBER_LENGTH - len(num)
    if fill < 0:
        return None
    for _ in range(fill):
        num = '0' + num
    return num
