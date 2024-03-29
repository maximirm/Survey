import unittest
from uuid import uuid4

from fastapi.testclient import TestClient
from app.repository.schemas import schemas
from main import app
from tests.test_db.test_db_setup import setup_test_db


class TestSurveyIntegration(unittest.TestCase):

    def setUp(self):
        setup_test_db(app)
        self.client = TestClient(app)

    def test_survey_integration(self):
        # Create Survey
        survey_create_data = {
            "creator_id": str(uuid4()),
            "title": "Test Survey",
            "description": "Test Description",
            "is_public": False,
            "questions": [],
        }
        create_response = self.client.post("/surveys/", json=survey_create_data)
        assert create_response.status_code == 200
        created_survey = schemas.Survey(**create_response.json())

        # Get Survey
        get_response = self.client.get(f"/surveys/{created_survey.id}")
        assert get_response.status_code == 200
        retrieved_survey = schemas.Survey(**get_response.json())
        assert retrieved_survey == created_survey

        # Delete Survey
        delete_response = self.client.delete(f"/surveys/{created_survey.id}")
        assert delete_response.status_code == 200
        assert delete_response.json() == f"Survey with ID {str(created_survey.id)} deleted successfully"

        # Get Survey again but expect 404
        get_deleted_response = self.client.get(f"/surveys/{created_survey.id}")
        assert get_deleted_response.status_code == 404
        assert get_deleted_response.json() == {"detail": f"Survey with ID {str(created_survey.id)} not found"}
