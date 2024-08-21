# dB의 내용을 바꾸는 코드 (결재화일 이름 오류 수정)

from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import database
from model.models import User, Question


db:Session = database.get_db_return() # type: ignore

Question_db_list= db.query(Question).all()

for q in Question_db_list:
    q.audit_year_start = q.audit_date.year
    q.audit_year_end = q.audit_date_end.year

db.commit()    # dB를 변경하는 문장
