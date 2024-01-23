from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repository.data_access import question_repository
from app.repository.schemas import schemas
from app.services.utils.converter import convert_question_model_to_schema


async def get_question(db: Session, question_id: UUID):
    db_question = await question_repository.get_question(db, question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with ID {str(question_id)} not found"
        )
    return convert_question_model_to_schema(db_question)


async def get_questions_by_survey_id(db: Session, survey_id: UUID):
    db_questions = await question_repository.get_questions_by_survey_id(db, survey_id)
    if not db_questions:
        raise HTTPException(
            status_code=404,
            detail=f"No Questions for Survey-ID {str(survey_id)} found"
        )
    return [convert_question_model_to_schema(db_question) for db_question in db_questions]


async def create_question(db: Session, question: schemas.QuestionCreate):
    try:
        return await question_repository.create_question(db, question)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Can not create Question. No Survey with ID {str(question.survey_id)} found"
        )


async def delete_question(db: Session, question_id: UUID):
    db_question = await question_repository.delete_question(db, question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with ID {str(question_id)} not found"
        )
    return {"message": f"Question with ID {str(question_id)} deleted successfully"}


async def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    db_questions = await question_repository.delete_questions_by_survey_id(db, survey_id)
    if not db_questions:
        raise HTTPException(
            status_code=404,
            detail=f"No Questions for Survey-ID {str(survey_id)} found"
        )
    return {"message": f"Questions for Survey-ID {str(survey_id)} deleted successfully"}
