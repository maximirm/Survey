from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import survey_repository
from app.repository.schemas import schemas
from app.services.utils.converter import convert_survey_model_to_schema


async def get_survey(db: Session, survey_id: UUID):
    db_survey = await survey_repository.get_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(
            status_code=404,
            detail=f"Survey with ID {str(survey_id)} not found"
        )
    return convert_survey_model_to_schema(db_survey)


async def get_all_surveys(db: Session):
    db_surveys = await survey_repository.get_all_surveys(db)
    if not db_surveys:
        return []
    return [convert_survey_model_to_schema(db_survey) for db_survey in db_surveys]


async def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = await survey_repository.get_surveys_by_creator_id(db, creator_id)
    if not db_surveys:
        return []
    return [convert_survey_model_to_schema(db_survey) for db_survey in db_surveys]


async def create_survey(db: Session, survey: schemas.SurveyCreate):
    return await survey_repository.create_survey(db, survey)


async def delete_survey(db: Session, survey_id: UUID):
    db_survey = await survey_repository.delete_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(
            status_code=404,
            detail=f"Survey with ID {str(survey_id)} not found"
        )
    return f"Survey with ID {str(survey_id)} deleted successfully"


async def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = await survey_repository.delete_surveys_by_creator_id(db, creator_id)
    if db_surveys is None:
        return f"No Surveys for creator-ID {str(creator_id)} found"
    return f"Surveys for creator-ID {str(creator_id)} deleted successfully"
