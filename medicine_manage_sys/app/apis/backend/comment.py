from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app import crud
from app.apis.dependencies import get_db
from app.schemas.result import Result
from app.utils import resp_200

router = APIRouter()


@router.get("/list", response_model=Result, summary="获取评论列表")
def list_comment(db: Session = Depends(get_db), skip: int = 1, limit: int = 10, staff=Security(get_db)):
    comment_list = crud.medicine_type.get_multi(db, skip, limit)
    return resp_200(data=comment_list, msg="查询成功")


@router.get("/total", response_model=Result, summary="获取评论总数")
def get_comment_total(db: Session = Depends(get_db), staff=Security(get_db)):
    total = crud.comment.get_total(db)
    return resp_200(data=total, msg="操作成功")
