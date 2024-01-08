from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/surveys/{survey_id}", response_model=schemas.Survey)
def read_survey(survey_id: UUID, db: Session = Depends(get_db)):
    db_survey = crud.get_survey(db, survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey


@app.get("/surveys/by_creator/{creator_id}", response_model=list[schemas.Survey])
def read_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return crud.get_surveys_by_creator_id(db, creator_id)


@app.post("/surveys/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    return crud.create_survey(db, survey)


@app.delete("/surveys/{survey_id}", response_model=dict)
def delete_survey(survey_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_survey(db, survey_id)


@app.delete("/surveys/by_creator/{creator_id}", response_model=dict)
def delete_surveys_by_creator_id(creator_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_surveys_by_creator_id(db, creator_id)


@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id: UUID, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.get("/questions/by_survey/{survey_id}", response_model=list[schemas.Question])
def read_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return crud.get_questions_by_survey_id(db, survey_id)


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question)


@app.delete("/questions/{question_id}", response_model=dict)
def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_question(db, question_id)


@app.delete("/questions/by_survey/{survey_id}", response_model=dict)
def delete_questions_by_survey_id(survey_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_questions_by_survey_id(db, survey_id)


@app.get("/responses/{response_id}", response_model=schemas.Response)
def read_response(response_id: UUID, db: Session = Depends(get_db)):
    db_response = crud.get_response(db, response_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response


@app.get("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def read_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return crud.get_responses_by_question_id(db, question_id)


@app.post("/responses/", response_model=schemas.Response)
def create_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    return crud.create_response(db, response)


@app.delete("/responses/{response_id}", response_model=schemas.Response)
def delete_response(response_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_response(db, response_id)


@app.delete("/responses/by_question/{question_id}", response_model=list[schemas.Response])
def delete_responses_by_question_id(question_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_responses_by_question_id(db, question_id)
