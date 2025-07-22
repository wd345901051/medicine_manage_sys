from fastapi import APIRouter

from app.apis.backend import login, medicine_type, medicine, depart, staff, order, privilege, role

app_router = APIRouter()

app_router.include_router(login.router, tags=["login"])
app_router.include_router(medicine_type.router, prefix="/medicine/type", tags=["medicine_type"])
app_router.include_router(medicine.router, prefix="/medicine", tags=["medicine"])
app_router.include_router(depart.router, prefix="/depart", tags=["depart"])
app_router.include_router(staff.router, prefix="/staff", tags=["staff"])
app_router.include_router(order.router, prefix="/order", tags=["order"])
app_router.include_router(privilege.router, prefix="/privilege", tags=["privilege"])
app_router.include_router(role.router, prefix="/role", tags=["role"])

