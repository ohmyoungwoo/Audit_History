from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from database.database import get_db
from domain.user.security import ldap_auth, verify_password

router = APIRouter(tags=["login"])


@router.post("/login")
async def user_login(form_data: schemas.UserBase, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .one_or_none()
    )

    try:
        ldap_res = ldap_auth(form_data.username, form_data.password)

        if user is None:
            user = models.User(
                **ldap_res, last_login=datetime.now(), date_joined=datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            update_info = {
                k: v
                for k, v in ldap_res.items()
                if k not in {"username", "employeeNumber"}
            }
            for var, value in update_info.items():
                setattr(user, var, value) if value else None
            user.last_login = datetime.now()
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except:
        if user is None:
            raise HTTPException(status_code=401)
        if verify_password(form_data.password, user.password):
            return user
        else:
            raise HTTPException(status_code=401)
