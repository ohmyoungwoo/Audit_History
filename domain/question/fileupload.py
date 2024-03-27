from tempfile import NamedTemporaryFile
from typing import IO

async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name
   
"""
#question_router.py 화일에 포함되어야 할 듯

from fastapi import FastAPI, File, UploadFile

@app.post("/file/store")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    return {"filepath": path,
            "filename": file.filename}
    
""" 