from sqlalchemy.orm import Session
from uuid import UUID

from app.services.exceptions.foreign_key_not_found_exception import ForeignKeyNotFoundException
from app.services.exceptions.response_not_found_exception import ResponseNotFoundException
from app.database.schemas import schemas
from app.database.crud import response_crud
from sqlalchemy.exc import IntegrityError

from app.services.utils.converter import convert_response_model_to_schema


def get_response(db: Session, response_id: UUID):
    db_response = response_crud.get_response(db, response_id)
    if db_response is None:
        raise ResponseNotFoundException(f"Response with ID {str(response_id)} not found")
    return convert_response_model_to_schema(db_response)


def get_responses_by_question_id(db: Session, question_id: UUID):
    db_responses = response_crud.get_responses_by_question_id(db, question_id)
    if not db_responses:
        raise ResponseNotFoundException(f"No Responses for Question-ID {str(question_id)} found")
    return [convert_response_model_to_schema(db_response) for db_response in db_responses]


def create_response(db: Session, response: schemas.ResponseCreate):
    try:
        return convert_response_model_to_schema(response_crud.create_response(db, response))
    except IntegrityError:
        raise ForeignKeyNotFoundException(
            f"Can not create Response. No Question with ID {str(response.question_id)} found"
        )


def delete_response(db: Session, response_id: UUID):
    db_response = response_crud.delete_response(db, response_id)
    if db_response is None:
        raise ResponseNotFoundException(
            f"Response with ID {str(response_id)} not found"
        )
    return {"message": f"Response with ID {str(response_id)} deleted successfully"}


def delete_responses_by_question_id(db: Session, question_id: UUID):
    db_responses = response_crud.delete_responses_by_question_id(db, question_id)
    if not db_responses:
        raise ResponseNotFoundException(
            f"No Responses for Question-ID {str(question_id)} found"
        )
    return {"message": f"Responses for Question-ID {str(question_id)} deleted successfully"}
