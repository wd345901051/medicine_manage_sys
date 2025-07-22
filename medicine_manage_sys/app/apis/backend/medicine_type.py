from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.apis.dependencies import get_db, get_current_staff, has_medicine_manage_permission
from app.schemas import MedicineTypeCreate
from app.schemas.result import Result
from app.utils import resp_201, resp_200

router = APIRouter()


@router.post("/add", response_model=Result, summary="添加药品种类")
def add_medicine_type(medicine_type_in: MedicineTypeCreate, db: Session = Depends(get_db),
                      staff=Security(has_medicine_manage_permission)):
    exist = crud.medicine_type.get_by_name(medicine_type_in.type_name, db)
    if exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="药品种类已存在")
    medicine_type = crud.medicine_type.create(medicine_type_in, db)
    return resp_201(msg=f'{medicine_type.type_name}添加成功')


@router.get("/list", response_model=Result, summary="获取药品种类列表")
def list_medicine_types(db: Session = Depends(get_db), skip: int = 1, limit: int = 10,
                        staff=Security(has_medicine_manage_permission)):
    medicine_type_list = crud.medicine_type.get_multi(db, skip, limit)
    return resp_200(data=medicine_type_list, msg="查询成功")


@router.delete("/delete/{id}", response_model=Result, summary="根据id删除药品种类")
def delete_medicine_type(id: int, db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    exist = crud.medicine_type.get_by_id(id, db)
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="药品种类不存在")
    crud.medicine_type.remove(id, db)
    return resp_200(msg="删除成功")


@router.post("/delete/multi", response_model=Result, summary="批量删除药品种类")
def delete_multi_medicine_type(id_list: List[int], db: Session = Depends(get_db),
                               staff=Security(has_medicine_manage_permission)):
    for id in id_list:
        medicine_type = crud.medicine_type.get_by_id(id, db)
        if not medicine_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="药品种类不存在")
    crud.medicine_type.remove_multi(id_list, db)
    return resp_200(msg="删除成功")


@router.get("/total", response_model=Result, summary="获取药品种类的数量")
def get_medicine_type_total(db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    total = crud.medicine_type.get_total(db)
    return resp_200(data=total, msg="操作成功")
