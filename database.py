from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./eduverse.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String) # 'faculty' or 'student'
    
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)
    semester = Column(Integer)
    attendance = Column(Float)
    assignment_score = Column(Float)
    quiz_score = Column(Float)
    mid_exam = Column(Float)
    final_exam = Column(Float)
    study_hours = Column(Float)
    previous_gpa = Column(Float)
    participation = Column(String)
    result = Column(String)
    
    # ML Outputs
    risk_score = Column(Float, nullable=True)
    risk_category = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
