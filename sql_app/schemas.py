from pydantic import BaseModel, UUID4
from typing import Optional, List


class ResponseBase(BaseModel):
    question_id: UUID4
    respondent_id: Optional[UUID4]
    response_text: List[str]


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase):
    id: UUID4

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    survey_id: UUID4
    order: int
    question_text: str
    type: int
    options: Optional[List[str]]


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: UUID4
    responses: list[Response] = []

    class Config:
        orm_mode = True


class SurveyBase(BaseModel):
    creator_id: UUID4
    title: str
    description: str


class SurveyCreate(SurveyBase):
    pass


class Survey(SurveyBase):
    id: UUID4
    questions: list[Question] = []

    class Config:
        orm_mode = True
