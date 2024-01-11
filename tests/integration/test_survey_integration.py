import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database.config.database import Base, engine
from app.database.schemas import schemas
from main import app


class TestSurveyIntegration(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_survey_integration(self):
        # Create Survey
        survey_create_data = {
            "creator_id": str(uuid4()),
            "title": "Integration Test Survey",
            "description": "Integration Test Description",
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
        assert delete_response.json() == {"message": f"Survey with ID {str(created_survey.id)} deleted successfully"}

        # Get Survey again but expect 404
        get_deleted_response = self.client.get(f"/surveys/{created_survey.id}")
        assert get_deleted_response.status_code == 404
        assert get_deleted_response.json() == {"detail": f"Survey with ID {str(created_survey.id)} not found"}
