import asyncio
import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from fastapi import HTTPException

from app.repository.schemas.schemas import Survey
from app.services import survey_service


class TestSurveyService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()

    @patch("app.repository.survey_repository.get_survey")
    def test_get_survey(self, mock_get_survey):
        survey_id = uuid4()

        test_survey = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            is_public=False,
            questions=[]
        )
        mock_get_survey.return_value = test_survey

        result = asyncio.run(survey_service.get_survey(self.db, survey_id))

        self.assertEqual(test_survey, result)
        self.assertIsInstance(result, Survey)
        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.get_survey", return_value=None)
    def test_get_survey_not_found(self, mock_get_survey):
        survey_id = uuid4()

        with self.assertRaises(HTTPException):
            asyncio.run(survey_service.get_survey(self.db, survey_id))
        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.get_surveys_by_creator_id")
    def test_get_surveys_by_creator_id(self, mock_get_surveys_by_creator_id):
        survey_id = uuid4()
        test_survey_1 = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            is_public=False,
            questions=[]
        )
        test_survey_2 = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            is_public=False,
            questions=[]
        )
        mock_get_surveys_by_creator_id.return_value = [test_survey_1, test_survey_2]

        result = asyncio.run(survey_service.get_surveys_by_creator_id(self.db, survey_id))

        self.assertEqual(2, len(result))
        self.assertEqual(test_survey_1, result[0])
        self.assertEqual(test_survey_2, result[1])
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.get_surveys_by_creator_id", return_value=None)
    def test_get_surveys_by_creator_id_not_found(self, mock_get_surveys_by_creator_id):
        survey_id = uuid4()

        result = asyncio.run(survey_service.get_surveys_by_creator_id(self.db, survey_id))

        self.assertEqual([], result)
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.create_survey")
    def test_create_survey(self, mock_create_survey):
        survey_id = uuid4()
        test_survey = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            is_public=False,
            questions=[]
        )
        mock_create_survey.return_value = test_survey

        result = asyncio.run(survey_service.create_survey(self.db, test_survey))

        self.assertEqual(test_survey, result)
        mock_create_survey.assert_called_once_with(self.db, test_survey)

    @patch("app.repository.survey_repository.delete_survey")
    def test_delete_survey(self, mock_delete_survey):
        survey_id = uuid4()
        mock_survey = MagicMock()
        mock_delete_survey.return_value = mock_survey

        result = asyncio.run(survey_service.delete_survey(self.db, survey_id))

        self.assertEqual(f"Survey with ID {str(survey_id)} deleted successfully", result)
        mock_delete_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.delete_survey", return_value=None)
    def test_delete_survey_not_found(self, mock_delete_survey):
        survey_id = uuid4()

        with self.assertRaises(HTTPException):
            asyncio.run(survey_service.delete_survey(self.db, survey_id))
        mock_delete_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.repository.survey_repository.delete_surveys_by_creator_id")
    def test_delete_surveys_by_creator_id(self, mock_delete_surveys_by_creator_id):
        creator_id = uuid4()
        mock_surveys = MagicMock()
        mock_delete_surveys_by_creator_id.return_value = mock_surveys

        result = asyncio.run(survey_service.delete_surveys_by_creator_id(self.db, creator_id))

        self.assertEqual(f"Surveys for creator-ID {str(creator_id)} deleted successfully", result)
        mock_delete_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)

    @patch("app.repository.survey_repository.delete_surveys_by_creator_id", return_value=None)
    def test_delete_surveys_by_creator_id_not_found(self, mock_delete_surveys_by_creator_id):
        creator_id = uuid4()

        result = asyncio.run(survey_service.delete_surveys_by_creator_id(self.db, creator_id))
        self.assertEqual(result, f"No Surveys for creator-ID {str(creator_id)} found")
        mock_delete_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)
