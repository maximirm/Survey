from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.controller.schemas import schemas
from app.database.database import get_db
from app.services import question_service

router = APIRouter()


@router.get("/questions/{question_id}", response_model=schemas.Question)
def get_question(question_id: UUID, db: Session = Depends(get_db)):
    db_question = question_service.get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.get("/questions/by_survey/{survey_id}", response_model=list[schemas.Question])
def get_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return question_service.get_questions_by_survey_id(db, survey_id)


@router.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return question_service.create_question(db, question)


@router.delete("/questions/{question_id}", response_model=dict)
def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    return question_service.delete_question(db, question_id)


@router.delete("/questions/by_survey/{survey_id}", response_model=dict)
def delete_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return question_service.delete_questions_by_survey_id(db, survey_id)
