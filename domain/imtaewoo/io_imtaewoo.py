import os
import uuid

from fastapi import HTTPException, UploadFile


async def write_workbook(file: UploadFile):
    try:
        basename, ext = os.path.splitext(file.filename)
        path = os.path.join("./uploads/audits", str(uuid.uuid1()) + ext)

        contents = await file.read()
        with open(path, "wb") as fp:
            fp.write(contents)
        return path
    except:
        raise HTTPException(status_code=400, detail="Upload failed.")
