from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.exceptions.foreign_key_not_found_exception import ForeignKeyNotFoundException
from app.services.exceptions.question_not_found_exception import QuestionNotFoundException
from app.services.schemas import schemas
from app.database.config.database import get_db
from app.services import response_service

router = APIRouter()


@router.get("/responses/{response_id}", response_model=schemas.Response)
def get_response(response_id: UUID, db: Session = Depends(get_db)):
    try:
        return response_service.get_response(db, response_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def get_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    try:
        return response_service.get_responses_by_question_id(db, question_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/responses/", response_model=schemas.Response)
def create_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    try:
        return response_service.create_response(db, response)
    except ForeignKeyNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/responses/{response_id}", response_model=schemas.Response)
def delete_response(response_id: UUID, db: Session = Depends(get_db)):
    try:
        return response_service.delete_response(db, response_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def delete_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    try:
        return response_service.delete_responses_by_question_id(db, question_id)
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
