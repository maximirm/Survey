import unittest
from unittest.mock import patch, MagicMock

from app.services.exceptions.survey_not_found_exception import SurveyNotFoundException

from app.services.survey_service import get_survey, get_surveys_by_creator_id, create_survey, delete_survey, \
    delete_surveys_by_creator_id
from uuid import uuid4


class TestSurveyService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()

    @patch("app.database.crud.survey_crud.get_survey")
    def test_get_survey(self, mock_get_survey):
        survey_id = uuid4()
        mock_survey = MagicMock()
        mock_get_survey.return_value = mock_survey

        result = get_survey(self.db, survey_id)

        self.assertEqual(mock_survey, result)
        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.get_survey", return_value=None)
    def test_get_survey_not_found(self, mock_get_survey):
        survey_id = uuid4()

        with self.assertRaises(SurveyNotFoundException):
            get_survey(self.db, survey_id)
        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.get_surveys_by_creator_id")
    def test_get_surveys_by_creator_id(self, mock_get_surveys_by_creator_id):
        survey_id = uuid4()
        mock_survey_1 = MagicMock()
        mock_survey_2 = MagicMock()
        mock_get_surveys_by_creator_id.return_value = [mock_survey_1, mock_survey_2]

        result = get_surveys_by_creator_id(self.db, survey_id)

        self.assertEqual(2, len(result))
        self.assertEqual(mock_survey_1, result[0])
        self.assertEqual(mock_survey_2, result[1])
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.get_surveys_by_creator_id", return_value=None)
    def test_get_surveys_by_creator_id_not_found(self, mock_get_surveys_by_creator_id):
        survey_id = uuid4()

        with self.assertRaises(SurveyNotFoundException):
            get_surveys_by_creator_id(self.db, survey_id)
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.create_survey")
    def test_create_survey(self, mock_create_survey):
        mock_survey = MagicMock()
        mock_create_survey.return_value = mock_survey

        result = create_survey(self.db, mock_survey)

        self.assertEqual(mock_survey, result)
        mock_create_survey.assert_called_once_with(self.db, mock_survey)