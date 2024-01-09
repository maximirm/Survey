from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.database.database import Base
import uuid


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String)
    description = Column(String)
    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    order = Column(Integer)
    question_text = Column(String)
    type = Column(Integer, nullable=False)
    options = Column(ARRAY(String))
    survey = relationship("Survey", back_populates="questions")
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    respondent_id = Column(UUID(as_uuid=True))
    response_text = Column(ARRAY(String))
    question = relationship("Question", back_populates="responses")
