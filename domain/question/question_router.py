from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse
import os
import datetime
import secrets

from database.database import get_db
from domain.question import question_schema
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from model.models import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR,'file_dir/')

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword: str =''):
    
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size, keyword=keyword)
    
    return {
        'total': total,
        'question_list': _question_list
    }
    
@router.get("/list-year", response_model=question_schema.QuestionList)
def question_list_year(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, year: int = 0):
    
    total, _question_list = question_crud.get_question_list_year(
        db, skip=page*size, limit=size, year=year)
    
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)
    
@router.post("/upload")
#async def store_file(file: UploadFile = File(...)):
async def store_file(file: UploadFile):
    #currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #saved_file_name = ''.join([file.filename, currentTime]) # type: ignore

    try:
        file_location = os.path.join(SAVE_DIR, file.filename) # type: ignore
        print ("file upload start: ", file_location)
        
        contents = await file.read()
        print ("file read complete")
        
        with open(file_location, "wb+") as file_object:
            #file_object.write(file.file.read())
            file_object.write(contents)
            #print ("file write at ", SAVE_DIR, "file_name :", file.filename)
        
        #os.replace(contents, file_location) (안됨)
        
        return {"file_name":file.filename, "file_path":file_location}
    except:
        raise HTTPException(status_code=400, detail="Upload failed.")
    
""" 임태우 파일 만들기
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
"""

@router.get("/download/{file_name}")
async def download_file(file_name:str):
    #print("Call download router"+file_name)
    file_path = os.path.join(SAVE_DIR, file_name)
    
    #if not os.path.exists(file_path):
    #    raise HTTPException(status_code=404, detail="저장된 파일이 없습니다")
    
    #print(f"Backend_download_File path: {file_path} ")
    return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)

""" 임태우 다운로드
@router.get("/penalty/file/{item_id}")
async def download_file(item_id: int, db: Session = Depends(get_db)):
    file = read_attach_by_id(db, item_id)
    return FileResponse(path=os.path.join(file.file_path))
"""