# models/user.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 기본 베이스 클래스 생성
Base = declarative_base()

class User(Base):
    """
    사용자 정보 테이블 모델
    - username: 고유한 사용자 이름
    - email: 이메일 주소
    - registered_at: 가입 일시 (기본값: 현재 시간)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
