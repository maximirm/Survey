from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.data_access import survey_access
from app.repository.schemas import schemas
from app.services.utils.converter import convert_survey_model_to_schema


async def get_survey(db: Session, survey_id: UUID):
    db_survey = await survey_access.get_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(
            status_code=404,
            detail=f"Survey with ID {str(survey_id)} not found"
        )
    return convert_survey_model_to_schema(db_survey)


async def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = await survey_access.get_surveys_by_creator_id(db, creator_id)
    if not db_surveys:
        raise HTTPException(
            status_code=404,
            detail=f"No Surveys for creator-ID {str(creator_id)} found"
        )
    return [convert_survey_model_to_schema(db_survey) for db_survey in db_surveys]


async def create_survey(db: Session, survey: schemas.SurveyCreate):
    return await survey_access.create_survey(db, survey)


async def delete_survey(db: Session, survey_id: UUID):
    db_survey = await survey_access.delete_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(
            status_code=404,
            detail=f"Survey with ID {str(survey_id)} not found"
        )
    return {"message": f"Survey with ID {str(survey_id)} deleted successfully"}


async def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = await survey_access.delete_surveys_by_creator_id(db, creator_id)
    if not db_surveys:
        raise HTTPException(
            status_code=404,
            detail=f"No Surveys for creator-ID {str(creator_id)} found"
        )
    return {"message": f"Surveys for creator-ID {str(creator_id)} deleted successfully"}
