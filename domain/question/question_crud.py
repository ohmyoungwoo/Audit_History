from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from model.models import Question, Answer, User
from sqlalchemy.orm import Session
from sqlalchemy import and_


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)  # keyword는 화면에서 전달 받은 값
        sub_query = db.query(Answer.question_id, Answer.content, User.username)\
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_ (sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |   # 진단 제목
                    Question.content.ilike(search) |   # 진단 상세 내용
                    User.username.ilike(search)        # 진단 작성자 이름
                    #sub_query.c.content.ilike(search) | # 답변내용, 
                    #sub_query.c.username.ilike(search) # 답변 작성자
            )
            # sub_query.c.question_id 에서 c 는 서브쿼리의 조회 항목이며, 
            # sub_query.c.question_id 는 서브쿼리의 조회 항목 중 question_id를 의미함
            # and_ 는 sqlalchemy 의 특이한 함수???
            
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc()) \
        .offset(skip).limit(limit).distinct().all()
        
    return total, question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user)
    
    db.add(db_question)
    db.commit()
    
def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question = Question(
        subject = question_update.subject,
        content = question_update.content,
        modify_date = datetime.now(),
    )
    
    db.add(db_question)
    db.commit()
    
def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()