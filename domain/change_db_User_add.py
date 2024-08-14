# dB의 내용을 바꾸는 코드 (db.username을 '오명우' -> EP ID로 변경)

from sqlalchemy.orm import Session


import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import database
from model.models import User, Question
from domain.user import user_crud, user_schema

id_dict = {
    '이재경': ["jkg.lee","","123001"],
    '허영': ["yeong.hur","","123002"],
    '기윤도': ["sol.ki","","123003"],
    '이두행': ["doohaeng.lee","","123004"],
    '김두형': ["duhyeong.kim","","123005"],
    '류충근': ["chunggeun.ryu","","123006"],
    '심준용': ["junyong.shim","","123007"],
    '윤기남': ["kinam.yoon","","123008"],
    '이병기': ["byoungki.lee","","123009"],
    '이연탁': ["yuntak.lee","","123010"],
    '서동한': ["daniel.seo","","123011"],
  }

db:Session = database.get_db_return() # type: ignore

user_db_list = db.query(User).all()
#print(user_db_list)

#User_db_list= db.query(User).all()
for name in id_dict:
    if not db.query(User).filter(User.username == id_dict[name][0]).all():
        #print(id_dict[name][0],"있다")
        user = User(username=id_dict[name][0], password =id_dict[name][1], email=id_dict[name][0]+"@lge.com", no_company =id_dict[name][2])
        db.add(user)
        print (id_dict[name][0], '추가됨')

db.commit()    # dB를 변경하는 문장