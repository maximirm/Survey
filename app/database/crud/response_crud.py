from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.services.schemas import schemas
from app.database.models import models


def get_response(db: Session, response_id: UUID):
    return db.query(models.Response) \
        .filter(models.Response.id == response_id) \
        .first()


def get_responses_by_question_id(db: Session, question_id: UUID):
    return db.query(models.Response) \
        .filter(models.Response.question_id == question_id) \
        .all()


def create_response(db: Session, response: schemas.ResponseCreate):
    db_response = models.Response(**dict(response))
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def delete_response(db: Session, response_id: UUID):
    db_response = get_response(db, response_id)
    if db_response:
        db.delete(db_response)
        db.commit()
        return db_response


def delete_responses_by_question_id(db: Session, question_id: UUID):
    db_responses = get_responses_by_question_id(db, question_id)
    if db_responses:
        for db_response in db_responses:
            db.delete(db_response)
        db.commit()
        return db_responses
