from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.apis.dependencies import get_db, has_order_manage_permission
from app.core import analyze_token
from app.schemas import OrderCreate, OrderUpdate
from app.schemas.result import Result
from app.utils import resp_200, resp_201

router = APIRouter()


# @router.get("/place", response_model=Result, summary="下单")
# def place_order(db: Session = Depends(get_db), *, pyload=Security(analyze_token)):
#
#     print(pyload)
#     return resp_201(msg=f'{pyload["id"]}创建成功')


# @router.post("/cancel", response_model=Result, summary="取消订单")
# def generate_order(db: Session = Depends(get_db), *, order_in: OrderCreate):
#     exist = crud.order.get_by_identity(db, order_in.identity)
#     if exist:
#         raise HTTPException(status_code=status.HTTP_302_FOUND, detail="该订单已存在")
#     order = crud.order.create(db=db, obj_in=order_in)
#     return resp_201(msg=f'{order.identity}创建成功')


# @router.post("/pay", response_model=Result, summary="支付订单")
# def generate_order(db: Session = Depends(get_db), *, order_in: OrderCreate):
#     exist = crud.order.get_by_identity(db, order_in.identity)
#     if exist:
#         raise HTTPException(status_code=status.HTTP_302_FOUND, detail="该订单已存在")
#     order = crud.order.create(db=db, obj_in=order_in)
#     return resp_201(msg=f'{order.identity}创建成功')


@router.post("/add", response_model=Result, summary="生成订单")
def generate_order(order_in: OrderCreate, db: Session = Depends(get_db),staff=Depends(has_order_manage_permission)):
    exist = crud.order.get_by_identity(order_in.identity,db)
    if exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="该订单已存在")
    order = crud.order.create(db=db, obj_in=order_in)
    return resp_201(msg=f'{order.identity}创建成功')


@router.get("/list", response_model=Result, summary="获取订单列表")
def list_orders(db: Session = Depends(get_db), skip: int = 1, limit: int = 10,staff=Depends(has_order_manage_permission)):
    order_list = crud.order.get_multi(db, skip, limit)
    return resp_200(data=order_list, msg="查询成功")


@router.post("/update", response_model=Result, summary="修改订单信息")
def update_order(id: int, order_in: OrderUpdate, db: Session = Depends(get_db),staff=Depends(has_order_manage_permission)):
    order_data = crud.order.get_by_id(id, db)
    if not order_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该订单不存在")
    crud.order.update(db_obj=order_data, order_in=order_in, db=db)
    return resp_200(msg="更新成功")


@router.delete("/delete/multi", response_model=Result, summary="删除订单")
def delete_order(id_list: List[int], db: Session = Depends(get_db),staff=Depends(has_order_manage_permission)):
    for id in id_list:
        order_data = crud.order.get_by_id(id, db)
        if not order_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该订单不存在")
    crud.order.remove_multi(id_list=id_list, db=db)
    return resp_200(msg="删除成功")


@router.get("/total", response_model=Result, summary="获取商家订单总数")
def get_total(db: Session = Depends(get_db),staff=Depends(has_order_manage_permission)):
    total = crud.order.get_total(db)
    return resp_200(data=total, msg="获取成功")

# @router.get("/list", response_model=Result, summary="获取订单列表")
# def list_orders(db: Session = Depends(get_db)):
#     order_list = db.query(Order).all()
#     print(medicine_type_list[0].medicines)
#     return resp_200(data=medicine_type_list, msg="查询成功")
