from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app import crud
from app.apis.dependencies import get_db, get_current_staff, has_privilege_manage_permission

router = APIRouter()


@router.post("/list", summary="获取权限列表")
def list_privilege(db: Session = Depends(get_db), skip: int = 1, limit: int = 10,
                   staff=Security(has_privilege_manage_permission)):
    return crud.privilege.get_multi(db, skip, limit)
