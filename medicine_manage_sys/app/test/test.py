from sqlalchemy.orm import Session

from app.apis.dependencies import get_db

db:Session = get_db()

db.query().outerjoin()