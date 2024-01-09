import unittest
from typing import List
from unittest.mock import Mock
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.database.crud.survey_crud import get_survey, get_surveys_by_creator_id, create_survey, delete_survey
from app.database.exceptions.survey_not_found_exception import SurveyNotFoundException
from app.database.models import models
from app.services.schemas import schemas


class SurveyCrudTest(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock(spec=Session)
        self.uuid = uuid4()
        self.creator_id = uuid4()
        self.unknown_uuid = uuid4()
        self.survey1 = models.Survey(id=self.uuid, creator_id=self.creator_id)
        self.survey2 = models.Survey(id=self.uuid, creator_id=self.creator_id)

    def test_get_survey(self):
        self.mock_db.query().filter().first.return_value = self.survey1

        result = get_survey(self.mock_db, self.uuid)

        self.assertEqual(self.survey1, result)

    def test_get_survey_unknown_uuid(self):
        self.mock_db.query().filter().first.return_value = None

        with self.assertRaises(SurveyNotFoundException) as context:
            get_survey(self.mock_db, self.unknown_uuid)

        self.assertIn(str(self.unknown_uuid), str(context.exception))

    def test_get_surveys_by_creator_id(self):
        surveys = [self.survey1, self.survey2]
        self.mock_db.query().filter().all.return_value = surveys

        result = get_surveys_by_creator_id(self.mock_db, self.creator_id)

        self.assertEqual(surveys, result)

    def test_get_surveys_by_unknown_creator_id_failure(self):
        self.mock_db.query().filter().all.return_value = []

        with self.assertRaises(SurveyNotFoundException) as context:
            get_surveys_by_creator_id(self.mock_db, self.creator_id)

        self.assertIn(str(self.creator_id), str(context.exception))

    def test_create_survey(self):
        survey_create_data = {
            "title": "Sample Survey",
            "description": "for testing purposes.",
            "creator_id": self.creator_id
        }
        survey_create_payload = schemas.SurveyCreate(**survey_create_data)

        result = create_survey(self.mock_db, survey_create_payload)

        self.assertIsInstance(result, models.Survey)
        self.mock_db.add.assert_called_once_with(result)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(result)


    def test_delete_survey(self):
        self.mock_db.query().filter().first.return_value = self.survey1
        result = delete_survey(self.mock_db, self.uuid)

        self.assertEqual(result, {"message": "Survey deleted successfully"})
        self.mock_db.delete.assert_called_once_with(self.survey1)
        self.mock_db.commit.assert_called_once()
