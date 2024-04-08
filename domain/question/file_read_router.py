from fastapi import APIRouter, FastAPI, File, UploadFile
from starlette.responses import FileResponse
import os

router = APIRouter(
#    prefix="/api/question",
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR,'file_dir/')
    

@router.get('/file_down/{file_name}')
def read_file(file_name:str):
    return FileResponse(''.join([SAVE_DIR,file_name]))