from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app.apis.dependencies import get_db
from app.core.token import create_access_token
from app.models import Staff
from app.schemas import Token
from app.utils.hashing import verify_password

router = APIRouter()


@router.post('/login', response_model=Token, summary='登录接口')
def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    staff = db.query(Staff).filter(Staff.job_number == form_data.username).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="用户不存在")
    if not verify_password(form_data.password, staff.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="密码错误")
    access_token = create_access_token(data={"sub": str(staff.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/logout", response_model=Result, summary="退出登录")
# def logout_token(request: Request):
#     if 'authorization' in request.headers.keys():
#         token = request.headers.get('authorization')[7:]   # 去除token前面的 Bearer
