from fastapi import APIRouter, Security
from typing import List
from fastapi import Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud
from ..dependencies import get_db, get_current_staff, has_medicine_manage_permission
from ...models import Staff
from ...schemas import MedicineCreate, MedicineUpdate
from ...schemas.result import Result
from ...utils import resp_200, resp_201

router = APIRouter()


@router.post("/add", response_model=Result, summary="添加药品")
def add_medicine(medicine_in: MedicineCreate, db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    exist = crud.medicine.get__by_sn(medicine_in.medicine_sn, db)
    if exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="该药品已存在")
    medicine = crud.medicine.create(medicine_in, db)
    return resp_201(msg=f'{medicine.medicine_sn}添加成功')


@router.get("/list", response_model=Result, summary="获取药品列表")
def list_medicines(db: Session = Depends(get_db), skip: int = 1, limit: int = 10,
                   staff: Staff = Security(has_medicine_manage_permission)):
    medicine_list = crud.medicine.get_multi(db, skip, limit)
    return resp_200(data=medicine_list, msg="查询成功")


@router.post("update", response_model=Result, summary="修改药品信息")
def update_medicine(id: int, medicine_in: MedicineUpdate, db: Session = Depends(get_db),
                    staff=Security(has_medicine_manage_permission)):
    medicine_data = crud.medicine.get_by_id(id, db)
    if not medicine_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该药品不存在")
    crud.medicine.update(db=db, db_obj=medicine_data, obj_in=medicine_in)
    return resp_200(msg="更新成功")


@router.delete("/delete/{id}", response_model=Result, summary="删除药品")
def delete_medicine(id: int, db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    medicine_data = crud.medicine.get_by_id(id, db)
    if not medicine_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"该药品不存在")
    crud.medicine.remove(id, db)
    return resp_200(msg="删除成功")


@router.post("/delete/multi", response_model=Result, summary="批量删除药品信息")
def delete_multi_medicine(id_list: List[int], db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    for id in id_list:
        medicine_data = crud.medicine.get_by_id(id, db)
        if not medicine_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="药品不存在")
    crud.medicine.remove_multi(id_list, db)
    return resp_200(msg="删除成功")


@router.get("/total", response_model=Result, summary="获取药品总数")
def get_medicine_total(db: Session = Depends(get_db), staff=Security(has_medicine_manage_permission)):
    total = crud.medicine.get_total(db)
    return resp_200(data=total, msg="操作成功")
