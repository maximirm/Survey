import unittest
from unittest.mock import patch, MagicMock, ANY
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.repository.schemas import schemas
from main import app
from tests.test_db.test_db_setup import setup_test_db


class TestQuestionController(unittest.TestCase):

    def setUp(self):
        setup_test_db(app)
        self.client = TestClient(app)

    @patch("app.services.question_service.get_question")
    def test_get_question(self, mock_get_question):
        question_id = uuid4()
        mock_question = MagicMock(
            id=str(question_id),
            survey_id=str(uuid4()),
            order=3,
            question_text="This is a question",
            type=3,
            options=[]
        )
        mock_get_question.return_value = mock_question

        response = self.client.get(f"/questions/{question_id}")

        assert response.status_code == 200
        print(response.json())
        assert response.json() == {
            "id": mock_question.id,
            "survey_id": mock_question.survey_id,
            "order": mock_question.order,
            "question_text": mock_question.question_text,
            "type": mock_question.type,
            "options": mock_question.options,
            "responses": []
        }
        mock_get_question.assert_called_once_with(ANY, question_id)

    @patch("app.services.question_service.get_question")
    def test_get_question_not_found(self, mock_get_question):
        question_id = uuid4()
        mock_get_question.side_effect = HTTPException(
            status_code=404,
            detail=f"Question with ID {str(question_id)} not found"
        )

        response = self.client.get(f"/questions/{question_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": f"Question with ID {str(question_id)} not found"}
        mock_get_question.assert_called_once_with(ANY, question_id)

    @patch("app.services.question_service.create_question")
    def test_create_question(self, mock_create_question):
        question_id = uuid4()
        question_create_data = {
            "survey_id": str(uuid4()),
            "order": 1,
            "question_text": "question_text",
            "type": 1,
            "options": [],
        }
        mock_question = MagicMock(id=str(question_id), **question_create_data)
        mock_create_question.return_value = mock_question

        response = self.client.post("/questions/", json=question_create_data)

        assert response.status_code == 200
        assert response.json() == {
            "id": mock_question.id,
            "responses": [],
            **question_create_data
        }
        mock_create_question.assert_called_once_with(ANY, schemas.QuestionCreate(**question_create_data))

    @patch("app.services.question_service.create_question")
    def test_create_question_related_survey_not_found(self, mock_create_question):
        survey_id = uuid4()
        question_create_data = {
            "survey_id": str(survey_id),
            "order": 1,
            "question_text": "question_text",
            "type": 1,
            "options": [],
        }
        mock_create_question.side_effect = HTTPException(
            status_code=400,
            detail=f"Can not create Question. No Survey with ID {str(survey_id)} found"
        )

        response = self.client.post("/questions/", json=question_create_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Can not create Question. No Survey with ID {str(survey_id)} found"
        }
        mock_create_question.assert_called_once_with(ANY, schemas.QuestionCreate(**question_create_data))

    @patch("app.services.question_service.delete_question")
    def test_delete_question(self, mock_delete_question):
        question_id = uuid4()
        mock_delete_question.return_value = {"message": f"Question with ID {str(question_id)} deleted successfully"}

        response = self.client.delete(f"/questions/{question_id}")

        assert response.status_code == 200
        assert response.json() == {"message": f"Question with ID {str(question_id)} deleted successfully"}
        mock_delete_question.assert_called_once_with(ANY, question_id)

    @patch("app.services.question_service.delete_question")
    def test_delete_question_not_found(self, mock_delete_question):
        question_id = uuid4()
        mock_delete_question.side_effect = HTTPException(
            status_code=404,
            detail=f"Question with ID {str(question_id)} not found"
        )

        response = self.client.delete(f"/questions/{question_id}")

        assert response.status_code == 404
        assert response.json() == {
            "detail": f"Question with ID {str(question_id)} not found"
        }
        mock_delete_question.assert_called_once_with(ANY, question_id)
