import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from app.database.schemas.schemas import Survey
from app.services.exceptions.survey_not_found_exception import SurveyNotFoundException
from app.services.survey_service import get_survey, get_surveys_by_creator_id, create_survey, delete_survey, \
    delete_surveys_by_creator_id


class TestSurveyService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()

    @patch("app.database.crud.survey_crud.get_survey")
    def test_get_survey(self, mock_get_survey):
        survey_id = uuid4()

        test_survey = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            questions=[]
        )
        mock_get_survey.return_value = test_survey

        result = get_survey(self.db, survey_id)

        self.assertEqual(test_survey, result)
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
        test_survey_1 = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            questions=[]
        )
        test_survey_2 = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            questions=[]
        )
        mock_get_surveys_by_creator_id.return_value = [test_survey_1, test_survey_2]

        result = get_surveys_by_creator_id(self.db, survey_id)

        self.assertEqual(2, len(result))
        self.assertEqual(test_survey_1, result[0])
        self.assertEqual(test_survey_2, result[1])
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.get_surveys_by_creator_id", return_value=None)
    def test_get_surveys_by_creator_id_not_found(self, mock_get_surveys_by_creator_id):
        survey_id = uuid4()

        with self.assertRaises(SurveyNotFoundException):
            get_surveys_by_creator_id(self.db, survey_id)
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.create_survey")
    def test_create_survey(self, mock_create_survey):
        survey_id = uuid4()
        test_survey = Survey(
            id=str(survey_id),
            creator_id=str(uuid4()),
            title="Survey Title",
            description="Survey Description",
            questions=[]
        )
        mock_create_survey.return_value = test_survey

        result = create_survey(self.db, test_survey)

        self.assertEqual(test_survey, result)
        mock_create_survey.assert_called_once_with(self.db, test_survey)

    @patch("app.database.crud.survey_crud.delete_survey")
    def test_delete_survey(self, mock_delete_survey):
        survey_id = uuid4()
        mock_survey = MagicMock()
        mock_delete_survey.return_value = mock_survey

        result = delete_survey(self.db, survey_id)

        self.assertEqual(result, {"message": f"Survey with ID {str(survey_id)} deleted successfully"})
        mock_delete_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.delete_survey", return_value=None)
    def test_delete_survey_not_found(self, mock_delete_survey):
        survey_id = uuid4()

        with self.assertRaises(SurveyNotFoundException):
            delete_survey(self.db, survey_id)
        mock_delete_survey.assert_called_once_with(self.db, survey_id)

    @patch("app.database.crud.survey_crud.delete_surveys_by_creator_id")
    def test_delete_surveys_by_creator_id(self, mock_delete_surveys_by_creator_id):
        creator_id = uuid4()
        mock_surveys = MagicMock()
        mock_delete_surveys_by_creator_id.return_value = mock_surveys

        result = delete_surveys_by_creator_id(self.db, creator_id)

        self.assertEqual(result, {"message": f"Surveys for creator-ID {str(creator_id)} deleted successfully"})
        mock_delete_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)

    @patch("app.database.crud.survey_crud.delete_surveys_by_creator_id", return_value=None)
    def test_delete_surveys_by_creator_id_not_found(self, mock_delete_surveys_by_creator_id):
        creator_id = uuid4()

        with self.assertRaises(SurveyNotFoundException):
            delete_surveys_by_creator_id(self.db, creator_id)
        mock_delete_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)
