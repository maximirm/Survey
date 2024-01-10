import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient
from main import app
from unittest.mock import ANY


class TestSurveyController(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.db = MagicMock()

    @patch("app.services.survey_service.get_survey")
    def test_get_survey(self, mock_get_survey):
        survey_id = uuid4()
        mock_survey = MagicMock()
        mock_survey.id = str(survey_id)
        mock_survey.creator_id = str(uuid4())
        mock_survey.title = "Survey Title"
        mock_survey.description = "Survey Description"

        mock_get_survey.return_value = mock_survey

        response = self.client.get(f"/surveys/{survey_id}")

        assert response.status_code == 200
        assert response.json() == {
            "creator_id": mock_survey.creator_id,
            "title": mock_survey.title,
            "description": mock_survey.description,
            "id": mock_survey.id,
            "questions": [],
        }

        mock_get_survey.assert_called_once_with(ANY, survey_id)
