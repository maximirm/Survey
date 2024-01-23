from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repository.data_access import response_repository
from app.repository.schemas import schemas


async def create_response(db: Session, response: schemas.ResponseCreate):
    try:
        return await response_repository.create_response(db, response)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Can not create Response. No Question with ID {str(response.question_id)} found"
        )
