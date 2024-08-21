from sqlalchemy.orm import Session
from model.models import Question, User, Answer
from database import database


def get_query_list(db: Session, keyword: str = ''):
   
    question_list = db.query(Question)
    
    if keyword:
        keyword_list = keyword.split()
        search_list =[]
        for key in keyword_list:
            search_list.append('%%{}%%'.format(key))
        
        search = search_list[0]
        query = question_list.filter(Question.subject.ilike(search)           # 진단 제목
                                                    |Question.content.ilike(search)           # 진단 상세 내용
                                                    |Question.auditor1.ilike(search)          # 진단자 이름1
                                                    |Question.auditor2.ilike(search)          # 진단자 이름2
                                                    |Question.auditor3.ilike(search)          # 진단자 이름3
                                                    |Question.company.ilike(search)           # 회사 (ex) LGE, 신성델타 ...
                                                    |Question.region.ilike(search)            # 사업장 
                                                    |Question.production.ilike(search)        # 제품군
                                                    |Question.audit_type.ilike(search)        # 진단유형
                                                    |Question.audit_year_start.ilike(search)  # Year_start
                                                    |Question.audit_year_end.ilike(search)    # Year_end
        )

        for search in search_list[1:]:
            query = query.union(question_list.filter(Question.subject.ilike(search)           # 진단 제목
                                                                    |Question.content.ilike(search)           # 진단 상세 내용
                                                                    |Question.auditor1.ilike(search)          # 진단자 이름1
                                                                    |Question.auditor2.ilike(search)          # 진단자 이름2
                                                                    |Question.auditor3.ilike(search)          # 진단자 이름3
                                                                    |Question.company.ilike(search)           # 회사 (ex) LGE, 신성델타 ...
                                                                    |Question.region.ilike(search)            # 사업장 
                                                                    |Question.production.ilike(search)        # 제품군
                                                                    |Question.audit_type.ilike(search)        # 진단유형
                                                                    |Question.audit_year_start.ilike(search)  # Year_start
                                                                    |Question.audit_year_end.ilike(search)    # Year_end
            ))
            

    return query
"""
db: Session = database.get_db_return()
skip: int = 0
limit: int = 10
    
query = get_query_list(db, "세탁기 오븐")
    
total = query.distinct().count()

search_list = query.order_by(Question.audit_date.desc()) \
    .offset(skip).limit(limit).distinct().all() # 리스트 정렬 (진단일자 기준)

print('--total:', total, '\n--result', search_list)
    
"""     
    