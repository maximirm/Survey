from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.repository.config.database import get_db
from app.repository.schemas import schemas
from app.services import question_service

router = APIRouter()


@router.get("/questions/{question_id}/", response_model=schemas.Question)
async def get_question(question_id: UUID, db: Session = Depends(get_db)):
    return await question_service.get_question(db, question_id)

#dont need delete
@router.get("/questions/by_survey/{survey_id}/", response_model=list[schemas.Question])
async def get_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return await question_service.get_questions_by_survey_id(db, survey_id)


@router.post("/questions/", response_model=schemas.Question)
async def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return await question_service.create_question(db, question)

#dont need delete
@router.delete("/questions/{question_id}/", response_model=dict)
async def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    return await question_service.delete_question(db, question_id)

#dont need delete
@router.delete("/questions/by_survey/{survey_id}/", response_model=dict)
async def delete_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return await question_service.delete_questions_by_survey_id(db, survey_id)
