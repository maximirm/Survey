from uuid import UUID

from sqlalchemy.orm import Session

from app.repository.data_access import survey_access
from app.repository.schemas import schemas
from app.services.exceptions.survey_not_found_exception import SurveyNotFoundException
from app.services.utils.converter import convert_survey_model_to_schema


def get_survey(db: Session, survey_id: UUID):
    db_survey = survey_access.get_survey(db, survey_id)
    if db_survey is None:
        raise SurveyNotFoundException(
            f"Survey with ID {str(survey_id)} not found"
        )
    return convert_survey_model_to_schema(db_survey)


def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = survey_access.get_surveys_by_creator_id(db, creator_id)
    if not db_surveys:
        raise SurveyNotFoundException(
            f"No Surveys for creator-ID {str(creator_id)} found"
        )
    return [convert_survey_model_to_schema(db_survey) for db_survey in db_surveys]


def create_survey(db: Session, survey: schemas.SurveyCreate):
    return convert_survey_model_to_schema(survey_access.create_survey(db, survey))


def delete_survey(db: Session, survey_id: UUID):
    db_survey = survey_access.delete_survey(db, survey_id)
    if db_survey is None:
        raise SurveyNotFoundException(
            f"Survey with ID {str(survey_id)} not found"
        )
    return {"message": f"Survey with ID {str(survey_id)} deleted successfully"}


def delete_surveys_by_creator_id(db: Session, creator_id: UUID):
    db_surveys = survey_access.delete_surveys_by_creator_id(db, creator_id)
    if not db_surveys:
        raise SurveyNotFoundException(
            f"No Surveys for creator-ID {str(creator_id)} found"
        )
    return {"message": f"Surveys for creator-ID {str(creator_id)} deleted successfully"}
