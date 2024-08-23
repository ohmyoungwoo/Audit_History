from datetime import datetime
import os

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from model.models import Question, User, Answer
from sqlalchemy.orm import Session
from sqlalchemy import and_
#from domain.question.query_list import get_query_list

#def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = '', year = None):
def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    query_list = db.query(Question)
    if keyword:
        query_list = get_query_list(db, keyword)
        
    #if year:
    #    search = '%%{}%%'.format(year)
    #    question_list = question_list \
    #        .filter(Question.audit_year_start.ilike(search)|
    #                Question.audit_year_end).ilike(search)
    #        )
        
    total = query_list.distinct().count()
    question_list = query_list.order_by(Question.audit_date.desc()) \
        .offset(skip).limit(limit).distinct().all() # 리스트 정렬 (진단일자 기준)
        
    return total, question_list

def get_question_list_year(db: Session, skip: int = 0, limit: int = 10, year:int = 0):
    question_list = db.query(Question)
    if year:
        search = '%%{}%%'.format(year)  # keyword는 화면에서 전달 받은 값
        question_list = question_list \
            .outerjoin(User) \
            .filter(Question.audit_year_start.ilike(search)|
                    Question.audit_year_end.ilike(search)
            )
            
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.audit_date.desc()) \
        .offset(skip).limit(limit).distinct().all() # 리스트 정렬 (진단일자 기준)
        
    return total, question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        audit_date=question_create.audit_date,
        audit_date_end=question_create.audit_date_end,
        audit_year_start=question_create.audit_year_start,
        audit_year_end=question_create.audit_year_end,
        file_name=question_create.file_name,
        file_path=question_create.file_path,
        pdf_file_name=question_create.pdf_file_name,
        pdf_file_path=question_create.pdf_file_path,
        user=user,
        auditor1 = question_create.auditor1,
        auditor2 = question_create.auditor2,
        auditor3 = question_create.auditor3,
        audit_type = question_create.audit_type,
        company = question_create.company,
        region = question_create.region,
        production = question_create.production,
        )
    
    db.add(db_question)
    db.commit()
    
def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    
    """ 작동 안됨
    db_question = Question(
        subject = question_update.subject,
        content = question_update.content,
        modify_date = datetime.now(),
    )
    """
    
    if ( question_update.file_path != None ) and (question_update.file_path != db_question.file_path):
        if os.path.exists(str(db_question.file_path)): #type: ignore
            os.remove(db_question.file_path) # type: ignore , 진단보고서 삭제      
    if ( question_update.pdf_file_path != None ) and (question_update.pdf_file_path != db_question.pdf_file_path):
        if os.path.exists(str(db_question.pdf_file_path)): #type: ignore
            os.remove(db_question.pdf_file_path) # type: ignore , 진단보고서 삭제     
             #print({"remove ----> db_quesiton:": db_question.file_path, "question_update:": question_update.file_path})

    db_question.subject = question_update.subject # type: ignore
    db_question.content = question_update.content # type: ignore
    db_question.modify_date = datetime.now() # type: ignore
    db_question.audit_date = question_update.audit_date # type: ignore
    db_question.audit_date_end = question_update.audit_date_end # type: ignore
    db_question.audit_year_start = question_update.audit_year_start # type: ignore
    db_question.audit_year_end = question_update.audit_year_end # type: ignore
    if question_update.file_name != None:
        db_question.file_name = question_update.file_name # type: ignore
    if question_update.file_path != None:
        db_question.file_path = question_update.file_path # type: ignore
    if question_update.pdf_file_name != None:
        db_question.pdf_file_name = question_update.pdf_file_name # type: ignore
    if question_update.pdf_file_path != None:
        db_question.pdf_file_path = question_update.pdf_file_path # type: ignore
    db_question.auditor1 = question_update.auditor1 # type: ignore
    db_question.auditor2 = question_update.auditor2 # type: ignore
    db_question.auditor3 = question_update.auditor3 # type: ignore
    db_question.audit_type = question_update.audit_type # type: ignore
    db_question.company = question_update.company # type: ignore
    db_question.region = question_update.region # type: ignore
    db_question.production = question_update.production # type: ignore
    
    db.add(db_question)
    db.commit()
    
def delete_question(db: Session, db_question: Question):
    
    if os.path.exists(str(db_question.file_path)): #type: ignore
        os.remove(db_question.file_path) # type: ignore , 진단보고서 삭제
    if os.path.exists(str(db_question.pdf_file_path)): #type: ignore
        os.remove(db_question.pdf_file_path) # type: ignore , 진단보고서 삭제
    
    db.delete(db_question)
    db.commit()
    

def get_query_list(db: Session, keyword: str = ''):
   
    question_list = db.query(Question)
    
    if keyword:
        keyword_list = keyword.split()
        search_list =[]
        for key in keyword_list:
            search_list.append('%%{}%%'.format(key))
        
        for search in search_list:
            if search == search_list[0]:
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
            
            else:
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
    
    