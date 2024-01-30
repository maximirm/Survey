import unittest
from unittest.mock import patch, MagicMock, ANY
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.repository.schemas import schemas
from main import app
from tests.test_db.test_db_setup import setup_test_db


class TestResponseController(unittest.TestCase):

    def setUp(self):
        setup_test_db(app)
        self.client = TestClient(app)

    @patch("app.services.response_service.create_response")
    def test_create_question(self, mock_create_response):
        response_id = uuid4()
        response_create_data = {
            "question_id": str(uuid4()),
            "respondent_id": str(uuid4()),
            "response_text": ["Apfel", "Birne"]
            ,
        }
        mock_response = MagicMock(id=str(response_id), **response_create_data)
        mock_create_response.return_value = mock_response

        response = self.client.post("/responses/", json=response_create_data)

        assert response.status_code == 200
        assert response.json() == {
            "id": mock_response.id,
            **response_create_data
        }
        mock_create_response.assert_called_once_with(ANY, schemas.ResponseCreate(**response_create_data))

    @patch("app.services.response_service.create_response")
    def test_create_response_related_survey_not_found(self, mock_create_response):
        question_id = uuid4()
        response_create_data = {
            "question_id": str(question_id),
            "respondent_id": str(uuid4()),
            "response_text": ["Apfel", "Birne"]
            ,
        }
        mock_create_response.side_effect = HTTPException(
            status_code=400,
            detail=f"Can not create Response. No Question with ID {str(question_id)} found"
        )

        response = self.client.post("/responses/", json=response_create_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": f"Can not create Response. No Question with ID {str(question_id)} found"
        }
        mock_create_response.assert_called_once_with(ANY, schemas.ResponseCreate(**response_create_data))
