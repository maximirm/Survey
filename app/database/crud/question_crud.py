from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID

from app.api.schemas import schemas
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


def delete_question(db: Session, question_id: UUID):
    question = get_question(db, question_id)
    if question is None:
        return {"error": "Question not found"}
    try:
        __delete_responses_by_question_id(db, question_id)
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        return {"error": "IntegrityError", "message": str(e)}


def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    questions = get_questions_by_survey_id(db, survey_id)
    for question in questions:
        delete_question(db, question.id)
    return {"message": "Questions deleted successfully"}


def __delete_responses_by_question_id(db: Session, question_id: UUID):
    db.query(models.Response)\
        .filter_by(question_id=question_id)\
        .delete(synchronize_session=False)
