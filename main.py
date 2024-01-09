from fastapi import FastAPI
from app.api import survey_controller, question_controller, response_controller
from app.database.database import engine
from app.database.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(survey_controller.router, tags=["surveys"])
app.include_router(question_controller.router, tags=["questions"])
app.include_router(response_controller.router, tags=["responses"])







