from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.exceptions.survey_not_found_exception import SurveyNotFoundException
from app.repository.schemas import schemas
from app.repository.config.database import get_db
from app.services import survey_service


router = APIRouter()


@router.get("/surveys/{survey_id}", response_model=schemas.Survey)
def get_survey(survey_id: UUID, db: Session = Depends(get_db)):
    try:
        return survey_service.get_survey(db, survey_id)
    except SurveyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/surveys/by_creator/{creator_id}", response_model=list[schemas.Survey])
def get_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    try:
        return survey_service.get_surveys_by_creator_id(db, creator_id)
    except SurveyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/surveys/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    return survey_service.create_survey(db, survey)


@router.delete("/surveys/{survey_id}", response_model=dict)
def delete_survey(survey_id: UUID, db: Session = Depends(get_db)):
    try:
        return survey_service.delete_survey(db, survey_id)
    except SurveyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/surveys/by_creator/{creator_id}", response_model=dict)
def delete_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    try:
        return survey_service.delete_surveys_by_creator_id(db, creator_id)
    except SurveyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
