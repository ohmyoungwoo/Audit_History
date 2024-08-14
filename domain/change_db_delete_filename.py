# dB의 내용을 바꾸는 코드 (결재화일 이름 오류 수정)

from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import database
from model.models import User, Question


db:Session = database.get_db_return() # type: ignore

Question_db_list= db.query(Question).all()

print(Question_db_list)

for q in Question_db_list:
    file_name : str = q.file_name # type: ignore
    pdf_file_name : str = q.pdf_file_name # type: ignore
    if file_name == pdf_file_name :
        #print(q.file_name, "--", q.pdf_file_name)
        q.pdf_file_name = "" # type: ignore
        q.pdf_file_path = "" # type: ignore
    
for q in Question_db_list:
    file_name : str = q.file_name # type: ignore
    pdf_file_name : str = q.pdf_file_name # type: ignore
    if file_name == pdf_file_name :
        print(q.file_name, "--", q.pdf_file_name)

db.commit()    # dB를 변경하는 문장