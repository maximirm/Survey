from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repository.config.database import get_db
from app.repository.schemas import schemas
from app.services import survey_service

router = APIRouter()


@router.get("/surveys/{survey_id}", response_model=schemas.Survey)
async def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    return await survey_service.get_survey(db, survey_id)


@router.get("/surveys/by_creator/{creator_id}", response_model=list[schemas.Survey])
async def get_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return await survey_service.get_surveys_by_creator_id(db, creator_id)


@router.post("/surveys/", response_model=schemas.Survey)
async def create_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    return await survey_service.create_survey(db, survey)


@router.delete("/surveys/{survey_id}", response_model=dict)
async def delete_survey(survey_id: UUID, db: Session = Depends(get_db)):
    return await survey_service.delete_survey(db, survey_id)


@router.delete("/surveys/by_creator/{creator_id}", response_model=dict)
async def delete_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return await survey_service.delete_surveys_by_creator_id(db, creator_id)
