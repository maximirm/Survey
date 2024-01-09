from uuid import UUID

from controller.schemas import schemas
from database.crud import survey_crud
from sqlalchemy.orm import Session


def get_survey(db: Session, survey_id: UUID):
    return survey_crud.get_survey(db, survey_id)


def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    return survey_crud.get_surveys_by_creator_id(db, creator_id)


def create_survey(db: Session, survey: schemas.SurveyCreate):
    return survey_crud.create_survey(db, survey)


def delete_survey(db: Session, survey_id: UUID):
    return survey_crud.delete_survey(db, survey_id)


def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    surveys = survey_crud.get_surveys_by_creator_id(db, creator_id)
    for survey in surveys:
        delete_survey(db, survey.id)
    return {"message": "Surveys deleted successfully"}
