from app.config.config import settings

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    """生成 token
    :param data:存储数据
    :return:加密后的token
    """
    to_encode = data.copy()
    # print(to_encode)
    # expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# token: Optional[str] = Header(...)  -> Union[str, Any]
def analyze_token(token: str):
    """解析 token"""

    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[ALGORITHM])

        # id: int = payload["sub"]
        # if id is None:
        #     raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Not authenticated",
        #             headers={"WWW-Authenticate": "Bearer"},
        #         )
        # return TokenData(id=id)
    # except jwt.api_jwt.ExpiredSignatureError:
    #     print('token失效')
    # except jwt.api_jwt.DecodeError:
    #     print('token错误')
    # except jwt.api_jwt.InvalidIssuerError:
    #     print('token非法')
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# if __name__ == '__main__':
#     token = create_access_token({'sub': 5})
#     analyze_token(token)
#     print(token)
