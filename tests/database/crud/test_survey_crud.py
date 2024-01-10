import unittest
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from app.database.crud import survey_crud
from app.database.models import models


class TestSurveyCrud(unittest.TestCase):
    def setUp(self):
        self.db = Session()

    @patch('app.database.crud.survey_crud.get_survey',
           return_value=models.Survey(
               id="10000000-0000-0000-0000-000000000000",
               creator_id="20000000-0000-0000-0000-000000000000"
           ))
    def test_get_survey(self, mock_get_survey):
        survey_id = "10000000-0000-0000-0000-000000000000"

        result = survey_crud.get_survey(self.db, survey_id)
        self.assertEqual(result.id, survey_id)

        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch('app.database.crud.survey_crud.get_surveys_by_creator_id',
           return_value=[
               models.Survey(
                   id="10000000-0000-0000-0000-000000000000",
                   creator_id="20000000-0000-0000-0000-000000000000"
               ),
               models.Survey(
                   id="11111111-0000-0000-0000-000000000000",
                   creator_id="20000000-0000-0000-0000-000000000000"
               )
           ])
    def test_get_surveys_by_creator(self, mock_get_surveys_by_creator_id):
        creator_id = "20000000-0000-0000-0000-000000000000"
        survey_id_1 = "10000000-0000-0000-0000-000000000000"
        survey_id_2 = "11111111-0000-0000-0000-000000000000"

        result = survey_crud.get_surveys_by_creator_id(self.db, creator_id)

        self.assertTrue(len(result), 2)
        self.assertEqual(result[0].id, survey_id_1)
        self.assertEqual(result[1].id, survey_id_2)
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)
