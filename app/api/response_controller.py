from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.repository.config.database import get_db
from app.repository.schemas import schemas
from app.services import response_service

router = APIRouter()


@router.get("/responses/{response_id}/", response_model=schemas.Response)
async def get_response(response_id: UUID, db: Session = Depends(get_db)):
    return await response_service.get_response(db, response_id)


@router.get("/responses/by_question/{question_id}/", response_model=list[schemas.Response])
async def get_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return await response_service.get_responses_by_question_id(db, question_id)


@router.post("/responses/", response_model=schemas.Response)
async def create_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    return await response_service.create_response(db, response)


@router.delete("/responses/{response_id}/", response_model=schemas.Response)
async def delete_response(response_id: UUID, db: Session = Depends(get_db)):
    return await response_service.delete_response(db, response_id)


@router.delete("/responses/by_question/{question_id}/", response_model=list[schemas.Response])
async def delete_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return await response_service.delete_responses_by_question_id(db, question_id)
