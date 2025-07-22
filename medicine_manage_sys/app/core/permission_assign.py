from sqlalchemy.orm import Session

from app.config.config import settings
from app.models import RolePrivilege


def flush_privilege(pri: int, db: Session):
    if pri == settings.MEDICINE_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.MEDICINE_MANAGE.append(privilege.role_id)
        return
    elif pri == settings.DEPART_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.DEPART_MANAGE.append(privilege.role_id)
        return
    elif pri == settings.STAFF_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.STAFF_MANAGE.append(privilege.role_id)
        return
    elif pri == settings.ROLE_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.ROLE_MANAGE.append(privilege.role_id)
        return
    elif pri == settings.PRIVILEGE_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.PRIVILEGE_MANAGE.append(privilege.role_id)
        return
    elif pri == settings.ORDER_PRIVILEGE:
        privilege_list = db.query(RolePrivilege).filter(RolePrivilege.privilege_id == pri).all()
        for privilege in privilege_list:
            settings.ORDER_MANAGE.append(privilege.role_id)
        return


def flush_all_privilege(db: Session):
    for privilege in settings.ALL_PRIVILEGE:
        flush_privilege(privilege, db)
        print(privilege)
    print("权限初始化完成！！！")
