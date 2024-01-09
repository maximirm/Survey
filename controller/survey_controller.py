from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from controller.schemas import schemas
from database.database import get_db
from services import survey_service

router = APIRouter()


@router.get("/surveys/{survey_id}", response_model=schemas.Survey)
def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    db_survey = survey_service.get_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey


@router.get("/surveys/by_creator/{creator_id}", response_model=list[schemas.Survey])
def get_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return survey_service.get_surveys_by_creator_id(db, creator_id)


@router.post("/surveys/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    return survey_service.create_survey(db, survey)


@router.delete("/surveys/{survey_id}", response_model=dict)
def delete_survey(survey_id: UUID, db: Session = Depends(get_db)):
    return survey_service.delete_survey(db, survey_id)


@router.delete("/surveys/by_creator/{creator_id}", response_model=dict)
def delete_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return survey_service.delete_surveys_by_creator_id(db, creator_id)
