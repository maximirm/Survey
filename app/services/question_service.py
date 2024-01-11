from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.data_access import question_access
from app.database.schemas import schemas
from app.services.exceptions.foreign_key_not_found_exception import ForeignKeyNotFoundException
from app.services.exceptions.question_not_found_exception import QuestionNotFoundException
from app.services.utils.converter import convert_question_model_to_schema


def get_question(db: Session, question_id: UUID):
    db_question = question_access.get_question(db, question_id)
    if db_question is None:
        raise QuestionNotFoundException(
            f"Question with ID {str(question_id)} not found"
        )
    return convert_question_model_to_schema(db_question)


def get_questions_by_survey_id(db: Session, survey_id: UUID):
    db_questions = question_access.get_questions_by_survey_id(db, survey_id)
    if not db_questions:
        raise QuestionNotFoundException(
            f"No Questions for Survey-ID {str(survey_id)} found"
        )
    return [convert_question_model_to_schema(db_question) for db_question in db_questions]


def create_question(db: Session, question: schemas.QuestionCreate):
    try:
        return convert_question_model_to_schema(question_access.create_question(db, question))
    except IntegrityError:
        raise ForeignKeyNotFoundException(
            f"Can not create Question. No Survey with ID {str(question.survey_id)} found"
        )


def delete_question(db: Session, question_id: UUID):
    db_question = question_access.delete_question(db, question_id)
    if db_question is None:
        raise QuestionNotFoundException(
            f"Question with ID {str(question_id)} not found"
        )
    return {"message": f"Question with ID {str(question_id)} deleted successfully"}


def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    db_questions = question_access.delete_questions_by_survey_id(db, survey_id)
    if not db_questions:
        raise QuestionNotFoundException(
            f"No Questions for Survey-ID {str(survey_id)} found"
        )
    return {"message": f"Questions for Survey-ID {str(survey_id)} deleted successfully"}
