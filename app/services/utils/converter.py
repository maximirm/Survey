from app.repository.models.models import Survey as SurveyModel, Question as QuestionModel, Response as ResponseModel
from app.repository.schemas.schemas import Survey as SurveySchema, Question as QuestionSchema, Response as ResponseSchema


def convert_survey_model_to_schema(model: SurveyModel) -> SurveySchema:
    return SurveySchema(
        id=str(model.id),
        creator_id=str(model.creator_id),
        title=model.title,
        description=model.description,
        is_public=model.is_public,
        questions=[convert_question_model_to_schema(question) for question in model.questions]
    )


def convert_question_model_to_schema(model: QuestionModel) -> QuestionSchema:
    return QuestionSchema(
        id=str(model.id),
        survey_id=str(model.survey_id),
        order=model.order,
        question_text=model.question_text,
        type=model.type,
        options=model.options,
        responses=[convert_response_model_to_schema(response) for response in model.responses]
    )


def convert_response_model_to_schema(model: ResponseModel) -> ResponseSchema:
    return ResponseSchema(
        id=str(model.id),
        question_id=str(model.question_id),
        respondent_id=str(model.respondent_id) if model.respondent_id else None,
        response_text=model.response_text
    )
