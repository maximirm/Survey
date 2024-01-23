from sqlalchemy.orm import Session

from app.repository.models.models import Response
from app.repository.schemas import schemas


async def create_response(db: Session, response: schemas.ResponseCreate):
    db_response = Response(**dict(response))
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response
