from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.repository.models.models import Response
from app.repository.schemas import schemas


async def get_response(db: Session, response_id: UUID):
    statement = select(Response).filter(Response.id == response_id)
    result = db.execute(statement)
    return result.scalars().first()


async def get_responses_by_question_id(db: Session, question_id: UUID):
    statement = select(Response).filter(Response.question_id == question_id)
    result = db.execute(statement)
    return result.scalars().all()


async def create_response(db: Session, response: schemas.ResponseCreate):
    db_response = Response(**dict(response))
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


async def delete_response(db: Session, response_id: UUID):
    db_response = await get_response(db, response_id)
    db.delete(db_response)
    db.commit()
    return db_response


async def delete_responses_by_question_id(db: Session, question_id: UUID):
    statement = select(Response).filter(Response.question_id == question_id)
    result = db.execute(statement)
    db_responses = await result.scalars().all()

    for response in db_responses:
        db.delete(response)

    db.commit()
    return db_responses
