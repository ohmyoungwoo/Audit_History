from fastapi import APIRouter, FastAPI, File, UploadFile
from tempfile import NamedTemporaryFile
from typing import IO
import os
import datetime
import secrets

router = APIRouter(
    #prefix="/api/question",
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR,'file_dir/')
    
@router.post("/api/question-create/file")
async def store_file(file: UploadFile = File(...)):
    currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #saved_file_name = ''.join([currentTime,secrets.token_hex(16)])
    saved_file_name = ''.join([file.filename, currentTime]) # type: ignore
    file_location = os.path.join(SAVE_DIR,saved_file_name)
    
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        
    return file_location