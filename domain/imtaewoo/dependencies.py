import datetime
import json
from fastapi import HTTPException, Depends, Cookie, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decrypt_token
from app.database import SessionLocal
from app import models

from fastapi import HTTPException

TWO_HOURS = 60 * 60 * 2


async def get_db():
    with SessionLocal() as session:
        try:
            yield session
        except HTTPException:
            session.rollback()
            raise
        finally:
            session.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str | None = Cookie(None, alias=settings.SESSION_TOKEN_NAME),
):
    try:
        username = decrypt_token(token)["username"]
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(models.User).filter(models.User.username == username).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
