from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app import db
from app.core import analyze_token
from app.config import settings

from app.db import redis_pool
from app.db.session import SessionLocal
from app.models import Staff, StaffRole


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

    # def get_current_staff(
    #         security_scopes: SecurityScopes,
    # token_data: str = Depends(oauth2_scheme),
    # db: Session = Depends(get_db)
    # ):
    """获取当前用户"""
    # payload = analyze_token(token_data)
    # token_data = TokenData(sub=payload.get("sub"))  # 获取token存储的用户权限
    # crud_obj = access_crud_by_scopes(token_scopes)  # 验证用户是否存在
    # user = crud_obj.get_by_id(id=payload.get("sub"), db=db)
    # if not user:
    #     raise UserNotExist()
    # for scope in security_scopes.scopes:
    #     if scope not in token_data.scopes:
    #         raise PermissionNotEnough('权限不足，拒绝访问')
    # return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_staff(db: Session = Depends(get_db), token_data: str = Depends(oauth2_scheme))->Staff:
    payload = analyze_token(token_data)
    staff = db.query(Staff).filter(Staff.id == int(payload["sub"])).first()
    return staff


def has_medicine_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.MEDICINE_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff


def has_depart_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.DEPART_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff


def has_staff_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.STAFF_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff


def has_privilege_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.PRIVILEGE_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff


def has_role_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.ROLE_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff


def has_order_manage_permission(db: Session = Depends(get_db), staff: Staff = Depends(get_current_staff)):
    role_list = db.query(StaffRole).filter(StaffRole.staff_id == staff.id).all()
    role_id_list = []
    for role in role_list:
        role_id_list.append(role.role_id)
    res = list(set(role_id_list).intersection(set(settings.ORDER_MANAGE)))
    if len(res) <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    return staff
