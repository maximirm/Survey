from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.repository.config.database import get_db
from app.repository.schemas.schemas import Question, QuestionCreate
from app.services import question_service

router = APIRouter()


@router.get("/questions/{question_id}/", response_model=Question)
async def get_question(question_id: UUID, db: Session = Depends(get_db)):
    return await question_service.get_question(db, question_id)


@router.post(
    "/questions/",
    response_model=Question,
    responses={
        400: {
            "description": "Integrity Error",
            "content": {
                "application/json":
                    {
                        "example": {
                            "detail": "Can not create Question. No Survey with ID (uuid) found"}
                    }
            }
        }
    }
)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return await question_service.create_question(db, question)


@router.delete("/questions/{question_id}/", response_model=dict)
async def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    return await question_service.delete_question(db, question_id)
