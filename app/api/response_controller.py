from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.repository.config.database import get_db
from app.repository.schemas import schemas
from app.services import response_service

router = APIRouter()


@router.post("/responses/", response_model=schemas.Response)
async def create_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    return await response_service.create_response(db, response)
