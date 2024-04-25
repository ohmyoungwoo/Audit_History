from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from model.models import Question, User#, Answer
from sqlalchemy.orm import Session
from sqlalchemy import and_


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)  # keyword는 화면에서 전달 받은 값
        #sub_query = db.query(Answer.question_id, Answer.content, User.username)\
        #    .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .filter(Question.subject.ilike(search) |   # 진단 제목
                    Question.content.ilike(search) |   # 진단 상세 내용
                    User.username.ilike(search)        # 진단 작성자 이름
                    #sub_query.c.content.ilike(search) | # 답변내용, 
                    #sub_query.c.username.ilike(search) # 답변 작성자
            #.outerjoin(sub_query, and_ (sub_query.c.question_id == Question.id)) \
            )
            # sub_query.c.question_id 에서 c 는 서브쿼리의 조회 항목이며, 
            # sub_query.c.question_id 는 서브쿼리의 조회 항목 중 question_id를 의미함
            # and_ 는 sqlalchemy 의 특이한 함수???
            
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
        file_name=question_create.file_name,
        file_path=question_create.file_path,
        user=user,
        auditor1 = question_create.auditor1,
        auditor2 = question_create.auditor2,
        audit_type = question_create.audit_type,
        region = question_create.region,
        production = question_create.production,
        )
    
    db.add(db_question)
    db.commit()
    
def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    
    """ 수정이 작동 안됨
    db_question = Question(
        subject = question_update.subject,
        content = question_update.content,
        modify_date = datetime.now(),
    )
    """
    db_question.subject = question_update.subject # type: ignore
    db_question.content = question_update.content # type: ignore
    db_question.modify_date = datetime.now() # type: ignore
    db_question.audit_date = question_update.audit_date # type: ignore
    db_question.file_name = question_update.file_name # type: ignore
    db_question.file_path = question_update.file_path # type: ignore
    db_question.auditor1 = question_update.auditor1 # type: ignore
    db_question.auditor2 = question_update.auditor2 # type: ignore
    db_question.audit_type = question_update.audit_type # type: ignore
    db_question.region = question_update.region # type: ignore
    db_question.production = question_update.production # type: ignore
    
    
    db.add(db_question)
    db.commit()
    
def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()