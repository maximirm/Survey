from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.repository.models import models
from app.repository.schemas import schemas


def get_question(db: Session, question_id: UUID):
    return db.query(models.Question) \
        .filter(models.Question.id == question_id) \
        .first()


def get_questions_by_survey_id(db: Session, survey_id: UUID):
    return db.query(models.Question) \
        .filter(models.Question.survey_id == survey_id) \
        .all()


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**dict(question))
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: UUID):
    db_question = db.query(models.Question)\
        .filter(models.Question.id == question_id)\
        .first()
    db.delete(db_question)
    db.commit()
    return db_question


def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    db_questions = db.query(models.Question) \
        .filter(models.Question.survey_id == survey_id)\
        .all()
    for question in db_questions:
        db.delete(question)
    db.commit()
    return db_questions
