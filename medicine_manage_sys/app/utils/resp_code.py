from typing import Any, Optional, Union

from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response, JSONResponse


# def resp_200(*, data: Optional[Any, None] = None, msg: str = 'Success') -> dict:
#     return {'code': 200, 'data': data, 'msg': msg}


def resp_200(*, data: Any = None, msg: str = "请求成功"):
    # return ORJSONResponse(status_code=status.HTTP_200_OK,
    #                       content={'code': 200, 'data': data, 'msg': msg})
    return {'code': 200, 'data': data, 'msg': msg}


def resp_201(*, data: str = None, msg: str = "创建成功"):
    # return ORJSONResponse(status_code=status.HTTP_201_CREATED,
    #                       content={'code': 200, 'data': data, 'msg': msg})
    return {'code': 200, 'data': data, 'msg': msg}


def resp_400(*, data: str = None, msg: str = "请求错误") -> Response:
    return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                          content={'code': 400, 'data': data, 'msg': msg})


def resp_401(*, data: str = None, msg: str = "未授权，请先登录") -> Response:
    return ORJSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                          content={'code': 401, 'data': data, 'msg': msg})


def resp_403(*, data: str = None, msg: str = "拒绝访问") -> Response:
    return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                          content={'code': 403, 'msg': msg, 'data': data})


def resp_404(*, data: str = None, msg: str = "请求不合法") -> Response:
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                          content={'code': 404, 'msg': msg, 'data': data})


def resp_422(*, data: str = None, msg: Union[list, dict, str] = "不可处理的实体") -> Response:
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          content={'code': 422, 'msg': msg, 'data': data})


def resp_500(*, data: str = None, msg: Union[list, dict, str] = "服务器错误") -> Response:
    return ORJSONResponse(headers={'Access-Control-Allow-Origin': '*'},
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          content={'code': 500, 'msg': msg, 'data': data})
