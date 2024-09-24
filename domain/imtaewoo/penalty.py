import os
import datetime

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_active_user, get_db


router = APIRouter(tags=["penalty"])


@router.get("/penalty/vendor", response_model=schemas.VendorName)
async def get_vendor_name(vendor_code: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Vendor).filter(models.Vendor.vendor_code == vendor_code).first()
    )


@router.get("/penalty", response_model=list[schemas.Penalty])
def get_penalty(db: Session = Depends(get_db)):
    return db.query(models.Penalty).all()


@router.post("/penalty")
async def create_penalty(
    penalty: schemas.PenaltyCreate,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_history = models.Penalty(
        **penalty.dict(exclude={"files"}), created_by=user.username
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)

    for file in penalty.files:
        if file["status"] == "done":
            path = os.path.join("./uploads/penalty/", file["uid"])
            os.replace(file["response"]["path"], path)
            db_attach = models.PenaltyAttach(
                name=file["name"],
                status="uploaded",
                file_path=path,
                file_type=file["type"],
                file_size=file["size"],
                last_modified_date=datetime.datetime.strptime(
                    file["lastModifiedDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                created_by=user.username,
                history_id=db_history.id,
            )
            db.add(db_attach)
            db.commit()

    db.refresh(db_history)
    return db_history


@router.put("/penalty/{item_id}")
async def update_penalty(
    item_id: int,
    penalty: schemas.PenaltyCreate,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_history = read_penalty_by_id(db, item_id)
    if db_history is None:
        return None

    update_data = penalty.dict(exclude={"files"}, exclude_unset=True)
    for var, value in update_data.items():
        setattr(db_history, var, value) if value else None

    db_history.modified_by = user.username
    db_history.modified_date = datetime.datetime.now()

    db.add(db_history)
    db.commit()
    db.refresh(db_history)

    for file in penalty.files:
        if file["status"] == "done":
            path = os.path.join("./uploads/penalty/", file["uid"])
            os.replace(file["response"]["path"], path)
            db_attach = models.PenaltyAttach(
                name=file["name"],
                status="uploaded",
                file_path=path,
                file_type=file["type"],
                file_size=file["size"],
                last_modified_date=datetime.datetime.strptime(
                    file["lastModifiedDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                created_by=user.username,
                history_id=db_history.id,
            )
            db.add(db_attach)
            db.commit()
            db.refresh(db_attach)

        if file["status"] == "removed":
            db_attach = read_attach_by_id(db, file["id"])

            if (db_attach != None) and (db_attach.created_by == user.username):
                if os.path.isfile(db_attach.file_path):
                    os.remove(db_attach.file_path)

                db.refresh(db_attach)
                db.delete(db_attach)
                db.commit()
            else:
                raise HTTPException(status_code=401)
        db.refresh(db_history)
    return db_history


@router.delete("/penalty/{item_id}")
def delete_penalty(
    item_id: int,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    penalty = read_penalty_by_id(db, item_id)

    if penalty.created_by == user.username:
        for file in penalty.files:
            if os.path.isfile(file.file_path):
                os.remove(file.file_path)

        db.refresh(penalty)
        db.delete(penalty)
        db.commit()
    else:
        raise HTTPException(status_code=401)

    return penalty


@router.get("/penalty/file/{item_id}")
async def download_file(item_id: int, db: Session = Depends(get_db)):
    file = read_attach_by_id(db, item_id)
    return FileResponse(path=os.path.join(file.file_path))


def read_penalty_by_id(db: Session, item_id: int):
    return db.query(models.Penalty).filter(models.Penalty.id == item_id).one_or_none()


def read_attach_by_id(db: Session, item_id: int):
    return (
        db.query(models.PenaltyAttach)
        .filter(models.PenaltyAttach.id == item_id)
        .one_or_none()
    )


def update_item(db: Session, item, update_data: dict):
    for key, value in update_data.items():
        setattr(item, key, value)
    db.commit()
