import unittest
from unittest.mock import ANY
from unittest.mock import patch, MagicMock
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.repository.schemas import schemas
from main import app
from tests.test_db.test_db_setup import setup_test_db


class TestSurveyController(unittest.TestCase):

    def setUp(self):
        setup_test_db(app)
        self.client = TestClient(app)

    @patch("app.services.survey_service.get_survey")
    def test_get_survey(self, mock_get_survey):
        survey_id = uuid4()
        mock_survey = MagicMock(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            is_public=False
        )
        mock_get_survey.return_value = mock_survey

        response = self.client.get(f"/surveys/{survey_id}")

        assert response.status_code == 200
        assert response.json() == {
            "creator_id": mock_survey.creator_id,
            "title": mock_survey.title,
            "description": mock_survey.description,
            "is_public": mock_survey.is_public,
            "id": mock_survey.id,
            "questions": [],
        }
        mock_get_survey.assert_called_once_with(ANY, survey_id)

    @patch("app.services.survey_service.get_survey")
    def test_get_survey_not_found(self, mock_get_survey):
        survey_id = uuid4()
        mock_get_survey.side_effect = HTTPException(status_code=404, detail="Survey not found")

        response = self.client.get(f"/surveys/{survey_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Survey not found"}
        mock_get_survey.assert_called_once_with(ANY, survey_id)

    @patch("app.services.survey_service.get_surveys_by_creator_id")
    def test_get_surveys_by_creator_id_success(self, mock_get_surveys):
        creator_id = uuid4()
        mock_surveys = [
            MagicMock(
                id=str(uuid4()),
                creator_id=str(creator_id),
                title="Survey 1",
                description="Description 1",
                is_public=False
            ),
            MagicMock(
                id=str(uuid4()),
                creator_id=str(creator_id),
                title="Survey 2",
                description="Description 2",
                is_public=False
            ),
        ]
        mock_get_surveys.return_value = mock_surveys

        response = self.client.get(f"/surveys/by_creator/{creator_id}")

        assert response.status_code == 200
        assert response.json() == [
            {
                "creator_id": survey.creator_id,
                "title": survey.title,
                "description": survey.description,
                "is_public": False,
                "id": survey.id,
                "questions": [],
            }
            for survey in mock_surveys
        ]
        mock_get_surveys.assert_called_once_with(ANY, creator_id)

    @patch("app.services.survey_service.get_surveys_by_creator_id")
    def test_get_surveys_by_creator_id_not_found(self, mock_get_surveys):
        creator_id = uuid4()
        mock_get_surveys.side_effect = HTTPException(
            status_code=404,
            detail="Surveys not found"
        )

        response = self.client.get(f"/surveys/by_creator/{creator_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Surveys not found"}
        mock_get_surveys.assert_called_once_with(ANY, creator_id)

    @patch("app.services.survey_service.create_survey")
    def test_create_survey(self, mock_create_survey):
        survey_id = uuid4()
        survey_create_data = {
            "creator_id": str(uuid4()),
            "title": "Survey Title",
            "description": "Survey Description",
            "is_public": False,
        }
        mock_survey = MagicMock(id=str(survey_id), **survey_create_data)
        mock_create_survey.return_value = mock_survey

        response = self.client.post("/surveys/", json=survey_create_data)

        assert response.status_code == 200
        assert response.json() == {
            "id": mock_survey.id,
            "questions": [],
            **survey_create_data,
        }
        mock_create_survey.assert_called_once_with(ANY, schemas.SurveyCreate(**survey_create_data))

    @patch("app.services.survey_service.delete_survey")
    def test_delete_survey(self, mock_delete_survey):
        survey_id = uuid4()
        mock_delete_survey.return_value = {"message": f"Survey with ID {survey_id} deleted successfully"}

        response = self.client.delete(f"/surveys/{survey_id}")

        assert response.status_code == 200
        assert response.json() == {"message": f"Survey with ID {survey_id} deleted successfully"}
        mock_delete_survey.assert_called_once_with(ANY, survey_id)

    @patch("app.services.survey_service.delete_survey")
    def test_delete_survey_not_found(self, mock_delete_survey):
        survey_id = uuid4()
        mock_delete_survey.side_effect = HTTPException(
            status_code=404,
            detail="Survey not found"
        )

        response = self.client.delete(f"/surveys/{survey_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Survey not found"}
        mock_delete_survey.assert_called_once_with(ANY, survey_id)

    @patch("app.services.survey_service.delete_surveys_by_creator_id")
    def test_delete_surveys_by_creator_id(self, mock_delete_surveys):
        creator_id = uuid4()
        mock_delete_surveys.return_value = "Surveys deleted successfully"

        response = self.client.delete(f"/surveys/by_creator/{creator_id}")

        assert response.status_code == 200
        assert response.json() == "Surveys deleted successfully"
        mock_delete_surveys.assert_called_once_with(ANY, creator_id)

    @patch("app.services.survey_service.delete_surveys_by_creator_id")
    def test_delete_surveys_by_creator_id_not_found(self, mock_delete_surveys):
        creator_id = uuid4()
        mock_delete_surveys.return_value = f"No Surveys for creator-ID {str(creator_id)} found"

        response = self.client.delete(f"/surveys/by_creator/{creator_id}")

        assert response.status_code == 200
        assert response.json() == f"No Surveys for creator-ID {str(creator_id)} found"

        mock_delete_surveys.assert_called_once_with(ANY, creator_id)
