from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID
from . import models, schemas


def get_survey(db: Session, survey_id: UUID):
    return db.query(models.Survey) \
        .filter(models.Survey.id == survey_id) \
        .first()


def get_surveys_by_creator_id(db: Session, creator_id: UUID):
    return db.query(models.Survey) \
        .filter(models.Survey.creator_id == creator_id) \
        .all()


def get_question(db: Session, question_id: UUID):
    return db.query(models.Question) \
        .filter(models.Question.id == question_id) \
        .first()


def get_questions_by_survey_id(db: Session, survey_id: UUID):
    return db.query(models.Question) \
        .filter(models.Question.survey_id == survey_id) \
        .all()


def get_response(db: Session, response_id: UUID):
    return db.query(models.Response) \
        .filter(models.Response.id == response_id) \
        .first()


def get_responses_by_question_id(db: Session, question_id: UUID):
    return db.query(models.Response) \
        .filter(models.Response.question_id == question_id) \
        .all()


def create_survey(db: Session, survey: schemas.SurveyCreate):
    db_survey = models.Survey(**dict(survey))
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**dict(question))
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def create_Response(db: Session, response: schemas.ResponseCreate):
    db_response = models.Response(**dict(response))
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


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


def delete_question(db: Session, question_id: UUID):
    question = get_question(db, question_id)
    if question is None:
        return {"error": "Question not found"}
    try:
        __delete_responses_by_question_id(db, question_id)
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        return {"error": "IntegrityError", "message": str(e)}


def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    questions = get_questions_by_survey_id(db, survey_id)
    for question in questions:
        delete_question(db, question.id)
    return {"message": "Questions deleted successfully"}


def __delete_responses_by_survey_id(db: Session, survey_id: UUID):
    db.query(models.Response).filter(models.Response.question_id.in_(
        db.query(models.Question.id).filter_by(survey_id=survey_id)
    )).delete(synchronize_session=False)


def __delete_questions_by_survey_id(db: Session, survey_id: UUID):
    db.query(models.Question).filter_by(survey_id=survey_id).delete(synchronize_session=False)


def __delete_responses_by_question_id(db: Session, question_id: UUID):
    db.query(models.Response).filter_by(question_id=question_id).delete(synchronize_session=False)


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
