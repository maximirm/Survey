from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID

from app.services.schemas import schemas
from app.database.models import models


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



