from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from app.repository.schemas import schemas
from app.repository.models import models


def get_survey(db: Session, survey_id: UUID):
    return db.query(models.Survey) \
        .filter(models.Survey.id == survey_id) \
        .first()


def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    return db.query(models.Survey) \
        .filter(models.Survey.creator_id == creator_id) \
        .all()


def create_survey(db: Session, survey: schemas.SurveyCreate):
    db_survey = models.Survey(**dict(survey))
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


def delete_survey(db: Session, survey_id: UUID):
    db_survey = db.query(models.Survey) \
        .filter(models.Survey.id == survey_id) \
        .first()
    db.delete(db_survey)
    db.commit()
    return db_survey


def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = db.query(models.Survey) \
        .filter(models.Survey.creator_id == creator_id) \
        .all()
    for survey in db_surveys:
        db.delete(survey)
    db.commit()
    return db_surveys
