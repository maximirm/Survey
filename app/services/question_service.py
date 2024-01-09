from uuid import UUID

from app.services.schemas import schemas
from app.database.crud import question_crud
from sqlalchemy.orm import Session


def get_question(db: Session, question_id: UUID):
    return question_crud.get_question(db, question_id)


def get_questions_by_survey_id(db: Session, survey_id: UUID):
    return question_crud.get_questions_by_survey_id(db, survey_id)


def create_question(db: Session, question: schemas.QuestionCreate):
    return question_crud.create_question(db, question)


def delete_question(db: Session, question_id: UUID):
    return question_crud.delete_question(db, question_id)


def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    return question_crud.delete_questions_by_survey_id(db, survey_id)
