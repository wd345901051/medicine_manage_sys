import datetime
import os
from datetime import date
from typing import List, Optional

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, File, Request, Query
from fastapi.encoders import jsonable_encoder
from pydantic import Field
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from starlette import status

from app import crud, db
from app.apis.dependencies import get_db, get_current_staff, has_staff_manage_permission
from app.config import settings
from app.models import Staff, StaffRole, Depart
from app.schemas import StaffCreate, StaffUpdate, RoleBase, StaffSearch
from app.schemas.result import Result
from app.utils import resp_201, resp_200
from app.utils.hashing import get_password_hash, verify_password
from app.utils.tools import get_uuid, generate_job_number

router = APIRouter()


@router.post("/add", response_model=Result, summary="添加员工")
async def add_staff(request: Request, staff_in: StaffCreate, db: Session = Depends(get_db),
                    staff: Staff = Security(has_staff_manage_permission)):
    db_obj = jsonable_encoder(staff_in)
    new_staff = Staff(**db_obj)
    depart = db.query(Depart).filter(Depart.id == staff_in.depart_id).first()
    depart_number = await request.app.state.redis.get(settings.DEPART_NUMBER + depart.depart_number)
    new_staff.job_number = depart.depart_number + generate_job_number(depart_number)
    print(depart_number,new_staff.job_number)
    new_staff.hashed_password = get_password_hash("123456")
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    await request.app.state.redis.incr(settings.DEPART_NUMBER + depart.depart_number)
    return resp_201(msg=f'{new_staff.job_number}添加成功')


@router.post("/list", response_model=Result, summary="多条件查询员工列表")
def get_staff_role(staff_in: StaffSearch, db: Session = Depends(get_db),
                   staff: Staff = Security(has_staff_manage_permission)):
    offset = (staff_in.skip - 1) * staff_in.limit
    staff_list = db.query(Staff).filter(
        or_(
            or_(Staff.full_name.like(str(staff_in.keyword) + "%"), staff_in.keyword is None),
            or_(Staff.job_number.like(str(staff_in.keyword) + "%"), staff_in.keyword is None)),
        or_(Staff.depart_id == staff_in.depart_id, staff_in.depart_id is None),
        or_(Staff.entry_time.between(staff_in.start_time, staff_in.end_time),
            staff_in.start_time is None or staff_in.end_time is None)).offset(offset).limit(
        staff_in.limit).all()
    return resp_200(data=staff_list, msg="查询成功")


@router.post("/update", response_model=Result, summary="员工修改信息")
def update_staff(staff_in: StaffUpdate, db: Session = Depends(get_db),
                 staff: Staff = Security(has_staff_manage_permission)):
    staff.hashed_password = get_password_hash(staff.hashed_password)
    crud.staff.update(db_obj=staff, obj_in=staff_in, db=db)
    return resp_200(msg="更新成功")


# @router.post("/update", response_model=Result, summary="员工修改信息")
# def update_staff(id: int, staff_in: StaffUpdate, db: Session = Depends(get_db),
#                  staff: Staff = Security(get_current_staff)):
#     staff_data = crud.staff.get_by_id(id=id, db=db)
#     if not staff_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该员工不存在")
#     crud.staff.update(db_obj=staff_data, obj_in=staff_in, db=db)
#     return resp_200(msg="更新成功")


@router.delete("/delete", response_model=Result, summary="删除员工")
def delete_staff(staff_id: int, db: Session = Depends(get_db), staff=Security(has_staff_manage_permission)):
    staff_data = crud.staff.get_by_id(staff_id, db)
    if not staff_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"该员工不存在")
    crud.staff.remove(staff_id, db)
    db.query(StaffRole).filter(StaffRole.staff_id == staff_id).delete()
    db.commit()
    return resp_200(msg="删除成功")


@router.get("/total", response_model=Result, summary="获取员工总人数")
def get_staff_total(db: Session = Depends(get_db), staff=Security(has_staff_manage_permission)):
    total = crud.staff.get_total(db)
    return resp_200(data=total, msg="操作成功")


@router.post("/update/avatar", summary="修改头像")
async def update_avatar(file: UploadFile = File(...), db: Session = Depends(get_db),
                        staff: Staff = Security(has_staff_manage_permission)):
    old_img = staff.avatar.split('/')[-1]
    old_img_url = "./" + settings.STATIC_DIR + "/" + settings.IMG_DIR + f"/{old_img}"
    if os.path.exists(old_img_url):
        os.remove(old_img_url)
    # 拼接新的图片路径
    img_name = get_uuid()
    img_suffix = file.filename.split('.')[-1]
    img_url = settings.STATIC_DIR + "/" + settings.IMG_DIR + f"/{img_name}.{img_suffix}"
    with open("./" + img_url, "wb") as f:
        new_img = await file.read()
        f.write(new_img)
    db_img_url = settings.BASE_URL + '/' + img_url
    crud.staff.update_avatar(id=staff.id, avatar=db_img_url, db=db)
    return resp_200(msg="操作成功")


@router.post("/modify/password", response_model=Result, summary="员工修改密码")
def modify_password(old_password: str, new_password: str, db: Session = Depends(get_db),
                    staff: Staff = Depends(has_staff_manage_permission)):
    if not verify_password(old_password, staff.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="旧密码不正确")
    new_password = get_password_hash(new_password)
    db.query(Staff).filter(Staff.id == staff.id).update({"hashed_password": new_password})
    db.commit()
    return resp_200(msg="密码修改成功")


@router.post("/reset/password", response_model=Result, summary="管理员重置密码")
def modify_password(staff_id: int, db: Session = Depends(get_db),
                    staff: Staff = Depends(has_staff_manage_permission)):
    staff_data = db.query(Staff).filter(Staff.id == staff_id).first()
    print(staff_data.id_number[-6:])
    new_password = get_password_hash(staff_data.id_number[-6:])
    db.query(Staff).filter(Staff.id == staff_id).update({"hashed_password": new_password})
    db.commit()
    return resp_200(msg="密码重置成功")


@router.post("/add/role", response_model=Result, summary="给员工添加角色")
def add_staff_role(staff_id: int, role_in: RoleBase, db: Session = Depends(get_db),
                   staff: Staff = Depends(has_staff_manage_permission)):
    db_obj = StaffRole()
    db_obj.staff_id = staff_id
    db_obj.role_id = role_in.id
    db_obj.role_name = role_in.role_name
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return resp_200(msg="添加角色成功")


@router.get("/get/role", response_model=Result, summary="查看员工的角色")
def get_staff_role(staff_id: int, db: Session = Depends(get_db),
                   staff: Staff = Depends(has_staff_manage_permission)):
    role = db.query(StaffRole).filter(StaffRole.staff_id == staff_id).all()
    return resp_200(data=role, msg="操作成功")


@router.get("/delete/role", response_model=Result, summary="删除员工拥有的角色")
def delete_staff_role(staff_id: int, role_id: int, db: Session = Depends(get_db),
                      staff: Staff = Depends(has_staff_manage_permission)):
    db.query(StaffRole).filter(StaffRole.staff_id == staff_id, StaffRole.role_id == role_id).delete()
    db.commit()
    return resp_200(msg="删除成功")
