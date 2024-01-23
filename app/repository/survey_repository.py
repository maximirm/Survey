from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.repository.models.models import Survey
from app.repository.schemas import schemas


async def get_survey(db: Session, survey_id: UUID):
    statement = select(Survey).filter(Survey.id == survey_id)
    result = db.execute(statement)
    return result.scalars().first()


async def get_all_surveys(db: Session):
    return db.execute(select(Survey)).scalars().all()


async def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    statement = select(Survey).filter(Survey.creator_id == creator_id)
    result = db.execute(statement)
    return result.scalars().all()


async def create_survey(db: Session, survey: schemas.SurveyCreate):
    db_survey = Survey(**dict(survey))
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


async def delete_survey(db: Session, survey_id: UUID):
    db_survey = await get_survey(db, survey_id)
    if db_survey:
        db.delete(db_survey)
        db.commit()
        return db_survey
    return None


async def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    statement = select(Survey).filter(Survey.creator_id == creator_id)
    result = db.execute(statement)
    db_surveys = result.scalars().all()

    for survey in db_surveys:
        db.delete(survey)

    db.commit()
    return db_surveys
