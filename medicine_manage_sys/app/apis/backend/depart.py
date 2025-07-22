from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.apis.dependencies import get_db, get_current_staff, has_depart_manage_permission
from app.config import settings
from app.models import Depart
from app.schemas import DepartCreate, DepartUpdate
from app.schemas.result import Result
from app.utils import resp_200

router = APIRouter()


@router.post("/add", response_model=Result, summary="添加部门")
async def add_depart(request: Request, depart_in: DepartCreate, db: Session = Depends(get_db),
                     staff=Security(has_depart_manage_permission)):
    exist = db.query(Depart).filter(
        or_(Depart.depart_number == depart_in.depart_number, Depart.name == depart_in.name)).first()
    if exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="部门已存在")
    depart = crud.depart.create(obj_in=depart_in, db=db)
    await request.app.state.redis.set(settings.DEPART_NUMBER + depart_in.depart_number, "1")
    return resp_200(msg=f'{depart.name}添加成功')


@router.get("/list", response_model=Result, summary="获取部门列表")
def list_depart(db: Session = Depends(get_db), skip: int = 1, limit: int = 10, staff=Security(has_depart_manage_permission)):
    depart_list = crud.depart.get_multi(db, skip, limit)
    return resp_200(data=depart_list, msg="查询成功")


@router.post("/update", response_model=Result, summary="更新部门信息")
def update_depart(id: int, depart_in: DepartUpdate, db: Session = Depends(get_db), staff=Security(has_depart_manage_permission)):
    depart_data = crud.depart.get_by_id(id, db)
    if not depart_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该部门不存在")
    crud.depart.update(db_obj=depart_data, obj_in=depart_in, db=db)
    return resp_200(msg="更新成功")


@router.delete("/delete/{id}", response_model=Result, summary="删除部门")
def delete_depart(id: int, db: Session = Depends(get_db), staff=Security(has_depart_manage_permission)):
    exist = crud.depart.get_by_id(id, db)
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该部门不存在")
    crud.depart.remove(id, db)
    return resp_200(msg="删除成功")


# @router.post("/delete/multi", response_model=Result, summary="批量删除部门")
# def delete_multi_depart(id_list: List[int], db: Session = Depends(get_db), staff=Security(get_current_staff)):
#     for id in id_list:
#         depart = crud.depart.get_by_id(id, db)
#         if not depart:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="部门不存在")
#     crud.depart.remove_multi(id_list, db)
#     return resp_200(msg="删除成功")


@router.post("/delete/multi", response_model=Result, summary="批量删除部门")
def delete_multi_depart(id_list: List[int], db: Session = Depends(get_db), staff=Security(has_depart_manage_permission)):
    db.query(Depart).filter(Depart.id.in_(id_list)).delete()
    db.commit()
    return resp_200(msg="删除成功")


@router.get("/total", response_model=Result, summary="获取部门总数")
def get_depart_total(db: Session = Depends(get_db), staff=Security(has_depart_manage_permission)):
    total = crud.depart.get_total(db)
    return resp_200(data=total, msg="操作成功")
