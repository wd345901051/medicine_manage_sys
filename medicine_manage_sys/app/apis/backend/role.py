from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.apis.dependencies import get_db, has_role_manage_permission
from app.core import flush_privilege, flush_all_privilege
from app.models import Privilege, RolePrivilege, Role, StaffRole
from app.schemas import RoleCreate, PrivilegeBase
from app.utils import resp_200

router = APIRouter()


@router.post("/add", summary="添加角色")
def add_role(role_in: RoleCreate, db: Session = Depends(get_db), staff=Security(has_role_manage_permission)):
    exist = crud.role.get_by_name(role_in.role_name, db)
    if exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"{role_in.role_name}已存在")
    crud.role.create(role_in, db)
    return resp_200(msg=f"{role_in.role_name}添加成功")


@router.get("/list", summary="获取角色列表")
def list_role(db: Session = Depends(get_db), skip: int = 1, limit: int = 10,
              staff=Security(has_role_manage_permission)):
    return crud.role.get_multi(db, skip, limit)


@router.post("/add/privilege", summary="给角色添加权限")
def add_role_privilege(role_id: int, privilege_list: List[PrivilegeBase], db: Session = Depends(get_db),
                       staff=Security(has_role_manage_permission)):
    privilege_id_list = []
    for privilege in privilege_list:
        privilege_id_list.append(privilege.id)
    role_exist = crud.role.get_by_id(role_id, db)
    if not role_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{role_id}不存在")
    privilege_exist = db.query(Privilege).filter(Privilege.id.in_(privilege_id_list)).all()
    privilege_exist_id = []
    for privilege in privilege_exist:
        privilege_exist_id.append(privilege.id)
    curr_list = []
    for privilege_id in privilege_id_list:
        if privilege_id not in privilege_exist_id:
            curr_list.append(privilege_id)
    if len(curr_list) > 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{curr_list}不存在")
    role_privilege_exist = db.query(RolePrivilege).filter(RolePrivilege.role_id == role_id).all()
    role_privilege_exist_id = []
    for role_privilege in role_privilege_exist:
        role_privilege_exist_id.append(role_privilege.privilege_id)
    for privilege_id in privilege_id_list:
        if privilege_id in role_privilege_exist_id:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="不能重复添加权限")
    db_objs = []
    for privilege in privilege_list:
        role_privilege = RolePrivilege()
        role_privilege.role_id = role_id
        role_privilege.privilege_id = privilege.id
        role_privilege.privilege_name = privilege.privilege_name
        db_objs.append(role_privilege)
    db.add_all(db_objs)
    db.commit()
    # db.refresh(db_objs)
    for pri in privilege_id_list:
        flush_privilege(pri, db)
    return resp_200(msg="添加权限成功")


@router.get("/get/privilege", summary="查询角色拥有的权限")
def list_role_privilege(role_id: int, db: Session = Depends(get_db), staff=Security(has_role_manage_permission)):
    data = db.query(RolePrivilege).filter(RolePrivilege.role_id == role_id).all()
    return resp_200(data=data, msg="查询成功")


@router.delete("/delete/privilege", summary="删除角色拥有的权限")
def delete_role_privilege(role_id: int, privilege_id_list: List[int], db: Session = Depends(get_db),
                          staff=Security(has_role_manage_permission)):
    db.query(RolePrivilege).filter(
        RolePrivilege.role_id == role_id, RolePrivilege.privilege_id.in_(privilege_id_list)).delete()
    db.commit()
    for pri in privilege_id_list:
        flush_privilege(pri, db)
    return resp_200(msg="删除成功")


@router.delete("/delete", summary="删除角色")
def delete_role_privilege(role_id: int, db: Session = Depends(get_db), staff=Security(has_role_manage_permission)):
    db.query(Role).filter(Role.id == role_id).delete()
    db.query(RolePrivilege).filter(RolePrivilege.role_id == role_id).delete()
    db.query(StaffRole).filter(StaffRole.role_id == role_id).delete()
    db.commit()
    flush_all_privilege(db)
    return resp_200(msg="删除成功")
