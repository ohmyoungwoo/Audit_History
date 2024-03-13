from model.models import Question
from sqlalchemy.orm import Session


def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.id)\
        .all()
        #.order_by(Question.create_date.desc())
    return question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question