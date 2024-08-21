from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from model.models import Question, User, Answer
from database.database import get_db
from database import database


db: Session = database.get_db_return()
skip: int = 0
limit: int = 10
#keyword: str = '세탁기 2024'
keyword: str = '세탁기 오븐'

question_list = db.query(Question)
    
if keyword:
    keyword_list = keyword.split()
    #search = '%%{}%%'.format(keyword_list)  # keyword는 화면에서 전달 받은 값
    #search2 = '%%{}%%'.format(keyword)  # keyword는 화면에서 전달 받은 값
    search_list =[]
    for key in keyword_list:
        search_list.append('%%{}%%'.format(key))
    
    print('--search: ', search_list)

    query = question_list.filter(Question.subject.like((search_list[0])))
    for search in search_list[1:]:
        query = query.union(question_list.filter(Question.subject.like(search)))
    
    """
        question_list = question_list \
        .outerjoin(User) \
            .filter(Question.subject.ilike(search)   # 진단 제목
                #Question.content.in_(search)|   # 진단 상세 내용
                #Question.auditor1.ilike(search)|    # 진단자 이름1
                #Question.auditor2.ilike(search)|    # 진단자 이름2
                #Question.auditor3.ilike(search)|    # 진단자 이름3
                #Question.company.ilike(search)|     # 회사 (ex) LGE, 신성델타 ...
                #Question.region.ilike(search)|      # 사업장 
                #Question.production.ilike(search)|  # 제품군
                #Question.audit_type.ilike(search)|   # 진단유형
                #Question.audit_year_start.in_(search)|   # Year_start
                #Question.audit_year_end.in_(search)   # Year_end
                #sub_query.c.content.ilike(search) | # 답변내용, 
                #sub_query.c.username.ilike(search) # 답변 작성자
        #.outerjoin(sub_query, and_ (sub_query.c.question_id == Question.id)) \
            )
        # sub_query.c.question_id 에서 c 는 서브쿼리의 조회 항목이며, 
        # sub_query.c.question_id 는 서브쿼리의 조회 항목 중 question_id를 의미함
        # and_ 는 sqlalchemy 의 특이한 함수???
    """
            
total = query.distinct().count()
#question_list = question_list.order_by(Question.audit_date.desc()) \
#   .offset(skip).limit(limit).distinct().all() # 리스트 정렬 (진단일자 기준)

search_list = query.order_by(Question.audit_date.desc()) \
   .offset(skip).limit(limit).distinct().all() # 리스트 정렬 (진단일자 기준)

#print('--total:', total, '\n--question list:', question_list)
print('--total:', total, '\n--result', search_list)
#print('--query', query)

