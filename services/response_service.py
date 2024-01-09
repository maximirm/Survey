from sqlalchemy.orm import Session
from uuid import UUID

from controller.schemas import schemas
from database.crud import response_crud


def get_response(db: Session, response_id: UUID):
    return response_crud.get_response(db, response_id)


def get_responses_by_question_id(db: Session, question_id: UUID):
    return response_crud.get_responses_by_question_id(db, question_id)


def create_response(db: Session, response: schemas.ResponseCreate):
    return response_crud.create_response(db, response)


def delete_response(db: Session, response_id: UUID):
    return response_crud.delete_response(db, response_id)


def delete_responses_by_question_id(db: Session, question_id: UUID):
    return response_crud.delete_responses_by_question_id(db, question_id)
