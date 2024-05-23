# dB의 내용을 바꾸는 코드 (db.username을 '오명우' -> EP ID로 변경)

from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import database
from model.models import User, Question

id_dict = {
    '오명우': 'myoungou.oh',
    '홍길동': 'temp',
    '김태화': 'keeth.kim',
    '이용대': 'ydi.lee',
    '김범준': 'beomjun.kim',
    '이승건': 'sunggeon.lee'}

db:Session = database.get_db_return() # type: ignore

"""
#dB 지우기 모듈
q = db.get(Question, 33)  
db.delete(q)
"""


"""
#dB 값 변경 모듈
#user_db_list = db.query(User).all()
for i in range(len(id_dict)):
    q = db.get(User, i+1) 
    #print("ID: {},  db: {}".format(i+1, q.username)) # type: ignore
    q.username = id_dict[q.username] # type: ignore   # dB의 username을 변경하는 부분
    
"""

db.commit()    # dB를 변경하는 문장