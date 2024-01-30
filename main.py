from fastapi import FastAPI
from app.api import survey_controller, question_controller, response_controller
from app.repository.config.database import engine
from app.repository.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(survey_controller.router, tags=["Surveys"])
app.include_router(question_controller.router, tags=["Questions"])
app.include_router(response_controller.router, tags=["Responses"])
