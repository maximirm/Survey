from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from controller.schemas import schemas
from database.database import get_db
from services import response_service

router = APIRouter()


@router.get("/responses/{response_id}", response_model=schemas.Response)
def get_response(response_id: UUID, db: Session = Depends(get_db)):
    db_response = response_service.get_response(db, response_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response


@router.get("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def get_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return response_service.get_responses_by_question_id(db, question_id)


@router.post("/responses/", response_model=schemas.Response)
def create_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    return response_service.create_response(db, response)


@router.delete("/responses/{response_id}", response_model=schemas.Response)
def delete_response(response_id: UUID, db: Session = Depends(get_db)):
    return response_service.delete_response(db, response_id)


@router.delete("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def delete_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return response_service.delete_responses_by_question_id(db, question_id)
