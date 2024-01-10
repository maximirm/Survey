from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.exceptions.foreign_key_not_found_exception import ForeignKeyNotFoundException
from app.services.exceptions.question_not_found_exception import QuestionNotFoundException
from app.services.schemas import schemas
from app.database.config.database import get_db
from app.services import question_service


router = APIRouter()


@router.get("/questions/{question_id}", response_model=schemas.Question)
def get_question(question_id: UUID, db: Session = Depends(get_db)):
    try:
        return question_service.get_question(db, question_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/questions/by_survey/{survey_id}", response_model=list[schemas.Question])
def get_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    try:
        return question_service.get_questions_by_survey_id(db, survey_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    try:
        return question_service.create_question(db, question)
    except ForeignKeyNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/questions/{question_id}", response_model=dict)
def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    try:
        return question_service.delete_question(db, question_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/questions/by_survey/{survey_id}", response_model=dict)
def delete_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    try:
        return question_service.delete_questions_by_survey_id(db, survey_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

