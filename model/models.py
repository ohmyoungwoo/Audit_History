from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    audit_flag = Column(Text, nullable=True)
    subject = Column(String, nullable=False) # 제목
    content = Column(Text, nullable=False) # 상세내용
    create_date = Column(DateTime, nullable=False) # 작성일자
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True) # 작성자 ID
    user = relationship("User", backref="question_users") # 작성자 이름
    modify_date = Column(DateTime, nullable=True) # 변경날자
    audit_date = Column(DateTime, nullable=True) # 진단날자
    file_name = Column(String, nullable=True) # 진단보고서 파일이름
    file_path = Column(String, nullable=True) # 진단보고서 저장위치 + 파일이름
    auditor1 = Column(String, nullable=True) # 진단자1
    auditor2 = Column(String, nullable=True) # 진단자2
    audit_type = Column(String, nullable=True) # 진단 구분 (품질체제진단, 이슈진단)
    region = Column(String, nullable=True) # 지역(창원, 구미, 평택, LGETH, LGEMN ... )
    production = Column(String, nullable=True) # 제품군 (냉장고, 세탁기, 에어컨 ...)
    

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=False, nullable=False)
    password = Column(String, nullable = False)
    email = Column(String, unique=True, nullable=False)
    no_company = Column(String, unique=True, nullable=False)
    