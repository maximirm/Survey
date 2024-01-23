from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.repository.models.models import Question
from app.repository.schemas import schemas


async def get_question(db: Session, question_id: UUID):
    statement = select(Question).filter(Question.id == question_id)
    result = db.execute(statement)
    return result.scalars().first()


async def get_questions_by_survey_id(db: Session, survey_id: UUID):
    statement = select(Question).filter(Question.survey_id == survey_id)
    result = db.execute(statement)
    return result.scalars().all()


async def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = Question(**dict(question))
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


async def delete_question(db: Session, question_id: UUID):
    db_question = await get_question(db, question_id)

    if db_question:
        db.delete(db_question)
        db.commit()
        return db_question
    return None


async def delete_questions_by_survey_id(db: Session, survey_id: UUID):
    statement = select(Question).filter(Question.survey_id == survey_id)
    result = db.execute(statement)
    db_questions = await result.scalars().all()

    for question in db_questions:
        db.delete(question)
    db.commit()
    return db_questions