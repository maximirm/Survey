from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID

from app.controller.schemas import schemas
from app.database.models import models


def get_survey(db: Session, survey_id: UUID):
    return db.query(models.Survey) \
        .filter(models.Survey.id == survey_id) \
        .first()


def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    return db.query(models.Survey)\
        .filter(models.Survey.creator_id == creator_id)\
        .all()


def create_survey(db: Session, survey: schemas.SurveyCreate):
    db_survey = models.Survey(**dict(survey))
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


def delete_survey(db: Session, survey_id: UUID):
    survey = get_survey(db, survey_id)
    if survey is None:
        return {"error": "Survey not found"}
    try:
        __delete_responses_by_survey_id(db, survey_id)
        __delete_questions_by_survey_id(db, survey_id)
        db.delete(survey)
        db.commit()
        return {"message": "Survey deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        return {"error": "IntegrityError", "message": str(e)}


def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    surveys = get_surveys_by_creator_id(db, creator_id)
    for survey in surveys:
        delete_survey(db, survey.id)
    return {"message": "Surveys deleted successfully"}


def __delete_responses_by_survey_id(db: Session, survey_id: UUID):
    db.query(models.Response)\
        .filter(models.Response.question_id
                .in_(db.query(models.Question.id)
                     .filter_by(survey_id=survey_id)
                     )
                )\
        .delete(synchronize_session=False)


def __delete_questions_by_survey_id(db: Session, survey_id: UUID):
    db.query(models.Question)\
        .filter_by(survey_id=survey_id)\
        .delete(synchronize_session=False)
