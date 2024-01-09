import unittest
from unittest.mock import patch, MagicMock
from app.database.crud import survey_crud


class SurveyCrudTest(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()

    def tearDown(self):
        pass

    @patch('app.database.crud.survey_crud.get_survey',
           return_value={
               "id": "10000000-0000-0000-0000-000000000000",
               "creator_id": "20000000-0000-0000-0000-000000000000"
           })
    def test_get_survey(self, mock_get_survey):
        survey_id = "10000000-0000-0000-0000-000000000000"
        creator_id = "20000000-0000-0000-0000-000000000000"
        result = survey_crud.get_survey(self.db, survey_id)

        self.assertEqual(result, {"id": survey_id, "creator_id": creator_id})
        mock_get_survey.assert_called_once_with(self.db, survey_id)
